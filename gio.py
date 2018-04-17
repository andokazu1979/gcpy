#! /usr/bin/env python

import sys
import logging
import numpy as np
from mpi4py import MPI

logger = logging.getLogger(__name__)

def read_grid(comm, fname, subgrid):
    """Read grid data"""

    amode = MPI.MODE_RDONLY
    fh = MPI.File.Open(comm, fname, amode)
    filetype = get_filetype(comm, subgrid)
    fh.Set_view(filetype=filetype)
    fh.Read_at_all(0, subgrid)
    
    fh.Close()
    
    subgrid_ = subgrid.byteswap()
    for i, item in enumerate(subgrid_):
        subgrid[i] = item
    
    logger.debug("input:\n{0}\n".format(subgrid))

def write_grid(comm, fname, subgrid):
    """Write grid data"""

    logger.debug("result:\n{0}\n".format(subgrid))
    
    subgrid = subgrid.byteswap()
    
    amode = MPI.MODE_WRONLY|MPI.MODE_CREATE
    fh = MPI.File.Open(comm, fname, amode)
    filetype = get_filetype(comm, subgrid)
    fh.Set_view(filetype=filetype)
    fh.Write_at_all(0, subgrid)
    
    fh.Close()

def get_filetype(comm, subgrid):
    n = np.array(subgrid.shape)

    shape = comm.Get_topo()[0]
    p = np.array(shape)

    rank = comm.Get_rank()
 
    wholesizes = n * p[:n.size]
    coords = np.array(comm.Get_coords(rank))
    starts = (n * coords[:n.size])
    filetype = MPI.FLOAT.Create_subarray(wholesizes, subgrid.shape, starts, MPI.ORDER_C)
    filetype.Commit()

    return filetype
