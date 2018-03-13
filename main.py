#! /usr/bin/env python

from gcdriver import GCDriver
import gcalc

class GCDriverScaling(GCDriver):

    def grid_calc(self):
        """Grid calculation"""
        
        gcalc.scaling_p(self.rank, self.subgrid)
        # gcalc.scaling_c(self.rank, self.subgrid)
        # gcalc.scaling_f(self.rank, self.subgrid)

if __name__ == '__main__':
    driver = GCDriverScaling()
    driver.process()

