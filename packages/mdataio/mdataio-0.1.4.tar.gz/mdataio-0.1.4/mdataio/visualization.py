import numpy as np
import cv2
import timeit
from matplotlib import pyplot as plt
import matplotlib.animation as anim
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.cm as pltcm
import matplotlib
from .common import normalize
matplotlib.use('tkAgg')
#https://matplotlib.org/tutorials/introductory/usage.html#what-is-a-backend

def imshow(img, cmap='gray', title=None, points=None):
    '''to show a single 2D image, points are assume to have a shape of Nx2'''
    def drawImage(ax, img, title, pts):
        ax.clear()
        if img.ndim == 3:
            ax.imshow(img)
        elif img.ndim == 2:
            ax.imshow(img, cmap=cmap, vmin=vmin, vmax=vmax)

        if title is not None:
            ax.set_title(title, fontdict={'fontsize': 8})

        if pts is not None:
            pts_color = pltcm.rainbow(np.linspace(0, 1, pts.shape[0]))#['red', 'green', 'blue', 'yellow']
            ax.scatter(x=pts[:,1], y=pts[:,0], c=pts_color[0:pts.shape[0]], s=10, marker='*')
        plt.draw()

    def onpress(event):
        nonlocal key_pressed
        key_pressed = event.key

    if img.ndim < 2 or img.ndim > 3:
        raise Exception('Only image of dims 2 and 3 are currently supported')
    vmin = np.min(img)
    vmax = np.max(img)

    fig, ax = plt.subplots()

    cid = fig.canvas.mpl_connect('key_press_event', onpress)

    key_pressed = None
    drawImage(ax, img, title, points)


    while True:
        plt.waitforbuttonpress()

        if key_pressed == 'escape':
            fig.clear()
            fig.canvas.mpl_disconnect(cid)
            plt.close(fig)
            break


def imshowlist(img_list, cmap_list=None, title_list=None, points_list=None, row=1):
    '''to show a list a 2D images side by side'''
    def drawImages(axes, img_list, title_list, pts_list):
        for i in range(len(img_list)):
            row_idx = i // col
            col_idx = i % col
            if title_list is not None:
                title = title_list[i]
            else:
                title = None

            if points_list is not None:
                pts = pts_list[i]
            else:
                pts = None

            axes[row_idx, col_idx].clear()
            if img_list[i].ndim == 3:
                axes[row_idx, col_idx].imshow(img_list[i])
            else:
                axes[row_idx, col_idx].imshow(img_list[i], cmap=cmap_list[i], vmin=vmin_list[i], vmax=vmax_list[i])

            if title is not None:
                axes[row_idx, col_idx].set_title(title, fontdict={'fontsize': 8})

            if pts is not None:
                pts_color = pltcm.rainbow(np.linspace(0, 1, pts.shape[0]))#['red', 'green', 'blue', 'yellow']
                axes[row_idx, col_idx].scatter(x=pts[:,1], y=pts[:,0], c=pts_color[0:pts.shape[0]], s=10, marker='*')
        plt.draw()

    def onpress(event):
        nonlocal key_pressed
        key_pressed = event.key


    if (len(img_list) <= 1):
        raise Exception('the input list should have at least 2 images')
    elif cmap_list != None:
        if (len(img_list) != len(cmap_list)):
            raise Exception('the input image list and the cmap list should have the same # of elements')

    for i in range(len(img_list)-1):
        if img_list[i].ndim < 2 or img_list[i].ndim > 4:
            raise Exception('Only image of dims 2 (HxW) and 3 (HxWx3) are currently supported')

    vmin_list = [np.min(img) for img in img_list]
    vmax_list = [np.max(img) for img in img_list]


    if cmap_list == None:
        cmap_list = ['gray' for i in range(len(img_list))]

    col = int(np.ceil(len(img_list) / row))
    fig, axes = plt.subplots(row, col)
    if np.ndim(axes) == 1:
        if row == 1:
            axes = np.expand_dims(axes, axis=0)
        elif col == 1:
            axes = np.expand_dims(axes, axis=-1)
    elif np.ndim(axes) == 0:
        axes = np.array([[axes]])

    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=None, hspace=None)
    # fig.set_size_inches(8, 4, forward=True)

    cid = fig.canvas.mpl_connect('key_press_event', onpress)

    key_pressed = None

    drawImages(axes, img_list, title_list, points_list)


    while True:
        plt.waitforbuttonpress()

        if key_pressed == 'escape':
            fig.clear()
            fig.canvas.mpl_disconnect(cid)
            plt.close(fig)
            break


        key_pressed = None

        drawImages(axes, img_list, title_list, points_list)


def volshow(img, cmap='gray'):
    '''to show a single 3D volume with functionality of go through each
    single slice interactively'''
    def drawImage(ax, img):
        ax.clear()
        ax.set_title('slice {}/{}'.format(zidx, depth))
        if img.ndim == 3:
            ax.imshow(img)
        else:
            ax.imshow(img, cmap=cmap, vmin=vmin, vmax=vmax)
        plt.draw()

    def onpress(event):
        nonlocal key_pressed
        key_pressed = event.key


    if img.ndim < 2 or img.ndim > 3:
        raise Exception('Only image of dims 2 and 3 are currently supported')
    vmin = np.min(img)
    vmax = np.max(img)

    ndim = img.ndim
    if ndim == 3 or ndim ==4:
        depth = img.shape[0]
    elif ndim == 2:
        depth = 1

    fig, ax = plt.subplots()

    cid = fig.canvas.mpl_connect('key_press_event', onpress)

    key_pressed = None
    zidx = 0
    if ndim == 2:
        img_slice = img
    elif ndim == 3 or ndim == 4:
        img_slice = img[zidx]
    drawImage(ax, img_slice)


    while True:
        plt.waitforbuttonpress()

        if key_pressed == 'escape':
            fig.clear()
            fig.canvas.mpl_disconnect(cid)
            plt.close(fig)
            break
        elif key_pressed == '.' and (ndim == 3 or ndim == 4):
            zidx += 1
            if zidx >= img.shape[0]:
                zidx = img.shape[0]-1
        elif key_pressed == ',' and (ndim == 3 or ndim == 4):
            zidx -= 1
            if zidx < 0:
                zidx = 0


        key_pressed = None
        if ndim == 2:
            img_slice = img
        elif ndim == 3 or ndim == 4:
            img_slice = img[zidx]
        drawImage(ax, img_slice)


def volshowlist(vol_list, cmap_list=None):
    '''to show a list of 3D volumes with functionality of go through the same
    slice of them side by side interactively
    '''
    def drawImages(axes, img_slice_list):
        for i in range(len(img_slice_list)):
            axes[i].clear()
            axes[i].set_title('slice {}/{}'.format(zidx, depth))
            if img_slice_list[i].ndim == 3:
                axes[i].imshow(img_slice_list[i])
            else:
                axes[i].imshow(img_slice_list[i], cmap=cmap_list[i], vmin=vmin_list[i], vmax=vmax_list[i])
        plt.draw()

    def onpress(event):
        nonlocal key_pressed
        key_pressed = event.key


    if (len(vol_list) <= 1):
        raise Exception('the input list should have at least 2 images')
    elif cmap_list != None:
        if (len(vol_list) != len(cmap_list)):
            raise Exception('the input image list and the cmap list should have the same # of elements')

    for i in range(len(vol_list)-1):
        if vol_list[i].ndim < 2 or vol_list[i].ndim > 4:
            raise Exception('Only image of dims 2 and 3 are currently supported')

    vmin_list = [np.min(img) for img in vol_list]
    vmax_list = [np.max(img) for img in vol_list]

    ndim = vol_list[0].ndim
    if ndim == 3 or ndim == 4:
        depth = vol_list[0].shape[0]
    elif ndim == 2:
        depth = 1

    if cmap_list == None:
        cmap_list = ['gray' for i in range(len(vol_list))]

    fig, axes = plt.subplots(1, len(vol_list))
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=None, hspace=None)
    # fig.set_size_inches(8, 4, forward=True)

    cid = fig.canvas.mpl_connect('key_press_event', onpress)

    key_pressed = None
    zidx = 0
    if ndim == 2:
        img_slice_list = [img for img in vol_list]
    elif ndim == 3 or ndim == 4:
        img_slice_list = [img[zidx] for img in vol_list]

    drawImages(axes, img_slice_list)


    while True:
        plt.waitforbuttonpress()

        if key_pressed == 'escape':
            fig.clear()
            fig.canvas.mpl_disconnect(cid)
            plt.close(fig)
            break
        elif key_pressed == '.' and (ndim == 3 or ndim == 4):
            zidx += 1
            if zidx >= vol_list[0].shape[0]:
                zidx = vol_list[0].shape[0]-1
        elif key_pressed == ',' and (ndim == 3 or ndim == 4):
            zidx -= 1
            if zidx < 0:
                zidx = 0


        key_pressed = None
        if ndim == 2:
            img_slice_list = [img for img in vol_list]
        elif ndim == 3 or ndim == 4:
            img_slice_list = [img[zidx] for img in vol_list]

        drawImages(axes, img_slice_list)


def change_label(seg, unique_label=None):
    if unique_label is None:
        unique_label = np.unique(seg)

    new_seg = np.zeros_like(seg, dtype='uint8')
    new_color = np.linspace(0,255, unique_label.size)
    for i in range(unique_label.size):
        new_seg[seg==unique_label[i]] = new_color[i]
    return new_seg


def overlay_image(img1, img2, cm='jet', unique_label=None, method='mask'):
    #img1 and img2 are both 2d image
    if method == 'mask':
        overlayed_image = np.zeros(img1.shape + (3,), dtype='float32')
        img1 = normalize(img1)*255
        img1 = np.expand_dims(img1, -1)
        img1 = np.repeat(img1, 3, axis=-1)
        cm_dict = {'autumn': cv2.COLORMAP_AUTUMN,
                    'cool': cv2.COLORMAP_COOL,
                    'hot': cv2.COLORMAP_HOT,
                    'hsv': cv2.COLORMAP_HSV,
                    'jet': cv2.COLORMAP_JET,
                    'rainbow': cv2.COLORMAP_RAINBOW,
                    'spring': cv2.COLORMAP_SPRING,
                    'summer': cv2.COLORMAP_SUMMER,
                    'winter': cv2.COLORMAP_WINTER}

        seg_newlabel = change_label(img2, unique_label=unique_label)
        colormap = cv2.applyColorMap(seg_newlabel, cm_dict[cm])
        colormap = cv2.cvtColor(colormap, cv2.COLOR_BGR2RGB)
        colormap = colormap.astype('float32')

        bk_mask = np.zeros_like(img2)
        bk_mask[img2 == 0] = 1
        bk_mask = np.expand_dims(bk_mask, -1)
        bk_mask = np.repeat(bk_mask, 3, axis=-1)
        colormap[bk_mask>0] = img1[bk_mask>0]

        overlayed_image = colormap * 0.4 + img1 * 0.6

        overlayed_image  = overlayed_image.astype('uint8')
    elif method == 'contour':
        img1 = normalize(img1)*255
        img1 = np.expand_dims(img1, -1)
        overlayed_image = np.repeat(img1, 3, axis=-1).astype('uint8')
        current_label = np.unique(img2)
        if unique_label is None:
            unique_label = np.unique(img2)

        cm_dict = {'autumn': cv2.COLORMAP_AUTUMN,
                    'cool': cv2.COLORMAP_COOL,
                    'hot': cv2.COLORMAP_HOT,
                    'hsv': cv2.COLORMAP_HSV,
                    'jet': cv2.COLORMAP_JET,
                    'rainbow': cv2.COLORMAP_RAINBOW,
                    'spring': cv2.COLORMAP_SPRING,
                    'summer': cv2.COLORMAP_SUMMER,
                    'winter': cv2.COLORMAP_WINTER}

        seg_newlabel = change_label(current_label, unique_label=unique_label)
        colormap = cv2.applyColorMap(seg_newlabel, cm_dict[cm])
        colormap = cv2.cvtColor(colormap, cv2.COLOR_BGR2RGB)
        for idx, label in enumerate(current_label.tolist()):
            if label != 0:
                binary_mask = img2 == label
                mask = binary_mask.astype('uint8')
                #approx_simple removes redundent points
                _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                longest_c = []
                for c in contours:
                    if len(c) > len(longest_c):
                        longest_c = c
                #put the contour in a list so that drawContour connects them
                cv2.drawContours(overlayed_image, [longest_c], -1, colormap[idx, 0].tolist(), thickness=1)

    else:
        raise Exception('only able to show contour|mask')

    return overlayed_image

def diff_image(img1, img2):
    #img1 and img2 are both 2d image of size HxW
    assert(img1.shape == img2.shape)
    assert(np.ndim(img1) == 2)

    # HxWx3
    diffed_img = np.zeros(img1.shape + (3,), dtype='float32')
    diffed_img[:, :, 0] = img1
    diffed_img[:, :, 1] = img2
    diffed_img[:, :, 2] = img1

    diffed_img = normalize(diffed_img)*255
    diffed_img = diffed_img.astype('uint8')
    return diffed_img

def diff_vol(img1, img2):
    #img1 and img2 are both 3d volumes of size DxHxW
    assert(img1.shape == img2.shape)
    assert(np.ndim(img1) == 3)

    # DxHxWx3
    diffed_vol = [diff_image(img1[i,:,:], img2[i,:,:]) for i in range(img1.shape[0])]
    diffed_vol = np.stack(diffed_vol, axis=0)
    return diffed_vol

def overlay_vol(img1, img2, cm='jet', unique_label=None, method='mask'):
    #img1 and img2 are both 3d volumes of size DxHxW
    assert(img1.shape == img2.shape)
    assert(np.ndim(img1) == 3)

    # DxHxWx3
    overlaid_vol = [overlay_image(img1[i,:,:], img2[i,:,:],
                    cm=cm,
                    unique_label=unique_label,
                    method=method) for i in range(img1.shape[0])]
    overlaid_vol = np.stack(overlaid_vol, axis=0)
    return overlaid_vol

def volshowpair(img1, img2, vis_type='overlay', method='mask', cm='jet'):
    def drawImage(ax, img):
        ax.clear()
        ax.set_title('slice {}/{}'.format(zidx, depth))
        ax.imshow(img)

        plt.draw()

    def onpress(event):
        nonlocal key_pressed
        key_pressed = event.key


    if (img1.shape != img2.shape):
        raise Exception('The two input image should have the same dimension')
    elif img1.ndim < 2 or img1.ndim > 3:
        raise Exception('Only image of dims 2 and 3 are currently supported')

    ndim = img1.ndim
    if ndim == 3:
        depth = img1.shape[0]
    elif ndim == 2:
        depth = 1

    fig, ax = plt.subplots()
    cid = fig.canvas.mpl_connect('key_press_event', onpress)

    key_pressed = None
    zidx = 0
    unique_label = np.unique(img2)

    if vis_type == 'overlay':
        if ndim == 3:
            img_overlay = overlay_image(img1[zidx, :, :],
                                        img2[zidx, :, :],
                                        unique_label=unique_label,
                                        method=method,
                                        cm=cm)
        elif ndim == 2:
            img_overlay = overlay_image(img1, img2, cm=cm)
        img_toshow = img_overlay
    elif vis_type == 'diff':
        if ndim == 3:
            img_diff = diff_image(img1[zidx, :, :], img2[zidx, :, :])
        elif ndim == 2:
            img_diff = overlay_image(img1, img2)
        img_toshow = img_diff
    else:
        raise Exception('Currently only support overlay|diff')
    drawImage(ax, img_toshow)


    while True:
        plt.waitforbuttonpress()

        if key_pressed == 'escape':
            fig.clear()
            fig.canvas.mpl_disconnect(cid)
            plt.close(fig)
            break
        elif key_pressed == '.' and ndim == 3:
            zidx += 1
            if zidx >= img1.shape[0]:
                zidx = img1.shape[0]-1
        elif key_pressed == ',' and ndim == 3:
            zidx -= 1
            if zidx < 0:
                zidx = 0

        key_pressed = None
        if vis_type == 'overlay':
            if ndim == 3:
                img_overlay = overlay_image(img1[zidx, :, :],
                                            img2[zidx, :, :],
                                            unique_label=unique_label,
                                            method=method,
                                            cm=cm)
            elif ndim == 2:
                img_overlay = overlay_image(img1, img2, cm=cm)
            img_toshow = img_overlay
        elif vis_type == 'diff':
            if ndim == 3:
                img_diff = diff_image(img1[zidx, :, :], img2[zidx, :, :])
            elif ndim == 2:
                img_diff = overlay_image(img1, img2)
            img_toshow = img_diff
        else:
            raise Exception('Currently only support overlay|diff')
        drawImage(ax, img_toshow)


def volshow3d(y_list, label_list=None, down_sample=1, marker_scale=2, alpha=0.1, cm='jet', mode='interactive'):
    def onpress(event):
        nonlocal key_pressed
        key_pressed = event.key


    if isinstance(y_list, np.ndarray):
        y_list = [y_list]
    elif not isinstance(y_list, list):
        raise Exception('Currently only support numpy array or list of numpy array')

    if label_list == None:
        label_list = np.unique(y_list[0]).tolist()

    fig = plt.figure(0)
    cid = fig.canvas.mpl_connect('key_press_event', onpress)
    key_pressed = None

    mNumCols = 4
    num = len(y_list)
    nrows = num//mNumCols + 1
    if num < mNumCols:
        ncols = num
    else:
        ncols = mNumCols

    #color_dict = {i:np.random.rand(1,3) for i in label_list}
    #create color map for the points
    cm_dict = {'autumn': cv2.COLORMAP_AUTUMN,
                'cool': cv2.COLORMAP_COOL,
                'hot': cv2.COLORMAP_HOT,
                'hsv': cv2.COLORMAP_HSV,
                'jet': cv2.COLORMAP_JET,
                'rainbow': cv2.COLORMAP_RAINBOW,
                'spring': cv2.COLORMAP_SPRING,
                'summer': cv2.COLORMAP_SUMMER,
                'winter': cv2.COLORMAP_WINTER}
    color_dict = {}
    seg_newlabel = change_label(np.expand_dims(np.array(label_list), -1), unique_label=np.array(label_list))
    colormap = cv2.applyColorMap(seg_newlabel, cm_dict[cm])
    colormap = cv2.cvtColor(colormap, cv2.COLOR_BGR2RGB)
    for idx, label in enumerate(label_list):
        color_dict[label] = colormap[idx,:,:].astype('float')/256

    for idx, y in enumerate(y_list):
        ax = fig.add_subplot(nrows, ncols, idx+1, projection='3d')
        ax.set_xlim([0, y.shape[2]])
        ax.set_ylim([0, y.shape[1]])
        ax.set_zlim([0, y.shape[0]])
        for label in label_list:
            pts = np.array(np.where(y==label))
            pts = pts[:,::down_sample]
            ax.scatter(pts[2,:],
                        pts[1,:],
                        pts[0,:],
                        alpha=alpha,
                        s=marker_scale,
                        c=color_dict[label])
            ax.set_title('{}'.format(idx))

    if mode == 'interactive':
        plt.draw()
        while True:
            plt.waitforbuttonpress()

            if key_pressed == 'escape':
                fig.clear()
                fig.canvas.mpl_disconnect(cid)
                plt.close(fig)
                break
    elif mode == 'silent':
        return fig, ax


def volshow3dmesh(y_list, label_list=None):
    def onpress(event):
        nonlocal key_pressed
        key_pressed = event.key


    if isinstance(y_list, np.ndarray):
        y_list = [y_list]
    elif not isinstance(y_list, list):
        raise Exception('Currently only support numpy array or list of numpy array')

    fig = plt.figure(0)
    cid = fig.canvas.mpl_connect('key_press_event', onpress)
    key_pressed = None

    mNumCols = 4
    num = len(y_list)
    nrows = num//mNumCols + 1
    if num < mNumCols:
        ncols = num
    else:
        ncols = mNumCols

    if label_list == None:
        label_list = np.unique(y_list[0]).tolist()

    color_dict = {i:np.random.rand(1,3) for i in label_list}
    for idx, y in enumerate(y_list):
        print(y.shape)
        ax = fig.add_subplot(nrows, ncols, idx+1, projection='3d')
        ax.set_xlim([0, y.shape[2]])
        ax.set_ylim([0, y.shape[1]])
        ax.set_zlim([0, y.shape[0]])
        for label in label_list:
            if label_list != 0:
                mask = y == label
                verts, faces, norm, val = measure.marching_cubes_lewiner(mask, step_size=20)
                verts = verts[:,::-1]

                mesh = Poly3DCollection(verts[faces], linewidths=0.1)
                mesh.set_edgecolor('k')
                mesh.set_facecolor(color_dict[label])
                mesh.set_alpha(1)
                ax.add_collection3d(mesh)

                ax.set_title('{}'.format(idx))

    plt.draw()
    while True:
        plt.waitforbuttonpress()

        if key_pressed == 'escape':
            fig.clear()
            fig.canvas.mpl_disconnect(cid)
            plt.close(fig)
            break

