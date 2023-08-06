import ustring         as s
from   ulog            import log

import cons            as cons
import ulog            as ulog


def translate(m):
    m00 = m
    m = wildfly_upgrade(m)
    m = do(m)
    m = bug(m)
    m = tongji(m)
    ulog.log_trans(m00, m)
    return m


def wildfly_upgrade(m):
    if (m in ["wu"]):
        do_wildfly_upgrade()
        m = cons.ignore_cmd
    return m


def do_wildfly_upgrade():
    import traceback

    class wildfly_upgrade_sub_console(sub_console):
        
        wildfly_upgrade_cmds = {
            "er"   : "hrun gsl fs ec",
            "d"    : "ci D:\\jedi\\yoda\\build\\lib\\driver\\mysql\\mysql-connector-java-5.1.38-bin.jar",
            "h"    : "ci LAPTOP-GZHOU",
            "qw"   : "ci Qilin@1234",
            "in"   : "g C:\\Users\\gzhou\\Desktop\\rename\\Project\\TMP\\input\\1209",
            "out"  : "g C:\\Users\\gzhou\\Desktop\\rename\\Project\\TMP\\output\\1209",
            "fbl1" : ".. gh1;g tmp;zj;g 1;g build.log",
            "fbl2" : ".. gh2;g tmp;zj;g 1;g build.log",
            "fbl3" : ".. gh3;g tmp;zj;g 1;g build.log",
            "fal1" : ".. gh1;g spark;g apps;zj;g 1;g log;g app.log",
            "fal2" : ".. gh2;g spark;g apps;zj;g 1;g log;g app.log",
            "fal3" : ".. gh3;g spark;g apps;zj;g 1;g log;g app.log",
        }
        
        def n(self):
            return "wildfly upgrade"
        
        def callback(self, m):
            m = self.translate(m)
            self.try_(self.main__, m)
        
        def translate(self, m):
            m00 = m
            if (self.wildfly_upgrade_cmds.__contains__(m)):
                m = self.wildfly_upgrade_cmds[m]
            ulog.log_trans(m00, m)
            return m
        
        def main__(self, m):
            try:
                ulog.increase_log_tab(4, all_=True)
                log()
                cons.r.do_run__(m)
            finally:
                ulog.decrease_log_tab(4, all_=True)
            return m
        
        def input_p(self):
            return True
        
    sub_console_ = wildfly_upgrade_sub_console()
    sub_console_.run()


def do(m):
    if (m in [" do"]):
        do_do()
        m = cons.ignore_cmd
    return m


def do_do():
    import traceback

    class do_sub_console(sub_console):
        
        do_id = None
        do_n = None
        
        do_cmds = {
            "ji" : "ji",
        }
        
        def n(self):
            return "do"
        
        def callback(self, m):
            m = self.translate(m)
            self.try_(self.main__, m)
        
        def translate(self, m):
            m00 = m
            
            m = self.v_(m)
            if (m == None):
                return m
            m = self.va_(m)
            if (m == None):
                return m
            m = self.select_(m)
            if (m == None):
                return m
            m = self.id_(m)
            if (m == None):
                return m
            m = self.n_(m)
            if (m == None):
                return m
            m = self.ci_(m)
            if (m == None):
                return m
            m = self.ji_(m)
            if (m == None):
                return m
            
            if (self.do_cmds.__contains__(m)):
                m = self.do_cmds[m]
            ulog.log_trans(m00, m)
            return m
        
        def v_(self, m):
            if (m == "v"):
                log()
                log(self.do_s())
                log()
                return None
            return m
        
        def va_(self, m):
            if (m == "va"):
                log()
                do_tasks = self.get_do_tasks()
                ulog.logl("do tasks", do_tasks)
                log()
                return None
            return m
        
        def select_(self, m):
            if (m in ["s", "sel", "select"]):
                log()
                do_tasks = self.get_do_tasks()
                import ulist
                selected = ulist.select("do tasks", do_tasks)
                if (s.st(selected, "DO-")):
                    self.do_id = s.cf(s.lf(selected, " "), "DO-")
                    self.do_n = s.clf(selected, " ")
                    import ci
                    ci.set_text(selected)
                    log(self.do_s())
                    log()
                return None
            return m
        
        def id_(self, m):
            if (s.match(m, "\\d\\d\\d\\d")):
                self.do_id = m
                self.do_n = self.find_n(m)
                self.v_("v")
                return None
            return m
        
        def n_(self, m):
            if (s.st(m, "n ")):
                self.do_n = s.cf(m, "n ")
                self.v_("v")
                return None
            return m
        
        def ci_(self, m):
            if (m == "ci"):
                import ci
                text = self.do_s()
                ci.set_text(text)
                log()
                ci.logci(text)
                return None
            return m
        
        def ji_(self, m):
            if (m == "ji"):
                import ci
                text = self.do_s()
                m = ".. ci {0};;ji".format(text)
                return m
            return m
        
        def main__(self, m):
            try:
                ulog.increase_log_tab(4, all_=True)
                log()
                cons.r.do_run__(m)
            finally:
                ulog.decrease_log_tab(4, all_=True)
            return m
        
        def do_s(self):
            if (self.do_n):
                return "DO-{0} {1}".format(self.do_id, self.do_n)
            else:
                return "DO-{0}".format(self.do_id)
        
        def find_n(self, m):
            m = "DO-" + m
            import fileio
            lines = fileio.l(cons.chf)
            lines = s._filter_(lines, s.st, m + " ")
            lines = s._filter_(lines, lambda x: len(x) > 10)
            if (len(lines) > 0):
                return s.cf(lines[0], m + " ")
            return None
        
        def get_do_tasks(self):
            import fileio
            lines = fileio.l(cons.chf)
            lines = s._filter_(lines, s.st, "DO-")
            lines = s._filter_(lines, lambda x:len(x) > 10)
            return lines
        
    sub_console_ = do_sub_console()
    sub_console_.run()


def bug(m):
    if (m in [" bug"]):
        bug_bug()
        m = cons.ignore_cmd
    return m


def bug_bug():
    import traceback

    class bug_sub_console(sub_console):
        
        bug_id = None
        bug_n = None
        
        bug_cmds = {
            "ji": "ji",
        }
        
        def n(self):
            return "bug"
        
        def callback(self, m):
            m = self.translate(m)
            self.try_(self.main__, m)
        
        def translate(self, m):
            m00 = m
            
            m = self.v_(m)
            if (m == None):
                return m
            m = self.va_(m)
            if (m == None):
                return m
            m = self.select_(m)
            if (m == None):
                return m
            m = self.id_(m)
            if (m == None):
                return m
            m = self.n_(m)
            if (m == None):
                return m
            m = self.ci_(m)
            if (m == None):
                return m
            m = self.ji_(m)
            if (m == None):
                return m
            
            if (self.bug_cmds.__contains__(m)):
                m = self.bug_cmds[m]
            ulog.log_trans(m00, m)
            return m
        
        def v_(self, m):
            if (m == "v"):
                log()
                log(self.bug_s())
                log()
                return None
            return m
        
        def va_(self, m):
            if (m == "va"):
                log()
                bugs = self.get_bugs()
                ulog.logl("bug tasks", bugs)
                log()
                return None
            return m
        
        def select_(self, m):
            if (m in ["s", "sel", "select"]):
                log()
                bugs = self.get_bugs()
                import ulist
                selected = ulist.select("bugs", bugs)
                if (s.st(selected, "VITR00")):
                    self.bug_id = s.cf(s.lf(selected, " "), "VITR00")
                    self.bug_n = s.clf(selected, " ")
                    import ci
                    ci.set_text(selected)
                    log(self.bug_s())
                    log()
                return None
            return m
        
        def id_(self, m):
            if (s.match(m, "\\d\\d\\d\\d")):
                self.bug_id = m
                self.bug_n = self.find_n(m)
                self.v_("v")
                return None
            return m
        
        def n_(self, m):
            if (s.st(m, "n ")):
                self.bug_n = s.cf(m, "n ")
                self.v_("v")
                return None
            return m
        
        def ci_(self, m):
            if (m == "ci"):
                import ci
                text = self.bug_s()
                ci.set_text(text)
                log()
                ci.logci(text)
                return None
            return m
        
        def ji_(self, m):
            if (m == "ji"):
                import ci
                text = self.bug_s()
                m = ".. ci {0};;ji".format(text)
                return m
            return m
        
        def main__(self, m):
            try:
                ulog.increase_log_tab(4, all_=True)
                log()
                cons.r.bug_run__(m)
            finally:
                ulog.decrease_log_tab(4, all_=True)
            return m
        
        def bug_s(self):
            if (self.bug_n):
                return "VITR00{0} {1}".format(self.bug_id, self.bug_n)
            else:
                return "VITR00{0}".format(self.bug_id)
        
        def find_n(self, m):
            m = "VITR00" + m
            import fileio
            lines = fileio.l(cons.chf)
            lines = s._filter_(lines, s.st, m + " ")
            lines = s._filter_(lines, lambda x: len(x) > 20)
            if (len(lines) > 0):
                return s.cf(lines[0], m + " ")
            return None
        
        def get_bugs(self):
            import fileio
            lines = fileio.l(cons.chf)
            lines = s._filter_(lines, s.st, "VITR00")
            lines = s._filter_(lines, lambda x:len(x) > 20)
            lines = s._cv_(lines, s.trim)
            lines = s.rmdup(lines)
            return lines
        
    sub_console_ = bug_sub_console()
    sub_console_.run()


def tongji(m):
    if (m in [" tj", " tongji"]):
        tongji_tongji()
        m = cons.ignore_cmd
    return m


def tongji_tongji():
    import traceback

    class tongji_sub_console(sub_console):
        
        tongji_list = None
        tongji_list_all = None
        
        def __init__(self):
            f = s.alogs_("tongji.txt")
            import fileio
            self.tongji_list = fileio.l(f)
            self.tongji_list_all = fileio.l(f)
        
        def n(self):
            return "tongji"
        
        def callback(self, m):
            m = self.translate(m)
            self.try_(self.main__, m)
        
        def translate(self, m):
            m00 = m
            m = self.v_(m)
            if (m == None):
                return m
            m = self.va_(m)
            if (m == None):
                return m
            m = self.vp_(m)
            if (m == None):
                return m
            ulog.log_trans(m00, m)
            return m
        
        def v_(self, m):
            if (m == "v"):
                log()
                ulog.logl(self.n(), self.tongji_list)
                log()
                return None
            return m
        
        def va_(self, m):
            if (m == "va"):
                log()
                ulog.logl(self.n(), self.tongji_list_all)
                log()
                return None
            return m
        
        def vp_(self, m):
            if (m == "vp"):
                log()
                l = self.tongji_list
                import pinyin
                l = s._cv_(l, lambda x: pinyin.get(x, format="strip"))
                ulog.logl(self.n(), l)
                log()
                return None
            return m
        
        def main__(self, m):
            import pinyin
            tongji_list_with_py = s._cv_(self.tongji_list, lambda x: (x, pinyin.get(x, format="strip")))
            tongji_list_with_py = s._filter_(tongji_list_with_py, lambda x: s.isf(x[1], m))
            if (len(tongji_list_with_py) == 0):
                # try first char
                tongji_list_with_py = s._cv_(self.tongji_list, lambda x: (x, pinyin.get_initial(x, delimiter="")))
                tongji_list_with_py = s._filter_(tongji_list_with_py, lambda x: s.isf(x[1], m))
            l = s._cv_(tongji_list_with_py, lambda x: x[0])
            import ulist
            one = ulist.select("remove", l)
            if (not one == None and len(one) > 0):
                log()
                log("remove: " + one)
                self.tongji_list = ulist.rm(self.tongji_list, one)
                self.v_("v")
            return m
        
    sub_console_ = tongji_sub_console()
    sub_console_.run()


class sub_console:
    
    def n(self):
        return ""
    
    def callback(self, m):
        pass
    
    def clean(self, m):
        pass
    
    def clean_up(self):
        pass
    
    def print_help(self, m):
        help_ = self.help()
        if (help_):
            ulog.logh(self.n(), help_)
            m = None
        return m
    
    def help(self):
        return None
    
    def input_p(self):
        return False
    
    def try_(self, func, m):
        try:
            if(m):
                m = func(m)
            return m
        except:
            log()
            import traceback
            traceback.print_exc()
            log()
            return None
    
    def run(self):
        log(self.n() + ":")
        log()
        try:
            ulog.increase_log_tab(4, all_=True)
            while (True):
                m = input(["    >", "    " + cons.p + ">"][self.input_p()])
                if (m in ["", "q"]):
                    self.clean_up()
                    break
                elif (m == "c"):
                    m = self.clean(m)
                elif (m == "h"):
                    m = self.print_help(m)
                try:
                    if (m):
                        self.callback(m)
                except:
                    log()
                    import traceback
                    traceback.print_exc()
                    log()
                    continue
        finally:
            ulog.decrease_log_tab(4, all_=True)

