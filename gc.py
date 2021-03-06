#! /usr/bin/env python

import sys
import numpy as np
import logging

from mpi4py import MPI
import gcalc
import gio
import gcomm

level_ = logging.DEBUG
# level_ = logging.INFO
# level_ = logging.WARNING
# level_ = logging.ERROR
# level_ = logging.CRITCAL

comm = MPI.COMM_WORLD
nproc = comm.Get_size()
rank = comm.Get_rank()

logging.basicConfig(filename='log.{0:06d}'.format(rank), filemode='w', level=level_)
logger = logging.getLogger(__name__)

def init(conf):

    global nx, ny, nz, nt 
    global px, py, pz, pt 
    global comm, nproc, rank
    global subgrid, axis_reduce

    logger.debug("MPI_COMM_WORLD: nproc {0}, rank {1}".format(nproc, rank))

    calc_pattern = conf['global']['calc_pattern']
    exec_cond = conf[calc_pattern]['exec_cond']

    nx = int(exec_cond['nx'])
    ny = int(exec_cond['ny'])
    nz = int(exec_cond['nz'])
    nt = int(exec_cond['nt'])
    
    px = int(exec_cond['px'])
    py = int(exec_cond['py'])
    pz = int(exec_cond['pz'])
    pt = int(exec_cond['pt'])
     
    logger.debug("px: {0}, py: {1}, pz: {2}, pt: {3}".format(px, py, pz, pt))

    comm = comm.Create_cart((pt, pz, py, px), reorder=True)
    nproc = comm.Get_size()
    rank = comm.Get_rank()

    subsizes = (int(nt/pt), int(nz/pz), int(ny/py), int(nx/px))
    subgrid = np.zeros(subsizes, dtype='f4')
    axis_reduce = None

    return subgrid

def get_grid(nx, ny, nz, nt):
    subsizes = (int(nt/pt), int(nz/pz), int(ny/py), int(nx/px))
    subgrid = np.zeros(subsizes, dtype='f4')
    return subgrid

def read_grid(input_, subgrid, is_little=False):

    gio.read_grid(comm, input_, subgrid, is_little)

def grid_calc_scaling(subgrid):

    return gcalc.scaling_p(rank, subgrid)

def grid_calc_sum(subgrid, axis_reduce):

    return gcalc.sum_c(subgrid, axis_reduce)

def grid_calc_mean(grid, axis_reduce):

    # return gcalc.sum_c(grid, axis_reduce) / grid.shape[axis_reduce]
    return gcalc.sum_p(grid, axis_reduce) / grid.shape[axis_reduce]

def grid_calc_concat(grid, axis_reduce=None):

    return gcalc.sum_p(grid, axis_reduce) / grid.shape[axis_reduce]

def write_grid1(subgrid, output, is_little=False):
    gio.write_grid(comm, output, subgrid, is_little)

def write_grid2(subgrid, output, axis_reduce=None, is_little=False):

    shape = comm.Get_topo()[0]

    if axis_reduce is None: # Reduction with all axes
        recvbuf = None
        if comm.Get_rank() == 0:
            recvbuf = np.zeros(subgrid.shape, dtype='f4')
        gcomm.reduce_p(comm, subgrid, recvbuf, MPI.SUM, 0)
        if rank == 0:
            if is_little == False:
                recvbuf = recvbuf.byteswap()
            recvbuf.tofile(output) # Output serially with one process
    else: # Reduction with one axis
        comm_io = comm.Sub([int(i != axis_reduce) for i in range(4)])
        if shape[axis_reduce] > 1: # Number of domains in axis for reduction are more than one.

            comm_reduce = comm.Sub([int(i == axis_reduce) for i in range(4)])

            recvbuf = None
            if comm_reduce.Get_rank() == 0:
                recvbuf = np.zeros(subgrid.shape, dtype='f4')
            gcomm.reduce_p(comm_reduce, subgrid, recvbuf, MPI.SUM, 0) # Reduction through domains in axis for reduction

            if comm_reduce.Get_rank() == 0:
                gio.write_grid(comm_io, output, recvbuf, is_little) # Output parallelly with processes of residual domain after reduction
        else: # Number of domain in axis for reduction is one.
            gio.write_grid(comm_io, output, subgrid, is_little) # Output parallelly with processes of residual domain after reduction
