import os
import ctypes
from numpy.ctypeslib import ndpointer

_libdir = os.path.dirname(__file__)
_lib = ctypes.CDLL(os.path.join(_libdir, "libgcalc.so"))
_lib.scaling.restype = None
_lib.scaling.argtypes = [ctypes.c_int, ndpointer(ctypes.c_int), ctypes.c_int]

def scaling(num, arr, size):
    _lib.scaling(num, arr, size)
