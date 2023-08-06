import ustring         as s
from   ulog            import log

import unittest

import test_base       as tb


class test_ustring(tb.test_base):

    def test_cf_01(self):
        self.eq(s.cf("abcdefg", "ab"), "cdefg")
        self.eq(s.cf("abcdefg", "ab", "ac"), "cdefg")
        self.eq(s.cf("abcdefg", 2), "cdefg")
        self.eq(s.cf("abcdefg"), "bcdefg")

    def test_cl_01(self):
        self.eq(s.cl("abcdefg", "fg"), "abcde")
        self.eq(s.cl("abcdefg", "fg", "fh"), "abcde")
        self.eq(s.cl("abcdefg", 2), "abcde")
        self.eq(s.cl("abcdefg"), "abcdef")

    def test_lf_01(self):
        self.eq(s.lf("abcdefg", " "), "abcdefg")
        self.eq(s.lf("abc defg", " "), "abc")
        self.eq(s.lf("abc de fg", " "), "abc")
        self.eq(s.clf("abcdefg", " "), "abcdefg")
        self.eq(s.clf("abc defg", " "), "defg")
        self.eq(s.clf("abc de fg", " "), "de fg")

    def test_split_01(self):
        astr = "a\nb"
        l = astr.split("\n")
        self.eq(l[0], "a")
        self.eq(l[1], "b")
        self.eq(s.sp("a b c", " "), ["a", "b", "c"])
        self.eq(s.sp("a  b    c", " ", no_el=True), ["a", "b", "c"])

    def test_string_array_01(self):
        l = ["a", "b", "c"]
        l[1] = l[1] + " " + l[2]
        l.pop()
        self.eq(l, ["a", "b c"])

    def test_get_parts_01(self):
        self.eq(s.get_parts("a b c"), ["a", "b", "c"])
        self.eq(s.get_parts("a b c "), ["a", "b", "c "])
        self.eq(s.get_parts("a b c  "), ["a", "b", "c  "])
        self.eq(s.get_parts("a;b;c"), ["a", "b", "c"])
        self.eq(s.get_parts("a;;b;;c"), ["a", "b", "c"])
        self.eq(s.get_parts("a(;;)b(;;)c"), ["a", "b", "c"])
        self.eq(s.get_parts("a(;;)b;c(;;)c d"), ["a", "b;c", "c d"])
        self.eq(s.get_parts("a b c", "{0}"), ["a b c"])
        self.eq(s.get_parts("a b c", "{0:4}{1}"), ["a", "b c"])
        self.eq(s.get_parts("a b c", "{0:4}{1:10}"), ["a", "b c"])
        self.eq(s.get_parts("a b c", "{0:4}{1:10}{2}"), ["a", "b", "c"])
        self.eq(s.get_parts("a b c ", "{0:4}{1:10}{2}"), ["a", "b", "c "])

    def test_conn_01(self):
        self.eq(s.conn(["a", "b"], " "), "a b")
        self.eq(s.conn(["a", "b"], ", "), "a, b")
        self.eq(s.conn(["a"], ", "), "a")
        self.eq(s.conn("a\nb", " "), "a b")
        self.eq(s.conns(["a", "b"], " "), "a b")
        self.eq(s.conns(["a", "b"], ", "), "a, b")
        self.eq(s.conns(["a"], ", "), "a")
        self.eq(s.conns("a\nb", " "), "a b")
        self.eq(s.conns("", "\n"), "")

    def test_match_01(self):
        self.eq(s.match("1 : abc", "\\d+ : .*"), True)
        self.eq(s.match("at com.vitria.servlet.autostart.AutoStartServlet$1.run(AutoStartServlet.java:120)", ".*\\(.*.java:\\d+\\)"), True)
        self.eq(s.match(".run(AutoStartServlet.java:120)", ".*\\(.*\\.java:\\d+\\)"), True)
        self.eq(s.match(".run(AutoStartServlet.java:)", ".*\\(.*\\.java:\\d+\\)"), False)
        self.eq(s.match(".run(AutoStartServlet.java:", ".*\\(.*\\.java:\\d+\\)"), False)
        self.eq(s.match(".run(AutoStartServlet.java:120", ".*\\(.*\\.java:\\d+\\)"), False)
        self.eq(s.match(".run(AutoStartServletjava:120)", ".*\\(.*\\.java:\\d+\\)"), False)
        self.eq(s.match("1 -", "(\\d+ )+-"), True)
        self.eq(s.match("1 2 -", "(\\d+ )+-"), True)
        self.eq(s.match("1 2 10 11 -", "(\\d+ )+-"), True)
        self.eq(s.match("1-", "\\d+-"), True)
        self.eq(s.match("123-", "\\d+-"), True)
        
        
    def test_has_p_01(self):
        self.eq(s.has_p("xxx a b c", "a"), True)
        self.eq(s.has_p("xxx a b c", "d"), False)
        self.eq(s.has_p("a b c", "a"), True)

    def test_rm_p_01(self):
        self.eq(s.rm_p("xxx a b c", "a"), "xxx b c")
        self.eq(s.rm_p("xxx a b c", "c"), "xxx a b")
        self.eq(s.rm_p("xxx a b c", "d"), "xxx a b c")

    def test_case_01(self):
        self.eq(s.to_upper_case("a"), "A")
        self.eq(s.to_lower_case("a"), "a")
        self.eq(s.to_lower_case_real("A"), "a")
        self.eq(s.to_camel_case("abc"), "Abc")
        self.eq(s.to_camel_words("abc def"), "Abc Def")

    def test_ifelse_01(self):
        self.eq(["a", "b"][False], "a")
        self.eq(["a", "b"][True], "b")

    def test_sort_01(self):
        self.eq(s.sort(s.conn(["3", "2", "1"])), s.conn(["1", "2", "3"]))
        self.eq(s.sort(s.conn(["3", "2", "1"]), reverse=True), s.conn(["3", "2", "1"]))
        self.eq(s.sort(["3", "2", "1"]), ["1", "2", "3"])
        self.eq(s.sort(["3", "2", "1"], reverse=True), ["3", "2", "1"])

        self.eq(s.sort(["a c b", "b b a", "c a c"]), ["a c b", "b b a", "c a c"])
        self.eq(s.sort(["a c b", "b b a", "c a c"], 1), ["a c b", "b b a", "c a c"])
        self.eq(s.sort(["a c b", "b b a", "c a c"], 2), ["c a c", "b b a", "a c b"])
        self.eq(s.sort(["a c b", "b b a", "c a c"], 3), ["b b a", "a c b", "c a c"])
        self.eq(s.sort(["a  c   b", "b  b       a", "c  a  c"], 1), ["a  c   b", "b  b       a", "c  a  c"])
        self.eq(s.sort(["a    c      b", "b  b    a", "c a  c"], 2), ["c a  c", "b  b    a", "a    c      b"])
        self.eq(s.sort(["a  c  b", "b  b     a", "c a   c"], 3), ["b  b     a", "a  c  b", "c a   c"])

        self.eq(s.sortreverse(s.conn(["3", "2", "1"])), s.conn(["3", "2", "1"]))
        self.eq(s.sortreverse(s.conn(["3", "2", "1"])), s.conn(["3", "2", "1"]))
        self.eq(s.sortreverse(["3", "2", "1"]), ["3", "2", "1"])
        self.eq(s.sortreverse(["3", "2", "1"]), ["3", "2", "1"])

    def test_cv__01(self):

        def func_01(x):
            return x

        self.eq(s.cv_("a1", func_01), "a1")
        self.eq(s.cv_(["a1"], func_01), ["a1"])
        self.eq(s.cv_(["a1", "b1"], func_01), ["a1", "b1"])

        def func_02(x):
            return s.al(x, "x")

        self.eq(s.cv_("a1", func_02), "a1x")
        self.eq(s.cv_(["a1"], func_02), ["a1x"])
        self.eq(s.cv_(["a1", "b1"], func_02), ["a1x", "b1x"])

        self.eq(s.cv_("a1", s.al, "x"), "a1x")
        self.eq(s.cv_(["a1"], s.al, "x"), ["a1x"])
        self.eq(s.cv_(["a1", "b1"], s.al, "x"), ["a1x", "b1x"])

    def test_append_01(self):
        a = ["1", "2"]
        r = []
        r += a
        r += ['34']
        self.eq(r, ["1", "2", "34"])

    def test_to_isf_keys_01(self):
        self.eq(s.to_isf_keys("a"), ["a"])
        self.eq(s.to_isf_keys("a "), ["a "])
        self.eq(s.to_isf_keys("a b  "), ["a", "b  "])
        self.eq(s.to_isf_keys("a b"), ["a", "b"])
        self.eq(s.to_isf_keys("a b c"), ["a", "b", "c"])
        self.eq(s.to_isf_keys("a st(b) c"), ["a", "st(b)", "c"])
        self.eq(s.to_isf_keys("a st(b ) c"), ["a", "st(b )", "c"])
        self.eq(s.to_isf_keys("a st( b ) c end( d )"), ["a", "st( b )", "c", "end( d )"])
        self.eq(s.to_isf_keys("st(a)"), ["st(a)"])
        self.eq(s.to_isf_keys("st(a )"), ["st(a )"])
        self.eq(s.to_isf_keys("st( a)"), ["st( a)"])
        self.eq(s.to_isf_keys("st( a) ( c ) end(b )"), ["st( a)", "( c )", "end(b )"])
        self.eq(s.to_isf_keys("a or(b)"), ["a", "or(b)"])

    def test_isf_01(self):
        self.eq(s.isf("a", "a"), True)
        self.eq(s.isf("a", "(a)"), True)
        self.eq(s.isf("abc", "st(a)"), True)
        self.eq(s.isf("abc", "end(c)"), True)
        self.eq(s.isf("abc", "not(a)"), False)
        self.eq(s.isf("abc", "a or(d)"), True)
        self.eq(s.isf("def", "a or(d)"), True)
        self.eq(s.isf("def", "a or(st(d))"), True)
        self.eq(s.isf("a", "a or(st(d) or(end(f)))"), True)
        self.eq(s.isf("def", "a or(st(d) or(end(f)))"), True)
        self.eq(s.isf("d e f", "a or(st(d e) or(end(e f)))"), True)
        self.eq(s.isf("d e f", "a or(not(st(d e)) or(end(e f)))"), True)
        self.eq(s.isf("d e f", "a or(not(st(d e)) end(e f))"), False)
        self.eq(s.isf("d e f", "d or(not(d))"), True)
        self.eq(s.isf("d e f", "d not(d)"), False)
        self.eq(s.isf("/a/b/c", "fn((c))"), True)
        self.eq(s.isf("D:\\a\\b\\c", "fn((c))"), True)
        self.eq(s.isf("/a/b/cde", "fn(st(c))"), True)
        self.eq(s.isf("/a/b/cde", "fn(end(e))"), True)
        
    def test_find_wrapped_01(self):
        self.eq(s.find_wrapped("a(b)c", "()"), "b")
        self.eq(s.find_wrapped("a(b c)c", "()"), "b c")
        self.eq(s.find_wrapped("a(b (c) d)c", "()"), "b (c) d")
        self.eq(s.find_wrapped("not(b st(c) d)c", "not()"), "b st(c) d")
        self.eq(s.find_wrapped("not(b st(c) d)c", "not123()"), None)

    def test_filter__01(self):
        self.eq(s.filter_(["a1", "b1", "c1"], "a", s.st), ["a1"])
        self.eq(s.filter_(["a1", "b1", "c1"], "b", s.st), ["b1"])
        self.eq(s.filter_(["a1", "b1", "c1"], ["a", "b"], s.st), ["a1", "b1"])
        self.eq(s.filter_(["a1", "b1", "c1"], ["a", "b", "d"], s.st), ["a1", "b1"])
        self.eq(s.filter_(["a1", "b1", "c1"], "a1", s.eq), ["a1"])
        self.eq(s.filter_(["a1", "b1", "c1"], "b1", s.eq), ["b1"])
        self.eq(s.filter_(["a1", "b1", "c1"], ["a1", "b1"], s.eq), ["a1", "b1"])
        self.eq(s.filter_(["a1", "b1", "c1"], ["a1", "b1", "d1"], s.eq), ["a1", "b1"])

    def test__filter__01(self):
        self.eq(s._filter_(["a1", "b1", "c1"], s.st, "a"), ["a1"])
        self.eq(s._filter_(["a1", "b1", "c1"], s.st, "b"), ["b1"])
        self.eq(s._filter_(["a1", "b1", "c1"], s.st, "a", "b"), ["a1", "b1"])
        self.eq(s._filter_(["a1", "b1", "c1"], s.st, "a", "b", "d"), ["a1", "b1"])
        self.eq(s._filter_(["a1", "b1", "c1"], s.eq, "a1"), ["a1"])
        self.eq(s._filter_(["a1", "b1", "c1"], s.eq, "b1"), ["b1"])
        self.eq(s._filter_(["a1", "b1", "c1"], s.eq, "a1", "b1"), ["a1", "b1"])
        self.eq(s._filter_(["a1", "b1", "c1"], s.eq, "a1", "b1", "d1"), ["a1", "b1"])
        self.eq(s._filter_(["a1", "b1", "c1"], lambda x: s.st(x, "a", "b")), ["a1", "b1"])
        self.eq(s._filter_("a1\nb1\nc1", lambda x: s.st(x, "a", "b")), "a1\nb1")

    def test_noel_01(self):
        self.eq(s.noel(["a1", "", "b1", " ", "  ", "", "c1"]), ["a1", "b1", "c1"])
        self.eq(s.noel("a1\n\nb1\n\n \n  \n\nc1\n\n"), "a1\nb1\nc1")

    def test_no_multi_el_01(self):
        self.eq(s.no_multi_el(["a1", "", "b1", " ", "  ", "", "c1"]), ["a1", "", "b1", "", "c1"])
        self.eq(s.no_multi_el("a1\n\nb1\n\n \n  \n\nc1\n\n\n\n"), "a1\n\nb1\n\nc1\n\n")

    def test_performance_01(self):
        # self.test_p(lambda : s.isf("d e f", "a or(not(st(d e)) or(end(e f)))"), n=100000)
        pass

