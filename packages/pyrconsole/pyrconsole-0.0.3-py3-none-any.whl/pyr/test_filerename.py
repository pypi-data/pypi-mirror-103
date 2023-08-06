import ustring         as s
from   ulog            import log

import unittest

import test_base       as tb
import filerename      as filerename


class test_filerename(tb.test_base):

    def test_is_ids_01(self):
        self.eq(filerename.is_rename_ids("1 : abc"), True)
        self.eq(filerename.is_rename_ids("1 2 3 : abc"), True)
        self.eq(filerename.is_rename_ids("123: abc"), True)

