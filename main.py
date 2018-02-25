#! /usr/bin/env python

from mpi4py import MPI
import numpy as np
import sys
import logging

import gcalc
import gcomm
import gtimer

level_ = logging.DEBUG
# level_ = logging.INFO
# level_ = logging.WARNING
# level_ = logging.ERROR
# level_ = logging.CRITCAL
logging.basicConfig(level = level_)
logger = logging.getLogger(__name__)

gtimer.timer_sta(0)

########################################
# Initialization for MPI
########################################

comm = MPI.COMM_WORLD
nproc = comm.Get_size()
rank = comm.Get_rank()

logger.debug("MPI_COMM_WORLD: nproc {0}, rank {1}".format(nproc, rank))

########################################
# Initialize grid
########################################

nx = int(sys.argv[1])
ny = int(sys.argv[2])
nz = int(sys.argv[3])

px = int(sys.argv[4])
py = int(sys.argv[5])
pz = int(sys.argv[6])

comm_ = comm.Create_cart((pz, py, px), reorder=True)
nproc = comm_.Get_size()
rank = comm_.Get_rank()

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


amode = MPI.MODE_RDONLY
fh = MPI.File.Open(comm_, sys.argv[7], amode)

sizes = (nz, ny, nx)
subsizes = (int(nz/pz), int(ny/py), int(nx/px))
subgrid = np.zeros(subsizes, dtype='f4')
coords = comm_.Get_coords(rank)
starts = (subsizes[0] * coords[0], subsizes[1] * coords[1], subsizes[2] * coords[2])
filetype = MPI.FLOAT.Create_subarray(sizes, subsizes, starts, MPI.ORDER_C)
filetype.Commit()
fh.Set_view(filetype=filetype)
fh.Read_at_all(0, subgrid)

fh.Close()

subgrid = subgrid.byteswap()

logger.debug("rank {0} input:\n{1}\n".format(rank, subgrid))

########################################
# Grid calculation
########################################

gcalc.scaling_p(rank, subgrid)
# gcalc.scaling_c(rank, subgrid)
# gcalc.scaling_f(rank, subgrid)

########################################
# Gather grid
########################################

# sendbuf = subgrid

# if rank == 0:
    # recvbuf = np.zeros([gsize,gsize], dtype='f4')
# comm.Gather(sendbuf, recvbuf, root=0)

# if rank == 0:
    # print("result:\n{1}\n".format(rank, recvbuf))

logger.debug("rank {0} result:\n{1}\n".format(rank, subgrid))

subgrid = subgrid.byteswap()

amode = MPI.MODE_WRONLY|MPI.MODE_CREATE
fh = MPI.File.Open(comm_, sys.argv[8], amode)

fh.Set_view(filetype=filetype)
fh.Write_at_all(0, subgrid)

fh.Close()

gtimer.timer_end(0)

logger.info("rank{0}: {1}".format(rank, gtimer.get_lst_elapse()))
