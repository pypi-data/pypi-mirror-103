import ustring         as s
from   ulog            import log

import unittest

import test_base       as tb
import tar             as tar


class test_tar(tb.test_base):

    def test_tar_01(self):
        self.eq(tar.rp("ms"), "D:\\jedi\\yoda\\m3o\\server\\src")
        self.eq(tar.rp("ms/a"), "D:\\jedi\\yoda\\m3o\\server\\src\\a")
        self.eq(tar.rp("ms\\a"), "D:\\jedi\\yoda\\m3o\\server\\src\\a")
        self.eq(tar.rp("ms\\a\\b\\c"), "D:\\jedi\\yoda\\m3o\\server\\src\\a\\b\\c")
        self.eq(tar.rp(".."), "C:\\Users\\gzhou\\Desktop")
        self.eq(tar.rp("../data"), "C:\\Users\\gzhou\\Desktop\\data")
        self.eq(tar.rp("../data/a/b/c"), "C:\\Users\\gzhou\\Desktop\\data\\a\\b\\c")
        self.eq(tar.rp("..\\data"), "C:\\Users\\gzhou\\Desktop\\data")
        self.eq(tar.rp("."), "C:\\Users\\gzhou\\Desktop\\rename")
        self.eq(tar.rp("./data"), "C:\\Users\\gzhou\\Desktop\\rename\\data")
        self.eq(tar.rp("./data/a/b/c"), "C:\\Users\\gzhou\\Desktop\\rename\\data\\a\\b\\c")
        self.eq(tar.rp(".\\data"), "C:\\Users\\gzhou\\Desktop\\rename\\data")

