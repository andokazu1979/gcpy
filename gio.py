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
    
    subgrid.byteswap(inplace=True)
    
    logger.debug("input:\n{0}\n".format(subgrid))

def write_grid(comm, fname, subgrid):
    """Write grid data"""

    logger.debug("result:\n{0}\n".format(subgrid))
    
    subgrid.byteswap(inplace=True)
    
    amode = MPI.MODE_WRONLY|MPI.MODE_CREATE
    fh = MPI.File.Open(comm, fname, amode)
    filetype = get_filetype(comm, subgrid)
    fh.Set_view(filetype=filetype)
    fh.Write_at_all(0, subgrid)
    
    fh.Close()

def get_filetype(comm, subgrid):
    nx = subgrid.shape[3]
    ny = subgrid.shape[2] 
    nz = subgrid.shape[1] 
    nt = subgrid.shape[0] 

    shape = comm.Get_topo()[0]
    px = shape[3]
    py = shape[2]
    pz = shape[1]
    pt = shape[0]

    rank = comm.Get_rank()
 
    subsizes = (int(nt/pt), int(nz/pz), int(ny/py), int(nx/px))
    coords = comm.Get_coords(rank)
    starts = (subsizes[0] * coords[0], subsizes[1] * coords[1], subsizes[2] * coords[2], subsizes[3] * coords[3])
    filetype = MPI.FLOAT.Create_subarray(subgrid.shape, subsizes, starts, MPI.ORDER_C)
    filetype.Commit()

    return filetype