import unittest
from datefeatures import ShoppingHolidays
from datetime import datetime
import numpy as np
import numpy.testing as npt


class Test_ShoppingHolidays(unittest.TestCase):

    def test1(self):
        # Singles Day (China) 2017
        x = datetime(2017, 11, 11)
        hd = ShoppingHolidays(country='all')
        y = hd.fit_transform(x).toarray()[0, 0]
        self.assertEquals(y, True)

    def test2(self):
        # Singles Day (China) 2017
        x = [datetime(2017, 11, 11)]
        hd = ShoppingHolidays(country='all')
        y = hd.fit_transform(x).toarray()[0, 0]
        self.assertEquals(y, True)

    def test3(self):
        # Singles Day (China) 2017
        x = np.array([datetime(2017, 11, 11)])
        hd = ShoppingHolidays(country='all')
        y = hd.fit_transform(x).toarray()[0, 0]
        self.assertEquals(y, True)

    def test4(self):
        # Singles Day (China) 2017, 2018, and 1992 (=is not)
        x = np.array([
            datetime(2017, 11, 11),
            datetime(2018, 11, 11),
            datetime(1992, 11, 11)
        ])
        hd = ShoppingHolidays(country='all')
        y = hd.fit_transform(x).toarray()
        target = np.array([True, True, False]).reshape(-1, 1)
        npt.assert_array_equal(y, target)
