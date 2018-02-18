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

sendbuf = None
if rank == 0:
    grid = np.ones([gsize,gsize], dtype='f4')
    sendbuf = grid

recvbuf = np.zeros([int(gsize/nproc),gsize], dtype='f4')

gcomm.scatter_p(comm, sendbuf, recvbuf, root=0)
# gcomm.scatter_c(comm, sendbuf, recvbuf, root=0)

subgrid = recvbuf

if rank == 0:
    print("initial:\n{0}\n".format(grid))

########################################
# Grid calculation
########################################

gcalc.scaling_p(rank, subgrid, subgrid.size)
# gcalc.scaling_c(rank, subgrid, subgrid.size)
# gcalc.scaling_f(rank, subgrid, subgrid.size)

########################################
# Gather grid
########################################

sendbuf = subgrid

if rank == 0:
    recvbuf = np.zeros([gsize,gsize], dtype='f4')
comm.Gather(sendbuf, recvbuf, root=0)

if rank == 0:
    print("result:\n{1}\n".format(rank, recvbuf))
