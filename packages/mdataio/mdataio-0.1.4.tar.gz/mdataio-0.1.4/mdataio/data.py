import os
import time
import glob
from pathlib import Path
import numpy as np
import SimpleITK as sitk
import pydicom as dicom
import nibabel as nib
from medpy.io import load
from multiprocessing import Pool

from .common import mkdir_p

class PatientBase:
    def __init__(self, root, logger=None):
        self.root = root
        self.file = Path(root)
        self.logger = logger

    def get_data(self):
        raise NotImplementedError("Define get_data for {} class".
                                  format(self.__class__.__name__))

    def _read_data(self):
        raise NotImplementedError("Define _read_data for {} class".
                                  format(self.__class__.__name__))

    def _write_slices(self, writer, series_tag_values, new_img, i, root_output):
        image_slice = new_img[:,:,i]

        # Tags shared by the series.
        list(map(lambda tag_value: image_slice.SetMetaData(tag_value[0], tag_value[1]), series_tag_values))

        # Slice specific tags.
        image_slice.SetMetaData("0008|0012", time.strftime("%Y%m%d")) # Instance Creation Date
        image_slice.SetMetaData("0008|0013", time.strftime("%H%M%S")) # Instance Creation Time

        # Setting the type to CT preserves the slice location.
        image_slice.SetMetaData("0008|0060", "CT")  # set the type to CT so the thickness is carried over
        # print(new_img.TransformIndexToPhysicalPoint((0,0,i)))
        # (0020, 0032) image position patient determines the 3D spacing between slices.
        image_slice.SetMetaData("0020|0032", '\\'.join(map(str,new_img.TransformIndexToPhysicalPoint((0,0,i))))) # Image Position (Patient)
        image_slice.SetMetaData("0020|0013", str(i)) # Instance Number
        image_slice.SetMetaData("0020|1041", str(-new_img.TransformIndexToPhysicalPoint((0,0,i))[2])) # Instance Number

        # Write to the output directory and add the extension dcm, to force writing in DICOM format.
        writer.SetFileName(os.path.join(root_output, str(i)+'.dcm'))
        writer.Execute(image_slice)

    def save_as_dicom(self, root_output, intercept=0):
        mkdir_p(root_output)

        sliceThickness = self.spacing[0] # Slice thickness
        patientName = str(self.file.name).split('.')[0]

        img = self.img + intercept

        new_img = sitk.GetImageFromArray(img)
        new_img.SetSpacing([self.spacing[1].item(), self.spacing[2].item(), self.spacing[0].item()])

        writer = sitk.ImageFileWriter()
        # Use the study/series/frame of reference information given in the meta-data
        # dictionary and not the automatically generated information from the file IO
        writer.KeepOriginalImageUIDOn()

        modification_time = time.strftime("%H%M%S")
        modification_date = time.strftime("%Y%m%d")

        # Copy some of the tags and add the relevant tags indicating the change.
        # For the series instance UID (0020|000e), each of the components is a number, cannot start
        # with zero, and separated by a '.' We create a unique series ID using the date and time.
        # tags of interest:
        direction = new_img.GetDirection()
        series_tag_values = [("0008|0031",modification_time), # Series Time
                            ("0008|0030",modification_time), # study time, this piece is critical for cvi42 to load, otherwise it will splited into 2 studies
                            ("0008|0021",modification_date), # Series Date
                            ("0008|0008","DERIVED\\SECONDARY"), # Image Type
                            ("0020|000e", "1.2.826.0.1.3680043.2.1125."+modification_date+".1"+modification_time), # Series Instance UID
                            ("0020|000d", "1.2.826.0.1.3680043.2.1125."+modification_date+".1"+modification_time), # study Instance UID, must have to organize all images together!!!!!
                            ("0020|0037", '\\'.join(map(str, (direction[0], direction[3], direction[6],# Image Orientation (Patient)
                                                                    direction[1],direction[4],direction[7])))),
                            ("0008|103e", "Created-SimpleITK"),
                            ("0010|0010", patientName),
                            ("0028|1053", "1"),
                            # ("0028|1052", "-1024"),
                            ("0028|1052", "0"),
                            ("0020|0011", "1"),#series number
                            ("0020|0012", "1"),#acquization number
                            ("0018|0050", str(sliceThickness)) #slice thickness
                            ] # Series Description

        # Write slices to output directory
        list(map(lambda i: self._write_slices(writer, series_tag_values, new_img, i, root_output), range(new_img.GetDepth())))

class PatientDicom(PatientBase):
    def __init__(self, root, logger=None, preview=False, num_process=1):
        super().__init__(root, logger)
        self.img, self.res, self.hdr = self._read_data(preview=preview, num_process=num_process)
        self.spacing = self.res
        self.raw_data = {'img': self.img,
                        'res': self.res,
                        'hdr': self.hdr}

    def compute_slice_location(self, cosines, ipp):
        ipp_a = np.array(ipp)
        normal = np.zeros(ipp_a.shape)
        normal[0] = float(cosines[1]*cosines[5]-cosines[2]*cosines[4])
        normal[1] = float(cosines[2]*cosines[3]-cosines[0]*cosines[5])
        normal[2] = float(cosines[0]*cosines[4]-cosines[1]*cosines[3])
        return np.dot(normal,ipp_a)

    def parse_dcm_metadata(self, dcm):
        unpacked_data = {}
        group_elem_to_keywords = {}
        # iterating here to force conversion from lazy RawDataElement to DataElement
        for d in dcm:
            pass

        # keys are pydicom.tag.BaseTag, values are pydicom.dataelem.DataElement
        for tag, elem in dcm.items():
            tag_group = tag.group
            tag_elem = tag.elem
            keyword = elem.keyword
            group_elem_to_keywords[(tag_group, tag_elem)] = keyword
            value = elem.value
            if keyword != '' and keyword != 'PixelData':
                unpacked_data[keyword] = value
        # pprint(group_elem_to_keywords)
        return unpacked_data, group_elem_to_keywords


    def filtering_dcm_files_by_phase(self, dcm_files, request_phase=-1):
        #returning files from a single phase, if request_phase = -1, retrun the first phase that has non zero number of slices
        output_dcm_files = []
        phase_files = {}
        slice_locations = []

        # #this works for ali's annotation dataset
        sorted_dcm_files = sorted(dcm_files, key=lambda x:x.split('/')[-1].split('--')[0])
        #this works for ctt dataset
        # sorted_dcm_files = sorted(dcm_files, key=lambda x: int(''.join(x.split('/')[-1].split('.')[-4:])))

        for filename in sorted_dcm_files:
            try:
                dicom_raw = dicom.read_file(filename)
                meta_dict, _ = self.parse_dcm_metadata(dicom_raw)
                # print(meta_dict)
        # slice_locations.append(meta_dict['SliceLocation'])
                ipp = meta_dict['ImagePositionPatient']
                cosines = meta_dict['ImageOrientationPatient']
                slice_locations.append(self.compute_slice_location(cosines, ipp))
            except:
                print("{} has A PROBLEM!".format(filename))
                continue

        phase = 0
        phase_files[phase] = []
        if slice_locations[1] > slice_locations[0]:
            ascending = 1
        else:
            ascending = 0

        for i in range(0, len(slice_locations)-1):
            if ascending:
                if slice_locations[i+1] > slice_locations[i]:
                    phase_files[phase].append(sorted_dcm_files[i])
                else:
                    phase_files[phase].append(sorted_dcm_files[i])
                    phase += 1
                    phase_files[phase] = []

            else:
                if slice_locations[i+1] < slice_locations[i]:
                    phase_files[phase].append(sorted_dcm_files[i])
                else:
                    phase_files[phase].append(sorted_dcm_files[i])
                    phase += 1
                    phase_files[phase] = []

        phase_files[phase].append(sorted_dcm_files[i+1])

        print({key:len(value) for key, value in phase_files.items()})
        output_dcm_files = phase_files[0]
        if request_phase == -2:
            return phase_files
        elif request_phase == -1:
            return output_dcm_files

    def _process_each_dicom(self, f_path):
        desired_attributes = ['SeriesNumber', 'InstanceNumber', 'PixelSpacing',
                            'ImagePositionPatient', 'ImageOrientationPatient', 'StudyInstanceUID',
                            'SeriesInstanceUID', 'SOPInstanceUID', 'Manufacturer', 'SliceThickness'
                            ]
        header = {key:None for key in desired_attributes}

        try:
            ds = dicom.read_file(f_path)
            data = ds.pixel_array
        except:
            try:
                ds = dicom.read_file(f_path)
                file = sitk.ReadImage(f_path)
                data = sitk.GetArrayFromImage(file)
                data = np.squeeze(data)
            except:
                #print("{} cannot be loaded".format(f_path))
                return (None, None)

        for key in desired_attributes:
            if key != 'PixelData':
                header[key] = ds[key].value

        data = data * ds.RescaleSlope + ds.RescaleIntercept

        return (data, header)


    def _load_dicoms(self, source_dir, multiphases=False, preview=False, num_process=1):
    # _, dcm_files = find_files_with_ending(source_dir, '.dcm')
        dcm_files = glob.glob(source_dir+'/*.dcm')
        total_number_slices = len(dcm_files)

        if preview:
            dcm_files = dcm_files[0:1]

        locs = []
        dcms = []
        if multiphases:
            dcm_files = self.filtering_dcm_files_by_phase(dcm_files, -1)

        # print('numbe of dicom files {}'.format(len(dcm_files)))
        p = Pool(num_process)
        process_outputs = p.map(self._process_each_dicom, dcm_files)

        for i, v in enumerate(process_outputs):
            if v[0] is not None:
                v[1]['TotalNumberSlices'] = total_number_slices
                cosines = v[1]['ImageOrientationPatient']
                ipp = v[1]['ImagePositionPatient']
                real_slice_location = self.compute_slice_location(cosines, ipp)
                if not real_slice_location in locs:
                    dcms += [v]
                    locs += [real_slice_location]
        p.close()
        p.join()

        order = sorted(range(len(locs)), key=lambda k: locs[k])
        dcms = [ dcms[i] for i in order]
        locs = [ locs[i] for i in order]
        return dcms, locs


    def _read_data(self, preview=False, num_process=1):
        flag_multiphases = False
        dcms, _ = self._load_dicoms(self.root, multiphases=flag_multiphases, preview=preview, num_process=num_process)
        hdr = dcms[0][1]
        z_len = len(dcms)
        z_del = (dcms[z_len-1][1]['ImagePositionPatient'][-1]-dcms[0][1]['ImagePositionPatient'][-1])/z_len
        hdr['SliceSpacing'] = z_del

        img_arrays = [dcms[dcm_idx][0] for dcm_idx in range(0, len(dcms))]
        img_arrays_shape = [dcms[dcm_idx][0].shape for dcm_idx in range(0, len(dcms))]
        img = np.stack(img_arrays, axis=0)
        img = img.astype('int16')


        res = np.array([float(hdr['SliceSpacing']),
                       float(hdr['PixelSpacing'][0]),
                       float(hdr['PixelSpacing'][1])],
                        dtype=np.float32
                       )

        full_hdr = {'ImagePositionPatient': [],
                    'ImageOrientationPatient': [],
                    'SeriesNumber': hdr['SeriesNumber'],
                    'InstanceNumber': hdr['InstanceNumber'],
                    'StudyInstanceUID': [],
                    'SeriesInstanceUID': [],
                    'SOPInstanceUID': [],
                    'SliceSpacing': hdr['SliceSpacing'],
                    'PixelSpacing': hdr['PixelSpacing'],
                    'Manufacturer': hdr['Manufacturer'],
                    'SliceThickness': hdr['SliceThickness'],
                    'TotalNumberSlices': hdr['TotalNumberSlices']
                    }
        for i in range(len(dcms)):
            full_hdr['ImagePositionPatient'].append(dcms[i][1]['ImagePositionPatient'])
            full_hdr['ImageOrientationPatient'].append(dcms[i][1]['ImageOrientationPatient'])
            full_hdr['StudyInstanceUID'].append(dcms[i][1]['StudyInstanceUID'])
            full_hdr['SeriesInstanceUID'].append(dcms[i][1]['SeriesInstanceUID'])
            full_hdr['SOPInstanceUID'].append(dcms[i][1]['SOPInstanceUID'])

        return img, res, full_hdr

    def get_data(self, return_list=['img', 'res']):
        to_return = []
        for i in return_list:
            to_return.append(self.raw_data[i])
        return tuple(to_return)

class PatientNifty(PatientBase):
    def __init__(self, filename):
        self.file = Path(filename)
        niiData = nib.load(filename)
        self.niiImg = niiData.get_data()
        self.niiHdr = niiData.header
        self.img, self.spacing = self._read_data()

    def _read_data(self):
        img = self.niiImg
        img = img.astype('int16')
        if img.ndim == 3:
            img = np.transpose(img, [2,0,1])
        elif img.ndim == 4:
            img = np.transpose(img, [3,2,0,1])

        hdr = self.niiHdr
        res = np.array([hdr["pixdim"][3], hdr["pixdim"][2], hdr["pixdim"][1]])

        return img, res

    def get_data(self):
        return self.img, self.spacing

class PatientMha(PatientBase):
    def __init__(self, filename):
        self.file = Path(filename)
        self.mhaData, self.mhaHeader = load(filename)
        self.img, self.spacing = self._read_data()

    def _read_data(self):
        img = self.mhaData

        img = img.astype('int16')
        spacing_list = self.mhaHeader.get_voxel_spacing()
        spacing = np.array([spacing_list[2], spacing_list[0], spacing_list[1]])
        img = img.transpose([2,1,0])

        return img, spacing

    def get_data(self):
        return self.img, self.res

class PatientMhd(PatientBase):
    def __init__(self, filename):
        self.file = Path(filename)
        self.itkimage = sitk.ReadImage(filename)
        self.img, self.spacing = self._read_data()

    def _read_data(self):
        img = sitk.GetArrayFromImage(self.itkimage)
        img = img.astype('int16')

        spacing = self.itkimage.GetSpacing()
        res = np.array([spacing[2], spacing[1], spacing[0]])

        return img, res

    def get_data(self):
        return self.img, self.spacing

