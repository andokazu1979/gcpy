#! /usr/bin/env python

from mpi4py import MPI
import numpy as np
import sys

import gcalc
import gcomm

########################################
# Initialization for MPI
########################################

comm = MPI.COMM_WORLD
nproc = comm.Get_size()
rank = comm.Get_rank()

########################################
# Initialize grid
########################################

gsize = int(sys.argv[1])

########################################
# Scatter grid
########################################

# sendbuf = None
# if rank == 0:
    # grid = np.ones([gsize,gsize], dtype='f4')
    # sendbuf = grid

# recvbuf = np.zeros([int(gsize/nproc),gsize], dtype='f4')

# gcomm.scatter_p(comm, sendbuf, recvbuf, root=0)
# # gcomm.scatter_c(comm, sendbuf, recvbuf, root=0)

# subgrid = recvbuf

# if rank == 0:
    # print("initial:\n{0}\n".format(grid))

subgrid = np.zeros([int(gsize/nproc),gsize], dtype='f4')

amode = MPI.MODE_RDONLY
fh = MPI.File.Open(comm, "./input.grd", amode)

# count_ = 10
# blocklength_ = 5
# stride_ = 10
blocklength_ = gsize / nproc
count_ = gsize ** 2 / blocklength_
stride_ = gsize
filetype = MPI.FLOAT.Create_vector(count_, blocklength_, stride_)
filetype.Commit()
offset = MPI.FLOAT.Get_size() * blocklength_ * rank
fh.Set_view(offset, filetype=filetype)
fh.Read_at_all(0, subgrid)

fh.Close()

print("rank {0} input:\n{1}\n".format(rank, subgrid))

########################################
# Grid calculation
########################################

gcalc.scaling_p(rank, subgrid, subgrid.size)
# gcalc.scaling_c(rank, subgrid, subgrid.size)
# gcalc.scaling_f(rank, subgrid, subgrid.size)

########################################
# Gather grid
########################################

# sendbuf = subgrid

# if rank == 0:
    # recvbuf = np.zeros([gsize,gsize], dtype='f4')
# comm.Gather(sendbuf, recvbuf, root=0)

# if rank == 0:
    # print("result:\n{1}\n".format(rank, recvbuf))

print("rank {0} result:\n{1}\n".format(rank, subgrid))

amode = MPI.MODE_WRONLY|MPI.MODE_CREATE
fh = MPI.File.Open(comm, "./output.grd", amode)

# offset = rank*subgrid.nbytes
fh.Set_view(offset, filetype=filetype)
fh.Write_at_all(0, subgrid)

fh.Close()
