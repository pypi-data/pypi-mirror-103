import unittest
from datetime import datetime
from hkit.dtutil import dtutil

class dtutilTest(unittest.TestCase):
    def setUp(self):
        self.today = datetime.now()
        pass

    def tearDown(self):
        pass

    def test_getXdayBefore(self):
        dtutil.getXdayBefore(1)
        dtutil.getXdayBefore(1, self.today)

    def test_getMonday(self):
        dtutil.getMonday()
        dtutil.getMonday(self.today)

    def test_getNextMonday(self)->str:
        dtutil.getNextMonday()
        dtutil.getNextMonday(self.today)

    def test_getSunday(self)->str:
        dtutil.getSunday()
        dtutil.getSunday(self.today)

    def test_getStartOfMonth(self)->str:
        dtutil.getStartOfMonth()
        dtutil.getStartOfMonth(self.today)

    def test_getStartOfNextMonth(self)->str:
        dtutil.getStartOfNextMonth()
        dtutil.getStartOfNextMonth(self.today)

    def test_getEndOfMonth(self)->str:
        dtutil.getEndOfMonth()
        dtutil.getEndOfMonth(self.today)