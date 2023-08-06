import ustring         as s
from   ulog            import log

import unittest

import test_base       as tb
import ustring_ops     as ops


class test_ustring_ops(tb.test_base):

    def test_ops_01(self):
        self.eq(ops.do_ops("a=b", "lf ="), "a")
        self.eq(ops.do_ops("a=b", "clf ="), "b")
        self.eq(ops.do_ops("a=b", "cf 1"), "=b")
        self.eq(ops.do_ops("a=b", "cf 2"), "b")
        self.eq(ops.do_ops("a=b", "cf a"), "=b")
        self.eq(ops.do_ops("a=b ", "trim"), "a=b")
        self.eq(ops.do_ops(" a=b ", "wrap"), "\" a=b \"")
        self.eq(ops.do_ops(" a=b ", "wrap ()"), "( a=b )")
        self.eq(ops.do_ops(" a=b ", "wrap123"), " a=b ")
        self.eq(ops.do_ops(" a=b ", "trim"), "a=b")
        self.eq(ops.do_ops(" a=b ", "trimleft"), "a=b ")
        self.eq(ops.do_ops(" a=b ", "trimright"), " a=b")
        self.eq(ops.do_ops(" a=b ", "rm ="), " ab ")
        self.eq(ops.do_ops(" a=b ", "c a b"), "=")
        self.eq(ops.do_ops("a\nb\nc", "ct b"), "b")
        self.eq(ops.do_ops("a\n\nb\n  \nc", "noel"), "a\nb\nc")
        self.eq(ops.do_ops("a\nb\na\nc\nb\nc\na", "rmdup"), "a\nb\nc")
        self.eq(ops.do_ops("a\nb\nc", "tol"), "abc")
        self.eq(ops.do_ops(["a=a1", "b=c1", "c=c1"], "lf ="), ["a", "b", "c"])

    '''
    ops = ["af", "al", "cf", "cl", "lf", "lfw", "clf", "clfw", "rt", "rtw", "crt", "crtw",
           "c", "cv", "cvic", "trim", "trimleft", "trimright", "nl", "api",
           "ct", "nct", "st", "nst", "end", "nend", "ctic", "nctic", "stic", "endic",
           "dt", "len", "isf", "count", "countn", "gndoc", "shrinkel", "tol"]
    '''

    # ops = ["af", "al", "cf", "cl", "lf", "lfw", "clf", "clfw", "rt", "rtw", "crt", "crtw"]
    def test_ops_02(self):
        self.eq(ops.do_ops("a=b", "af x"), "xa=b")
        self.eq(ops.do_ops("a=b", "al x"), "a=bx")
        self.eq(ops.do_ops("xa=b", "cf x"), "a=b")
        self.eq(ops.do_ops("xa=b", "cf 1"), "a=b")
        self.eq(ops.do_ops("a=bx", "cl x"), "a=b")
        self.eq(ops.do_ops("a=bx", "cl 1"), "a=b")
        self.eq(ops.do_ops("a=b", "lf ="), "a")
        self.eq(ops.do_ops("a=b", "lfw ="), "a=")
        self.eq(ops.do_ops("a=b", "clf ="), "b")
        self.eq(ops.do_ops("a=b", "clfw ="), "=b")
        self.eq(ops.do_ops("a=b", "rt ="), "b")
        self.eq(ops.do_ops("a=b", "rtw ="), "=b")
        self.eq(ops.do_ops("a=b", "crt ="), "a")
        self.eq(ops.do_ops("a=b", "crtw ="), "a=")

    def test_ops_02_ml(self):
        self.eq(ops.do_ops("a=b\na=b", "af x"), "xa=b\nxa=b")
        self.eq(ops.do_ops("a=b\na=b", "al x"), "a=bx\na=bx")
        self.eq(ops.do_ops("xa=b\nxa=b", "cf x"), "a=b\na=b")
        self.eq(ops.do_ops("xa=b\nxa=b", "cf 1"), "a=b\na=b")
        self.eq(ops.do_ops("a=bx\na=bx", "cl x"), "a=b\na=b")
        self.eq(ops.do_ops("a=bx\na=bx", "cl 1"), "a=b\na=b")
        self.eq(ops.do_ops("a=b\na=b", "lf ="), "a\na")
        self.eq(ops.do_ops("a=b\na=b", "lfw ="), "a=\na=")
        self.eq(ops.do_ops("a=b\na=b", "clf ="), "b\nb")
        self.eq(ops.do_ops("a=b\na=b", "clfw ="), "=b\n=b")
        self.eq(ops.do_ops("a=b\na=b", "rt ="), "b\nb")
        self.eq(ops.do_ops("a=b\na=b", "rtw ="), "=b\n=b")
        self.eq(ops.do_ops("a=b\na=b", "crt ="), "a\na")
        self.eq(ops.do_ops("a=b\na=b", "crtw ="), "a=\na=")

    # ops = ["c", "cv", "cvic", "trim", "trimleft", "trimright", "wrap", "nl", "api"]
    def test_ops_03(self):
        self.eq(ops.do_ops("a=b", "c a b"), "=")
        self.eq(ops.do_ops("a=b", "cv a b"), "b=b")
        self.eq(ops.do_ops("abc Abc ABC", "cvic abc def"), "def Def DEF")
        self.eq(ops.do_ops(" a=b ", "trim"), "a=b")
        self.eq(ops.do_ops(" a=b ", "trimleft"), "a=b ")
        self.eq(ops.do_ops(" a=b ", "trimright"), " a=b")
        self.eq(ops.do_ops(" a=b ", "wrap"), "\" a=b \"")
        self.eq(ops.do_ops(" a=b ", "wrap '"), "' a=b '")
        self.eq(ops.do_ops(" a=b ", "wrap ()"), "( a=b )")
        self.eq(ops.do_ops(" a=b ", "wrap and{}"), "and{ a=b }")
        self.eq(ops.do_ops("\" a=b \"", "unwrap"), " a=b ")
        self.eq(ops.do_ops("' a=b '", "unwrap '"), " a=b ")
        self.eq(ops.do_ops("( a=b )", "unwrap ()"), " a=b ")
        self.eq(ops.do_ops("and{ a=b }", "unwrap and{}"), " a=b ")
        self.eq(ops.do_ops("a=b", "nl  LINE,"), " a=b,")
        self.eq(ops.do_ops("a=b", "nl  LINE,  "), " a=b,  ")
        self.eq(ops.do_ops("a=b", "nl LINE;"), "a=b;")
        self.eq(ops.do_ops("a b", "nl {0:4}{1}"), "a   b")
        self.eq(ops.do_ops("a b c", "nl {0:4}{1}"), "a   b c")
        # TODO api

    def test_ops_03_ml(self):
        self.eq(ops.do_ops("a=b\na=b", "c a b"), "=\n=")
        self.eq(ops.do_ops("a=b\na=b", "cv a b"), "b=b\nb=b")
        self.eq(ops.do_ops("abc Abc ABC\nabc Abc ABC", "cvic abc def"), "def Def DEF\ndef Def DEF")
        self.eq(ops.do_ops(" a=b \n a=b ", "trim"), "a=b\na=b")
        self.eq(ops.do_ops(" a=b \n a=b ", "trimleft"), "a=b \na=b ")
        self.eq(ops.do_ops(" a=b \n a=b ", "trimright"), " a=b\n a=b")
        self.eq(ops.do_ops("a=b\na=b", "nl  LINE,"), " a=b,\n a=b,")
        self.eq(ops.do_ops("a=b\na=b", "nl  LINE,  "), " a=b,  \n a=b,  ")
        self.eq(ops.do_ops("a=b\na=b", "nl LINE;"), "a=b;\na=b;")
        self.eq(ops.do_ops("a b\na b", "nl {0:4}{1}"), "a   b\na   b")
        self.eq(ops.do_ops("a b c\na b c", "nl {0:4}{1}"), "a   b c\na   b c")
        # TODO api

    # ops = ["ct", "nct", "st", "nst", "end", "nend", "ctic", "nctic", "stic", "nstic", "endic", "nendic"]
    def test_ops_04(self):
        self.eq(ops.do_ops("a=a1\nb=b1", "ct a"), "a=a1")
        self.eq(ops.do_ops("a=a1\nb=b1", "nct a"), "b=b1")
        self.eq(ops.do_ops("a=a1\nb=b1", "st a"), "a=a1")
        self.eq(ops.do_ops("a=a1\nb=b1", "nst a"), "b=b1")
        self.eq(ops.do_ops("a=a1\nb=b1", "end a1"), "a=a1")
        self.eq(ops.do_ops("a=a1\nb=b1", "nend a1"), "b=b1")
        self.eq(ops.do_ops("a=a1\nb=b1", "ctic A"), "a=a1")
        self.eq(ops.do_ops("a=a1\nb=b1", "nctic A"), "b=b1")
        self.eq(ops.do_ops("a=a1\nb=b1", "stic A"), "a=a1")
        self.eq(ops.do_ops("a=a1\nb=b1", "nstic A"), "b=b1")
        self.eq(ops.do_ops("a=a1\nb=b1", "endic A1"), "a=a1")
        self.eq(ops.do_ops("a=a1\nb=b1", "nendic A1"), "b=b1")
        self.eq(ops.do_ops("a=a1\nb=b1", "match a=a\\d+"), "a=a1")
        self.eq(ops.do_ops("a=a1", "nct a"), "")

    # ops = ["dt", "len", "isf", "count", "countn", "gndoc", "shrinkel", "noel", "tol", "conns", "conn"]
    # TODO: "dt", "len", "isf", "count", "countn", "gndoc"
    def test_ops_05(self):
        self.eq(ops.do_ops("a\n\nb", "shrinkel"), "a\nb")
        self.eq(ops.do_ops("a\n  \nb", "shrinkel"), "a\nb")
        self.eq(ops.do_ops("a\n\nb", "noel"), "a\nb")
        self.eq(ops.do_ops("a\n  \nb", "noel"), "a\nb")
        self.eq(ops.do_ops("a\n\nb", "tol"), "ab")
        self.eq(ops.do_ops("a\n  \nb", "tol"), "a  b")
        self.eq(ops.do_ops("a\nb", "conn  "), "a b")
        self.eq(ops.do_ops("a\nb", "conn   "), "a  b")
        self.eq(ops.do_ops("a\nb", "conn , "), "a, b")
        self.eq(ops.do_ops("a\nb", "conn ;"), "a;b")
        self.eq(ops.do_ops("a\nb", "conns  "), "a b")
        self.eq(ops.do_ops("a\nb", "conns   "), "a  b")
        self.eq(ops.do_ops("a\nb", "conns , "), "a, b")
        self.eq(ops.do_ops("a\nb", "conns ;"), "a;b")
        self.eq(ops.do_ops("a", "use abcde"), "abcde")
        self.eq(ops.do_ops("a\nb", "use abcde"), "abcde")

