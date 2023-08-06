import ustring         as s
from   ulog            import log

import unittest

import test_base       as tb
import tar             as tar
import cons            as cons
import fileio          as fileio
import filedelete      as filedelete


class test_fileio(tb.test_base):

    def test_mkdir_01(self):
        root = cons.tmp + "\\a"
        f = cons.tmp + "\\a"
        fileio.mkdir(f)
        self.eq(fileio.exists(f), True)
        filedelete.do_del_file(root)
        f = cons.tmp + "\\a\\b\\c"
        fileio.mkdir(f)
        self.eq(fileio.exists(f), True)
        filedelete.do_del_file(root)

    def test_get_vtba_01(self):
        self.eq(fileio.get_vtba(tar.rp("jmvv")), tar.rp("home"))
        self.eq(fileio.get_vtba(tar.rp("rn")), None)

