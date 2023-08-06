import unittest
from datefeatures import frac_sec, frac_min, frac_hour, frac_day, frac_month
from datetime import datetime
import numpy as np


yrs, mth, day, hr, mi, sc, ms = 1994, 3, 11, 11, 22, 57, 661170


class Test_MonthCirlce(unittest.TestCase):

    def test1(self):
        u = frac_sec(ms)
        s = np.sin(2.0 * np.pi * u)
        c = np.cos(2.0 * np.pi * u)
        self.assertAlmostEqual(u, 0.66117)
        self.assertAlmostEqual(s, -0.848244113421714)
        self.assertAlmostEqual(c, -0.529605441857814)

    def test2(self):
        u = frac_min(sc, ms)
        s = np.sin(2.0 * np.pi * u)
        c = np.cos(2.0 * np.pi * u)
        self.assertAlmostEqual(u, 0.9610195)
        self.assertAlmostEqual(s, -0.2424803670138401)
        self.assertAlmostEqual(c, 0.9701563129789104)

    def test3(self):
        u = frac_hour(mi, sc, ms)
        s = np.sin(2.0 * np.pi * u)
        c = np.cos(2.0 * np.pi * u)
        self.assertAlmostEqual(u, 0.38268365833333334)
        self.assertAlmostEqual(s, 0.6721585613887134)
        self.assertAlmostEqual(c, -0.7404072314286613)

    def test4(self):
        u = frac_day(hr, mi, sc, ms)
        s = np.sin(2.0 * np.pi * u)
        c = np.cos(2.0 * np.pi * u)
        self.assertAlmostEqual(u, 0.47427848576388887)
        self.assertAlmostEqual(s, 0.16091043607852898)
        self.assertAlmostEqual(c, -0.9869690124624063)

    def test5(self):
        u = frac_month(yrs, mth, day, hr, mi, sc, ms)
        s = np.sin(2.0 * np.pi * u)
        c = np.cos(2.0 * np.pi * u)
        self.assertAlmostEqual(u, 0.37013801566980287)
        self.assertAlmostEqual(s, 0.7283747291946037)
        self.assertAlmostEqual(c, -0.6851789940378264)
