import os
from ctypes import CDLL, POINTER, c_int, c_float, byref, sizeof
import numpy as np
from numpy.ctypeslib import ndpointer
from mpi4py import MPI

_libdir = os.path.dirname(__file__)

if MPI._sizeof(MPI.Comm) == sizeof(c_int):
    MPI_Comm = c_int
else:
    MPI_Comm = c_void_p
_libc = CDLL(os.path.join(_libdir, "libgcommc.so"))
_libc.sayhello.restype = None
_libc.sayhello.argtypes = [MPI_Comm]
_libc.scatter.restype = None
_libc.scatter.argtypes = [MPI_Comm, ndpointer(c_float), c_int, ndpointer(c_float), c_int, c_int]

def sayhello(comm):
    comm_ptr = MPI._addressof(comm)
    comm_val = MPI_Comm.from_address(comm_ptr)
    _libc.sayhello(comm_val)

def scatter_p(comm, sendbuf, recvbuf, root):
    comm.Scatter(sendbuf, recvbuf, root)

def scatter_c(comm, sendbuf, recvbuf, root):
    comm_ptr = MPI._addressof(comm)
    comm_val = MPI_Comm.from_address(comm_ptr)
    if sendbuf is None:
        sendbuf = np.zeros([recvbuf.size], dtype='f4')
        size_ = sendbuf.size
    else:
        size_ = sendbuf.size
    _libc.scatter(comm_val, sendbuf, size_, recvbuf, recvbuf.size, root)
