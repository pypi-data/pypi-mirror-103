import ustring         as s
from   ulog            import log

import unittest

import filesystem      as filesystem


class test_base(unittest.TestCase):

    def setUp(self):
        filesystem.fs_init()

    def tearDown(self):
        pass

    def eq(self, *args):
        self.assertEqual(*args)

    def test_p(self, func="", n=1000000):
        if (not func == ""):
            start = s.nowts()
            for i in range(n):  # @UnusedVariable
                func()
            end = s.nowts()
            avg = (end - start) / n
            eps = 1000 / avg
            log("eps: " + s.format_f(eps))
