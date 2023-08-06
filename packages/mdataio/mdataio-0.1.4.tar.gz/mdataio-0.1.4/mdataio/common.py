import numpy as np
import os
import re

def normalize(arr):
    arr = arr.astype('float32')
    arr_min = np.min(arr)
    output = (arr-arr_min)/(np.max(arr)-arr_min +1e-5)
    return output

def mkdir_p(path):
    exist = True
    if not os.path.exists(path):
        exist = False
        os.makedirs(path)
    return exist


def load_npz(path):
    a = np.load(path)
    a = a[a.files[0]]
    return a
