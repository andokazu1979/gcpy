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

class GCDriver(object):

    def __init__(self):
        """Initialization for MPI"""

        comm = MPI.COMM_WORLD
        nproc = comm.Get_size()
        rank = comm.Get_rank()
        
        logging.basicConfig(filename='log.{0:06d}'.format(rank), filemode='w', level=level_)
        self.logger = logging.getLogger(__name__)
        
        gtimer.timer_sta(1, 'Initialization')
        
        self.logger.debug("MPI_COMM_WORLD: nproc {0}, rank {1}".format(nproc, rank))
        
        self.nx = int(sys.argv[1])
        self.ny = int(sys.argv[2])
        self.nz = int(sys.argv[3])
        self.nt = int(sys.argv[4])
        
        self.px = int(sys.argv[5])
        self.py = int(sys.argv[6])
        self.pz = int(sys.argv[7])
        self.pt = int(sys.argv[8])
        
        self.comm = comm.Create_cart((self.pt, self.pz, self.py, self.px), reorder=True)
        self.nproc = self.comm.Get_size()
        self.rank = self.comm.Get_rank()
        
        gtimer.timer_end(1)

    def process(self):
        """Do all processes"""

        gtimer.timer_sta(0, 'Total')

        gtimer.timer_sta(2, 'Input')
        self.read_grid()
        gtimer.timer_end(2)

        gtimer.timer_sta(3, 'Grid calculation')
        self.grid_calc()
        gtimer.timer_end(3)

        gtimer.timer_sta(4, 'Output')
        self.write_grid()
        gtimer.timer_end(4)

        gtimer.timer_end(0)

        for item in gtimer.get_lst_elapse():
            self.logger.info("rank{0}: {1}".format(self.rank, item))

    def read_grid(self):
        """Read grid data"""
        
        amode = MPI.MODE_RDONLY
        fh = MPI.File.Open(self.comm, sys.argv[9], amode)
        
        sizes = (self.nt, self.nz, self.ny, self.nx)
        subsizes = (int(self.nt/self.pt), int(self.nz/self.pz), int(self.ny/self.py), int(self.nx/self.px))
        subgrid = np.zeros(subsizes, dtype='f4')
        coords = self.comm.Get_coords(self.rank)
        starts = (subsizes[0] * coords[0], subsizes[1] * coords[1], subsizes[2] * coords[2], subsizes[3] * coords[3])
        self.filetype = MPI.FLOAT.Create_subarray(sizes, subsizes, starts, MPI.ORDER_C)
        self.filetype.Commit()
        fh.Set_view(filetype=self.filetype)
        fh.Read_at_all(0, subgrid)
        
        fh.Close()
        
        self.subgrid = subgrid.byteswap()
        
        self.logger.debug("rank {0} input:\n{1}\n".format(self.rank, self.subgrid))

    def grid_calc(self):
        """Grid calculation"""

        pass
                
    def write_grid(self):
        """Write grid data"""
        
        self.logger.debug("rank {0} result:\n{1}\n".format(self.rank, self.subgrid))
        
        subgrid = self.subgrid.byteswap()
        
        amode = MPI.MODE_WRONLY|MPI.MODE_CREATE
        fh = MPI.File.Open(self.comm, sys.argv[10], amode)
        
        fh.Set_view(filetype=self.filetype)
        fh.Write_at_all(0, subgrid)
        
        fh.Close()

