import numpy as np
import cv2
import timeit
from matplotlib import pyplot as plt
import matplotlib.animation as anim
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class VideoSaver:
    """
    The VideoSaver class servers as the wrapper for the video saving functionality

    Parameters
    ----------
    input_list: a list of numpy arrays [img1, img2, ... imgN], imgs can be of size of HxW for gray
    scale image or size of HxWx3 for RGB image
                or a list of list of numpy arrays [[img1, img2], [img1, img2] ...]. This is useful to
                show volumes side by side.
                Each single item in the outmost list composes a single frame

    """
    def __init__(self, input_list):
        if len(input_list) == 0:
            raise Exception('input list has to have more than 1 item')
        self.input_list = input_list

    def to_video(self, filename):
        rows = 1
        if isinstance(self.input_list[0], np.ndarray):
            cols = 1
            fps = int(self.input_list[0].shape[0]/5)
        elif isinstance(self.input_list[0], list):
            cols = len(self.input_list[0])
            fps = int(self.input_list[0][0].shape[0]/5)
        else:
            raise Exception('Currently only support numpy array or list of numpy array')

        fig, axes = plt.subplots(rows, cols)
        if rows*cols == 1:
            axes = [axes]
        fig.subplots_adjust(left=0.05, bottom=0.1, right=0.95, top=0.9, wspace=None, hspace=None)
        fig.set_size_inches(4*cols, 4, forward=True)

        to_be_annimated = []
        for item in self.input_list:
            if isinstance(item, np.ndarray):
                img_list = [item]
            elif isinstance(item, list):
                img_list = item
            else:
                raise Exception('Currently only support numpy array or list of numpy array')

            frame = []
            for i, img in enumerate(img_list):
                if img.ndim == 2:
                    subframe = axes[i].imshow(img, cmap='gray')
                elif img.ndim == 3:
                    subframe = axes[i].imshow(img)
                frame.append(subframe)
            to_be_annimated.append(frame)
        ani = anim.ArtistAnimation(fig, to_be_annimated, repeat_delay=1000)

        ani.save(filename, fps=fps)
        print('saving video at {} fps finished'.format(fps))

        fig.clear()
        plt.close(fig)


