import ustring         as s
from   ulog            import log

import ci              as ci
import cons            as cons
import env             as env
import fileio          as fileio
import filelistfind    as filelistfind
import ulist           as ulist
import ulog            as ulog

b_trans_map = {
    "btd" : "bvToday",
}


def translate(m):
    m00 = m
    m = b_2_space(m)
    m = b_trans(m)
    m = add_ci(m)
    m = add_again(m)
    m = add_root(m)
    m = bn(m)  # new
    m = bvs(m)  # view specified
    m = bw(m)  # view specified
    m = tr_daiban(m)
    ulog.log_trans(m00, m)
    return m


def b_2_space(m):
    for k in ["b", "brm", "bv", "bn"]:
        if (s.st(m, k + "  ")):
            m = s.cf(m, k + "  ")
            if (opt().view_specified):
                m = k + s.cv(opt().view_specified, ".", "") + " " + m
            else:
                m = k + " " + m
    return m


def b_trans(m):
    if (b_trans_map.__contains__(m)):
        m = b_trans_map[m]
    return m


def add_ci(m):
    if (m == "b+"):
        m = "b " + ci.get_text()
    elif (s.st(m, "b") and s.end(m, "+")):
        m = s.cf(m, "b")
        m = s.cl(m, "+")
        if (m in opt().keys[3]):
            m = "b" + m + " " + ci.get_text()
        else:
            m = cons.ignore_cmd
    return m


def add_again(m):
    if (s.st(m, "b:")):
        if (not opt().last_add_key == None):
            m = s.cf(m, "b:")
            m = "b" + opt().last_add_key + " " + m
        elif (not opt().view_specified == None):
            m = s.cf(m, "b:")
            m = "b" + s.cv(opt().view_specified, ".", "") + " " + m
        else:
            m = cons.ignore_cmd
    return m


def add_root(m):
    if (s.st(m, "b ")):
        m = s.cf(m, "b ")
        m = "broot " + m
    return m


def bn(m):
    if (s.st(m, "bn")):
        k = s.trimleft(s.cf(m, "bn"))
        k = search_key(k, "add")
        if (k in opt().keys[3]):
            v = input("what is daiban task to add? ")
            if (v):
                return "b" + k + " " + v
        return cons.ignore_cmd
    return m


def bvs(m):
    if (s.st(m, "bvs ", "bv")):
        k = s.trimleft(s.cf(m, "bvs ", "bv"))
        if (k == "up"):
            k = opt().view_specified
            if (s.ct(k, ".")):
                k = s.crt(k, ".")
            else:
                k = None
        elif (k in opt().keys[3]):
            o = opt().o_map[k]
            k = o.full_key()
        else:
            k = search_key(k, "view specified")
            if (k):
                o = opt().o_map[k]
                k = o.full_key()
            else:
                return cons.ignore_cmd
        opt().view_specified = k
        vs()
        log()
        view()
        return cons.ignore_cmd
    return m


def bw(m):
    if (m == "bwb"):
        m = "bw1"
    if (m == "bwg"):
        m = "g " + s.alogs_("DaiBanWorkspace")
    if (s.st(m, "bwn ")):
        m = s.cf(m, "bwn ")
        dbw = s.alogs_("DaiBanWorkspace")
        f = dbw + s.sep(dbw) + m + ".log"
        fileio.w(f, ["No DaiBan."])
        m = "bw " + m
    if (m == "bw"):
        ulog.logl("DaiBan Files", s.cv_(bw_files_names(), bw_append_working))
    elif (s.st(m, "bw")):
        m = s.trim(s.cf(m, "bw"))
        if (s.is_number(m)):
            cons.daiban_workspace = bw_files()[int(m) - 1]
            do_reload()
            m = "ba"
        else:
            files = bw_files()
            files = s._filter_(files, lambda f: s.isf(fileio.get_file_simple_name(f), m))
            if (len(files) == 1):
                cons.daiban_workspace = files[0]
                do_reload()
                m = "ba"
            elif (len(files) > 1):
                cons.daiban_workspace = ulist.select("DaiBan File", files)
                do_reload()
                m = "ba"
            else:
                m = cons.ignore_cmd
    return m


def bw_files():
    ws = s.alogs_("DaiBanWorkspace")
    files = []
    daiban_f = s.alogs_("DaiBan.log")
    files_ws = filelistfind.list_dir_(ws)
    files += [daiban_f]
    files += files_ws
    return files


def bw_files_names():
    return s.cv_(bw_files(), fileio.get_file_name)


def bw_append_working(x):
    n = fileio.get_file_name(cons.daiban_workspace)
    if (x == n):
        x += " [Working]"
    return x


def tr_daiban(m):
    if (m == "b"):
        m = view()
    elif (m == "b;"):
        opt().view_specified = "1"
        m = view()
    elif (m == "bl" or s.st(m, "bl")):
        m = view(list_level=to_bl_level(m))
    elif (m == "ba"):
        opt().view_specified = None
        m = view()
    elif (m == "bva"):
        m = view(all_=True)
    elif (m == "bvs" or m == "bv"):
        m = vs()
    elif (m == "brl"):  # reload
        do_reload()
        m = view()
    elif (m == "bg"):
        m = "g " + daiban_file()
    elif (m == "bgo"):
        m = ".. g " + daiban_file() + ";f"
    elif (is_add(m)):
        m = do_add(m)
    elif (is_rm(m)):
        m = do_rm(m)
    elif (is_ci(m)):
        m = do_ci(m)
    elif (is_top(m)):
        m = do_top(m)
    elif (is_up(m)):
        m = do_up(m)
    elif (is_down(m)):
        m = do_down(m)
    return m


def view(all_=False, list_level=4):
    o = inst()
    lines = o.to_lines(all_, list_level=list_level)
    log(lines)
    return cons.ignore_cmd


def do_reload():
    cons.daiban = None
    opt().reset()


def vs():
    k = opt().view_specified
    log()
    if (k):
        env.do_vs_log("view specified", k)
    else:
        env.do_vs_log("view specified", "None")
    return cons.ignore_cmd


def is_add(m):
    if (s.ct(m, " ")):
        k = s.lf(m, " ")
        if (s.st(k, "b")):
            k = s.cf(k, "b")
            if (k in opt().keys[2] or k == "root"):
                return True
    return False


def do_add(m):
    k = s.lf(m, " ")
    line = s.clf(m, " ")
    k = s.cf(k, "b")
    o = opt().o_map[k]
    level = o.level + 1
    lines = s.sp(line)
    log()
    for line in lines:
        new_o = to(line, level)
        do_parent_(o, new_o, level)
        log("add daiban: \"{0}\"".format(new_o.full_line()))
    log()
    save()
    do_reload()
    set_spec(new_o)
    view()
    opt().last_add_key = k
    return cons.ignore_cmd


def is_rm(m):
    return s.st(m, "brm")


def do_rm(m):
    m = s.trimleft(s.cf(m, "brm"))
    k = m
    if (k in opt().keys[3]):
        log()
    else:
        k = search_key(k, "remove")
    if (k in opt().keys[3]):
        o = opt().o_map[k]
        if (not o.is_done):
            set_spec(o)
            log("remove daiban: \"{0}\"".format(o.full_line()))
            log()
            parent = o.parent
            parent.tasks.remove(o)
            save()
            do_reload()
            view()
    return cons.ignore_cmd


def is_ci(m):
    return s.st(m, "bci")


def do_ci(m):
    m = s.trimleft(s.cf(m, "bci"))
    k = m
    if (k in opt().keys[3]):
        log()
    else:
        k = search_key(k, "ci")
    if (k in opt().keys[3]):
        o = opt().o_map[k]
        m = "ci " + o.n
        return m
    return cons.ignore_cmd


def is_top(m):
    return s.st(m, "btop")


def do_top(m):
    m = s.trimleft(s.cf(m, "btop"))
    k = m
    if (k in opt().keys[3]):
        log()
    else:
        k = search_key(k, "top")
    if (k in opt().keys[3]):
        o = opt().o_map[k]
        if (not o.is_done):
            set_spec(o)
            log("move daiban to top: \"{0}\"".format(o.full_line()))
            log()
            parent = o.parent
            parent.tasks.remove(o)
            parent.tasks.insert(0, o)
            save()
            do_reload()
            view()
    return cons.ignore_cmd


def is_up(m):
    return s.st(m, "bup")


def do_up(m):
    m = s.trimleft(s.cf(m, "bup"))
    k = m
    if (k in opt().keys[3]):
        log()
    else:
        k = search_key(k, "up")
    if (k in opt().keys[3]):
        o = opt().o_map[k]
        if (not o.is_done):
            set_spec(o)
            log("move daiban up: \"{0}\"".format(o.full_line()))
            log()
            parent = o.parent
            index = parent.tasks.index(o)
            if (index > 0):
                parent.tasks.remove(o)
                parent.tasks.insert(index - 1, o)
            save()
            do_reload()
            view()
    return cons.ignore_cmd


def is_down(m):
    return s.st(m, "bdown")


def do_down(m):
    m = s.trimleft(s.cf(m, "bdown"))
    k = m
    if (k in opt().keys[3]):
        log()
    else:
        k = search_key(k, "down")
    if (k in opt().keys[3]):
        o = opt().o_map[k]
        if (not o.is_done):
            set_spec(o)
            log("move daiban down: \"{0}\"".format(o.full_line()))
            log()
            parent = o.parent
            index = parent.tasks.index(o)
            if (index < len(parent.tasks) - 1):
                parent.tasks.remove(o)
                parent.tasks.insert(index + 1, o)
            save()
            do_reload()
            view()
    return cons.ignore_cmd


def set_spec(o):
    if (opt().view_specified == None):
        if (o.level >= 2):
            opt().view_specified = o.get_root().full_key()
    else:
        if (o.level == 1):
            opt().view_specified = None


def search_key(k, n, all_=False):
    opt_ = opt()
    o = opt_.keys[3]
    o, k = search_key_in_specified(o, k)
    if (not all_):
        o = s._filter_(o, (lambda x: not opt_.o_map[x].is_done_()))
    o = s.cv_(o, lambda x: (x, opt_.o_map[x].n))
    o = s._filter_(o, (lambda x: s.isf(x[1], k)))
    if (o == None or len(o) == 0):
        return None
    elif (len(o) == 1):
        k = o[0][0]
        o_ = opt_.o_map[k]
        ulog.logl("daiban " + n + " list", [o_.full_line_f()])
        log()
        return o[0][0]
    else:
        o = s.cv_(o, lambda x: opt_.o_map[x[0]].full_line_f())
        o = ulist.select("daiban " + n, o)
        o = s.lf(o, " ")
        o = s.cv(o, ".", "")
        return o


def search_key_in_specified(o, k):
    if (s.ct(k, " ")):
        a = s.lf(k, " ")
        b = s.clf(k, " ")
        if (a in o):
            k = b
            o = s._filter_(o, s.st, a)
    return o, k


def daiban_file():
    return cons.daiban_workspace


def opt():
    if (cons.daiban_option == None):
        cons.daiban_option = option()
        inst()  # force to load
    return cons.daiban_option


def inst():
    if (cons.daiban == None):
        load()
    return cons.daiban


def load():
    root = to("root", 0)
    cons.daiban = root
    opt_ = opt()
    opt_.o_map["root"] = root
    for i in range(1, 5):
        opt_.keys[i - 1] += ["root"]
    lines = fileio.l(daiban_file())
    lines = s._filter_(lines, lambda x: x != "" and not x in ["No DaiBan.", "DaiBan:"])
    for line in lines:
        i = s.get_indent_size(line)
        line = s.trim(line)
        for k in range(4):
            level = k + 1
            if (i == 4 * level):
                o = to(line, level, load=True)
                parent_(o, level)


def save():
    o = inst()
    lines = o.to_lines(all_=True)
    fileio.w(daiban_file(), lines)


def to(line, level, load=False):
    o = daiban()
    if (load):
        n = s.trim(s.clf(line, "."))
    else:
        n = s.trim(line)
    o.is_done = s.st(n, "[d]")
    o.n = s.cf(n, "[d]")
    o.level = level
    return o


def parent_(o, level):
    p = cons.daiban
    for i in range(level - 1):  # @UnusedVariable
        p = sl(p.tasks)
    do_parent_(p, o, level)


def do_parent_(p, o, level):
    p.tasks += [o]
    p.sort()
    o.parent = p
    o.key = p.key + o.get_index_s()
    add_key(level, o)


def add_key(level, o):
    opt_ = opt()
    for i in range(level, 5):
        opt_.keys[i - 1] += [o.key]
    opt_.o_map[o.key] = o


def sl(l):
    return ulist.last(l)


def to_bl_level(m):
    if (m == "bl"):
        return 1
    else:
        return int(s.cf(m, "bl"))


class daiban:
    n = ""
    key = ""
    is_done = False
    level = 1
    parent = None
    tasks = None

    def __init__(self):
        self.tasks = []

    def __str__(self):
        return self.n

    def to_line(self):
        index_s = self.get_index_s()
        indent = s.get_indent_string(4 * self.level)
        index_indent_size = self.get_index_indent_size(self.level)
        msg = "{0}{1:" + str(index_indent_size) + "}{2}"
        n = self.n
        if (self.is_done):
            n = "[d]" + n
        return msg.format(indent, index_s + ".", n)

    def get_index(self):
        return self.parent.tasks.index(self) + 1

    def get_index_s(self):
        return self.to_index_s(self.get_index())

    def get_index_indent_size(self, level):
        if (level == 3):
            return 6
        return 4
    
    def to_index_s(self, index):
        if (self.level == 1):
            return str(index)
        elif (self.level == 2):
            return chr(96 + index)
        elif (self.level == 3):
            return cons.roman_numbers[index - 1]
        elif (self.level == 4):
            return str(index)
    
    def to_lines(self, all_=False, list_level=4):
        r = []
        if (not all_ and self.is_done):
            pass
        elif (not all_ and not self.is_view()):
            pass
        elif (self.level > list_level):
            pass
        else:
            if (self.level == 0):
                if (len(self.tasks) > 0):
                    r += ["DaiBan:", ""]
                else:
                    r += ["No DaiBan."]
            else:
                r += [self.to_line()]
                if (self.level == 1):
                    r += [""]
            if (len(self.tasks) > 0):
                for task_ in self.tasks:
                    r += task_.to_lines(all_, list_level=list_level)
                if (self.level == 1 and list_level > 1):
                    r += [""]
        return r
    
    def is_view(self):
        if (self.is_root()):
            return True
        spec = opt().view_specified
        if (spec):
            spec = opt().view_specified + "."
            if (not spec == None):
                k = self.full_key() + "."
                if (s.st(k, spec) or s.st(spec, k) or k == spec):
                    return True
                return False
        return True

    def full_key(self):  # 1.a.i.1
        if (self.level == 0):
            return ""
        elif (self.level == 1):
            return self.get_index_s()
        else:
            return self.parent.full_key() + "." + self.get_index_s()
        
    def full_key_short(self):  # 1ai1
        if (self.level == 0):
            return ""
        elif (self.level == 1):
            return self.get_index_s()
        else:
            return self.parent.full_key_short() + self.get_index_s()

    def full_line(self):
        return self.full_key() + ". " + self.n

    def full_line_f(self):
        return "{0:11}{1}".format(self.full_key() + ".", self.n)
    
    def get_root(self):
        o = self
        while (o.level > 1):
            o = o.parent
        return o
    
    def is_done_(self):
        if (self.level <= 1):
            return self.is_done
        if (self.is_done):
            return True
        else:
            return self.parent.is_done_()
        
    def is_root(self):
        return self.n == "root"
    
    def sort(self):
        r = []
        r += s._filter_(self.tasks, lambda x: not x.is_done)
        r += s._filter_(self.tasks, lambda x: x.is_done)
        self.tasks = r


class option:
    last_add_key = None
    view_specified = "1"
    keys = [[], [], [], []]
    o_map = dict()
    
    def reset(self):
        self.last_add_key = None
        self.keys = [[], [], [], []]
        self.o_map = dict()

