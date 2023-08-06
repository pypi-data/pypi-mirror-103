import ustring         as s
from   ulog            import log

import unittest

import test_base       as tb
import ulist           as ulist


class test_ulist(tb.test_base):

    def test_list_01(self):
        l = [1, 2, 3]
        self.eq(ulist.add(l, 4), [1, 2, 3, 4])
        self.eq(ulist.add(l, 1), [1, 2, 3])
        self.eq(ulist.add(l, [1, 4, 5]), [1, 2, 3, 4, 5])
        self.eq(ulist.rm(l, 4), [1, 2, 3])
        self.eq(ulist.rm(l, 1), [2, 3])
        l = [1, 2, 3, 1]
        self.eq(ulist.rm(l, 1), [2, 3])
        self.eq(ulist.rm(l, [1, 2]), [3])

