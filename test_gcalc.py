#! /usr/bin/env python

import pytest
import numpy as np

from gcpy import gcalc

class TestGcalc(object):

    @pytest.fixture()
    def na1(cls):
        na = np.arange(0,16).astype(np.float32).reshape([2,2,2,2])
        return na

    @pytest.fixture()
    def na2(cls):
        na = np.zeros(16).astype(np.float32).reshape([2,2,2,2])
        return na

    @pytest.fixture()
    def na3(cls):
        na = np.zeros(32).astype(np.float32).reshape([4,2,2,2])
        return na

    def test_subst_p(self, na1, na2, na3):
        gcalc.subst_p(na2, na1)
        assert  na2[0,0,0,0] == na1[0,0,0,0]
        assert  na2[1,1,1,1] == na1[1,1,1,1]

        gcalc.subst_p(na3[:2,:,:,:], na1)
        assert  na3[0,0,0,0] == na1[0,0,0,0]
        assert  na3[1,1,1,1] == na1[1,1,1,1]
        assert  na3[2,0,0,0] == pytest.approx(0.0)
        assert  na3[3,1,1,1] == pytest.approx(0.0)

    def test_subst_c(self, na1, na2, na3):
        gcalc.subst_c(na2, na1)
        assert  na2[0,0,0,0] == na1[0,0,0,0]
        assert  na2[-1,-1,-1,-1] == na1[-1,-1,-1,-1]

        gcalc.subst_c(na3[1:3,:,:,:], na1)
        assert  na3[0,0,0,0] == pytest.approx(0.0)
        assert  na3[1,0,0,0] == na1[0,0,0,0]
        assert  na3[2,1,1,1] == na1[1,1,1,1]
        assert  na3[3,0,0,0] == pytest.approx(0.0)
