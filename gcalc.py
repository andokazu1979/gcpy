import os
from ctypes import CDLL, POINTER, c_int, c_float, byref
from numpy.ctypeslib import ndpointer

_libdir = os.path.dirname(__file__)

_libc = CDLL(os.path.join(_libdir, "libgcalcc.so"))
_libc.scaling.restype = None
_libc.scaling.argtypes = [c_int, ndpointer(c_float), c_int]

_libf = CDLL(os.path.join(_libdir, "libgcalcf.so"))
_libf.scaling_.restype = None
_libf.scaling_.argtypes = [POINTER(c_int), ndpointer(c_float), POINTER(c_int)]

def scaling_p(num, arr, size):
    arr *= num

def scaling_c(num, arr, size):
    _libc.scaling(num, arr, size)

def scaling_f(num, arr, size):
    _libf.scaling_(byref(c_int(num)), arr, byref(c_int(size)))
