from   ulog            import log

import unittest

import test_base       as tb
import cons            as cons
import fileio          as fileio
import git             as git
import svn             as svn
import ustring         as s


class test_common(tb.test_base):

    def test_common_01(self):
        i = 0
        i += 1
        self.eq(i, 1)

    def test_common_02(self):
        pass

    def test_common_03(self):
        pass

    def test_git_01(self):
        self.eq(git.is_git_dir("D:\\huazhi\\projects\\git\\bt\\lenovo"), True)
        self.eq(git.is_git_dir("D:\\huazhi\\projects\\git\\bt"), True)
        self.eq(git.is_git_dir("D:\\huazhi\\projects\\git"), False)
        self.eq(git.is_git_dir("D:\\jedi\\yoda"), False)
        self.eq(svn.is_svn_dir("D:\\huazhi\\projects\\svn\\bt\\lenovo"), False)
        self.eq(svn.is_svn_dir("D:\\huazhi\\projects\\svn\\bt"), False)
        self.eq(svn.is_svn_dir("D:\\huazhi\\projects\\svn"), False)
        self.eq(svn.is_svn_dir("D:\\jedi\\yoda"), True)

