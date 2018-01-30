#! /usr/bin/env python

from mpi4py import MPI
import numpy as np
import sys

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
    grid = np.ones([gsize,gsize], dtype='i')
    print("initial:\n{0}\n".format(grid))
    sendbuf = grid

recvbuf = np.zeros([gsize/nproc,gsize], dtype='i')

comm.Scatter(sendbuf, recvbuf, root=0)

subgrid = recvbuf

########################################
# Grid calculation
########################################

subgrid = subgrid * rank

########################################
# Gather grid
########################################

sendbuf = subgrid

if rank == 0:
    recvbuf = np.zeros([gsize,gsize], dtype='i')
comm.Gather(sendbuf, recvbuf, root=0)

if rank == 0:
    print("result:\n{1}\n".format(rank, recvbuf))


