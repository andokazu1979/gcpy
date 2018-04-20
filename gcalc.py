import os
from ctypes import CDLL, POINTER, c_int, c_float, byref
import numpy as np
from numpy.ctypeslib import ndpointer

_libdir = os.path.dirname(__file__)

_libc = CDLL(os.path.join(_libdir, "libgcalcc.so"))
_libc.scaling.restype = None
_libc.scaling.argtypes = [c_int, ndpointer(c_float), c_int, c_int, c_int, c_int]
_libc.subst.restype = None
_libc.subst.argtypes = [ndpointer(c_float), ndpointer(c_float), c_int]
_libc.sum.restype = None
_libc.sum.argtypes = [ndpointer(c_float), c_int, ndpointer(c_float), c_int]

_libf = CDLL(os.path.join(_libdir, "libgcalcf.so"))
_libf.scaling_.restype = None
_libf.scaling_.argtypes = [POINTER(c_int), ndpointer(c_float), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

def scaling_p(num, arr):
    arr *= num

def scaling_c(num, arr):
    nx = arr.shape[3]
    ny = arr.shape[2]
    nz = arr.shape[1]
    nt = arr.shape[0]
    _libc.scaling(num, arr, nx, ny, nz, nt)

def scaling_f(num, arr):
    nx = arr.shape[3]
    ny = arr.shape[2]
    nz = arr.shape[1]
    nt = arr.shape[0]
    _libf.scaling_(byref(c_int(num)), arr, byref(c_int(nx)), byref(c_int(ny)), byref(c_int(nz)), byref(c_int(nt)))

def subst_p(arr1, arr2):
    np.copyto(arr1, arr2)

def subst_c(arr1, arr2):
    _libc.subst(arr1, arr2, arr1.size)

def sum_c(arr, dim=None):
    if dim is None:
        length = arr.size
        arr_tmp = np.zeros(1).astype(np.float32)
    else:
        length = arr.shape[dim]
        arr_tmp = np.zeros(arr.shape).astype(np.float32).sum(dim)
    lst_trans = _get_trans_shape(arr.ndim, dim)
    _libc.sum(arr_tmp, length, arr.transpose(lst_trans).copy(), arr.size)
    return arr_tmp

def _get_trans_shape(n, dim):
    if dim is None:
        lst = range(n)
    else:
        lst = []
        for i in range(n):
            if i != dim:
                lst.append(i)
        lst.append(dim)
    return lst

