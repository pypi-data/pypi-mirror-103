import ustring         as s
from   ulog            import log

import ulog            as ulog
import tar             as tar
import env             as env


def select(n, lines, select=True, max_size=20):
    to = ""
    last_m = ""
    lines00 = lines
    max_size__ = max_size
    if (select and len(lines) > 1):
        if (max_size > 0):
            lines = sf(lines, max_size)
        ulog.logl(n + " list", lines)
        log()
        opt = select_option()
        while (True):
            m = input("    which one? ")
            
            if (m in ["", "q"]):
                break
            
            if (m == " "):
                m = last_m
            else:
                last_m = m
            
            if (m == "gl"):
                to = last(lines)
                break
            
            if (m == "va"):
                lines = lines00
                lines = opt.filter(lines)
                do_select_log(lines)
                continue
            
            if (m in ["more", "m"]):
                lines = lines00
                lines = opt.filter(lines)
                max_size = max_size + max_size__
                lines = sf(lines, max_size)
                do_select_log(lines)
                continue
            
            if (m == "vs"):
                log()
                env.do_vs_log("condition", opt.condition, tab=8)
                env.do_vs_log("last", last_m, tab=8)
                log()
                continue
            
            if (m == "ci"):
                text = s.conn(lines)
                s._r_("ci.set_text", text)
                log()
                s._r_("ci.logci", text)
                return ""
            
            if (s.is_number(m) and 1 <= int(m) <= len(lines)):
                to = lines[int(m) - 1]
                break
            
            if (s.st(m, "is ")):
                m = "fn(({0}))".format(s.cf(m, "is "))
            if (s.st(m, "st ")):
                m = "fn(st({0}))".format(s.cf(m, "st "))
            if (s.st(m, "end ")):
                m = "fn(end({0}))".format(s.cf(m, "end "))
            
            lines = do_select_filter(lines, m, opt)
    
            if (len(lines) == 0):
                break
            if (len(lines) == 1):
                to = lines[0]
                break
            
            do_select_log(lines)
            
        log()
    else:
        if (len(lines) == 0):
            to = None
        else:
            to = lines[0]
    return to


def do_select_log(lines):
    log()
    ulog.logl("", lines)
    log()


def do_select_filter(lines, m, opt):
    if (m == "d"):
        lines = s.filter_(lines, "", is_dir)
    elif (m == "f"):
        lines = s.filter_(lines, "", is_file)
    elif (m == "ml"):
        lines = s._filter_(lines, s.ct, "\n", "$$LINE_SEP$$")
    elif (m == "ol"):
        lines = s._filter_(lines, s.nct, "\n", "$$LINE_SEP$$")
    else:
        if (tar.is_dir_key(m)):
            m = tar.rp(m)
        lines = s._filter_(lines, s.isf, m)
        opt.add(m)
    return lines


class select_option:
    condition = ""
    
    def add(self, m):
        if (self.condition == ""):
            self.condition = m
        else:
            self.condition += (" " + m)
    
    def filter(self, lines):
        if (self.condition == ""):
            pass
        else:
            lines = s._filter_(lines, s.isf, self.condition)
        return lines


def is_dir(x, m):  # @UnusedVariable
    return s._r_("fileio.is_dir", x)


def is_file(x, m):  # @UnusedVariable
    return s._r_("fileio.is_file", x)


def sf(l, n):
    i = min(n, len(l))
    return l[0:i]


def sl(l, n):
    i = max(0, len(l) - n)
    return l[i:len(l)]


def first(l):
    return l[0]


def last(l):
    return l[len(l) - 1]


def ct(l, o):
    if (o in l):
        return True
    return False


def nct(l, o):
    return not ct(l, o)


def is_empty(l):
    return len == None or len(l) == 0


def not_empty(l):
    return not is_empty(l)


def filter_list(lines, p, func=s.isf):
    return list(filter(lambda x:func(x, p), lines))


def remove_lines(lines, ids):
    left_lines = []
    for i in range(len(lines)):
        if (not i in ids):
            left_lines.append(lines[i])
    return left_lines


def add(l, o):  # o is line, or lines
    if (isinstance(o, list)):
        r = []
        r += l
        for o_ in o:
            if (not l.__contains__(o_)):
                r += [o_]
        return r
    else:
        if (not l.__contains__(o)):
            r = []
            r += l
            r += [o]
            return r
    return l

    
def rm(l, o):  # o is line, or lines
    r = []
    r += l
    if (isinstance(o, list)):
        for o_ in o:
            while (r.__contains__(o_)):
                r.remove(o_) 
    else:
        while (r.__contains__(o)):
            r.remove(o)
    return r
