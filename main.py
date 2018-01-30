#! /usr/bin/env python

from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
nproc = comm.Get_size()
rank = comm.Get_rank()

# print("nproc: {0}, rank {1}\n".format(nproc, rank))

msize = int(sys.argv[1])

sendbuf = None
if rank == 0:
    grid = np.ones([msize,msize], dtype='i')
    print("initial:\n{0}\n".format(grid))
    sendbuf = grid

recvbuf = np.zeros([msize/nproc,msize], dtype='i')

comm.Scatter(sendbuf, recvbuf, root=0)

# print("rank{0}:\nrecvbuf={1}\n".format(rank, recvbuf))

subgrid = recvbuf

sendbuf = subgrid * rank

if rank == 0:
    recvbuf = np.zeros([msize,msize], dtype='i')
comm.Gather(sendbuf, recvbuf, root=0)

if rank == 0:
    print("result:\n{1}\n".format(rank, recvbuf))


