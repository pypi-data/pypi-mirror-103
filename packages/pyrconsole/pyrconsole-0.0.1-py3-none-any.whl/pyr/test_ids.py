import ustring         as s
from   ulog            import log

import unittest

import test_base       as tb
import ids             as ids


class test_ids(tb.test_base):

    def test_ids_01(self):
        self.eq(ids.is_ids("a", "a"), False)
        self.eq(ids.is_ids("1a", "a"), True)
        self.eq(ids.is_ids("123a", "a"), True)
        self.eq(ids.is_ids("1 a", "a"), True)
        self.eq(ids.is_ids("1 2 3 a", "a"), True)
        self.eq(ids.is_ids("1a b c", "a"), True)
        self.eq(ids.is_ids("123a b c", "a"), True)
        self.eq(ids.is_ids("1 a b c", "a"), True)
        self.eq(ids.is_ids("1 2 3 a b c", "a"), True)

    def test_ids_02(self):
        self.eq(ids.get_ids("1a", "a"), [0])
        self.eq(ids.get_ids("123a", "a"), [0, 1, 2])
        self.eq(ids.get_ids("1 a", "a"), [0])
        self.eq(ids.get_ids("1 2 3 a", "a"), [0, 1, 2])
        self.eq(ids.get_ids("1a b c", "a"), [0])
        self.eq(ids.get_ids("123a b c", "a"), [0, 1, 2])
        self.eq(ids.get_ids("1 a b c", "a"), [0])
        self.eq(ids.get_ids("1 2 3 a b c", "a"), [0, 1, 2])

    def test_ids_03(self):
        l = ["0", "1", "2", "3"]
        self.eq(ids.get_selected(l, "1a", "a"), ['0'])
        self.eq(ids.get_selected(l, "123a", "a"), ["0", "1", "2"])
        self.eq(ids.get_selected(l, "1 a", "a"), ['0'])
        self.eq(ids.get_selected(l, "1 2 3 a", "a"), ["0", "1", "2"])
        self.eq(ids.get_selected(l, "1a b c", "a"), ['0'])
        self.eq(ids.get_selected(l, "123a b c", "a"), ["0", "1", "2"])
        self.eq(ids.get_selected(l, "1 a b c", "a"), ['0'])
        self.eq(ids.get_selected(l, "1 2 3 a b c", "a"), ["0", "1", "2"])
        self.eq(ids.get_selected(l, "1 2 3 a b c", "a", "b"), ["0", "1", "2"])
        self.eq(ids.get_selected(l, "1 2 3 a b c", "b", "a"), ["0", "1", "2"])

