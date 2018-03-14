#! /usr/bin/env python

import sys
import logging

from mpi4py import MPI

import gtimer

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

class Analyzer(object):

    def __init__(self):
        """Initialization for MPI"""

        gtimer.timer_sta(1, 'Initialization')

        logger.debug("MPI_COMM_WORLD: nproc {0}, rank {1}".format(nproc, rank))

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

    def do_analysis(self):
        self.pre_process()
        self.main_process()
        self.post_process()

    def pre_process(self):
        pass

    def main_process(self):

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

        self.show_timer_result()

    def post_process(self):
        pass

    def read_grid(self):
        pass

    def grid_calc(self):
        pass

    def write_grid(self):
        pass

    def show_timer_result(self):

        for item in gtimer.get_lst_elapse():
            logger.info("rank{0}: {1}".format(self.rank, item))

