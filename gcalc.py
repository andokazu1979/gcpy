import os
from ctypes import CDLL, POINTER, c_int, c_float, byref
from numpy.ctypeslib import ndpointer

_libdir = os.path.dirname(__file__)

_libc = CDLL(os.path.join(_libdir, "libgcalcc.so"))
_libc.scaling.restype = None
_libc.scaling.argtypes = [c_int, ndpointer(c_float), c_int, c_int, c_int, c_int]

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
    _libf.scaling_(byref(c_int(num)), arr, byref(c_int(nx)), byref(c_int(ny)), byref(c_int(nz)), byref(c_int(nz)))
