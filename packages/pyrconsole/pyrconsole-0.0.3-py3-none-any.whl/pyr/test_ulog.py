import ustring         as s
from   ulog            import log

import unittest

import test_base       as tb


class test_ulog(tb.test_base):

    def test_cf_01(self):
        l = ["a", "b"]
        log(l)

