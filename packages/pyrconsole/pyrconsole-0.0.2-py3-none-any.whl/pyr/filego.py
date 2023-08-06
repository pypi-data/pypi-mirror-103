import ustring         as s
from   ulog            import log
from   ulog            import logd

import ci              as ci
import cons            as cons
import env             as env
import fileio          as fileio
import filelistfind    as filelistfind
import tar             as tar
import translate       as tr
import ulist           as ulist
import ulog            as ulog


def translate(m):
    m00 = m
    m = fmk(m)
    m = go_map(m)
    m = gb(m)
    m = gl(m)
    m = gf(m)
    m = space_number(m)
    m = space_sub_dir(m)
    m = ffs(m)
    m = dot_p(m)
    m = f_dot(m)
    m = fh(m)
    m = goto(m)
    m = prev_file(m)
    m = next_file(m)
    m = h123(m)
    m = vtba_sub(m)
    m = dot_dot(m)
    m = f_plus(m)
    m = code_line(m)
    m = message_code(m)
    m = a_up(m)
    m = a_find(m)
    m = i_find(m)
    m = m_dir(m)
    m = bf_zj(m)
    m = support(m)
    m = back(m)
    m = gex(m)
    m = gw20(m)
    ulog.log_trans(m00, m)
    return m


def go_map(m):
    if (cons.file_go_map.__contains__(m)):
        m = "g " + cons.file_go_map.get(m)
    elif (cons.file_open_map.__contains__(m)):
        if (m == "ok"):
            m = ".. kuiup;g " + cons.file_open_map.get(m) + ";f[]"
        else:
            m = ".. g " + cons.file_open_map.get(m) + ";f[]"
    return m


def gb(m):
    if (s.st(m, "gb ")):
        return "g {0}{1}{2}.bat".format(cons.bat_dir, s.sep(cons.bat_dir), s.cf(m, "gb "))
    return m


def gl(m):
    if (m == "gl" and fileio.is_dir(cons.p)):
        return "g last"
    return m


def gf(m):
    if (m == "gf"):
        if (not cons.mark_go_dir == None):
            mark_go_dir = cons.mark_go_dir
            cons.mark_go_dir = None
            return "g " + mark_go_dir
        else:
            return cons.ignore_cmd
    return m


def space_number(m):
    if (s.match(m, " \\d+")):
        to = s.cf(m, " ")
        if (s.is_number(to)):
            return "g " + to
    return m


def space_sub_dir(m):
    if (s.st(m, " ")):
        to = s.cf(m, " ")
        if (not to == ""):
            if (filelistfind.is_sub_dir(cons.p, to)):
                return "g " + cons.p + s.sep(cons.p) + filelistfind.get_sub_dir(cons.p, to)
    return m


def ffs(m):
    if (m == "ffs"):
        m = "f.10.101.0.4"
    elif (m == "ffs "):
        m = "f.10.101.0.4 "
    return m


def dot_p(m):
    if (s.st(m, ".p ")):
        m = s.cf(m, ".p ")
        m = "f." + m
    return m


def f_dot(m):
    if (m == "f."):
        m = "f." + ci.get_text()
    elif (m == "f. "):
        m = "f." + ci.get_text() + " "
    elif (s.st(m, "f.") and s.end(m, "  ")):
        m = "{0} ={1} ".format(s.trim(m), cons.p)
    
    if (s.st(m, "f.")):
        m = s.cf(m, "f.")
        select = s.end(m, " ")
        m = s.trim(m)
        in_dir = None
        if (s.ct(m, " =")):
            in_dir = tar.rp(s.rt(m, " ="))
            m = s.lf(m, " =")
        f = cons.fhf
        lines = fileio.l(f)
        lines = list(filter(lambda x: s.isf(x, m), lines))
        if (not in_dir == None):
            lines = list(filter(lambda x: s.st(x, in_dir), lines))
        if (len(lines) > 0):
            to = ulist.select("file", lines, select)
            if (not to == ""):
                m = "g " + to
            else:
                m = ""
        else:
            m = do_a_find(m)
            if (m == None):
                log("ERROR: No file with \"{0}\" in file history \"{1}\".".format(m, f))
                m = cons.ignore_cmd
            else:
                logd("find in all: " + m)
                m = "g " + m
    return m


def fh(m):
    if (m == "fh" or s.st(m, "fh ")):
        m = s.trim(s.cf_eq(m, "fh"))
        select = True
        file_path = cons.fhf
        lines = fileio.l(file_path)
        lines = list(filter(lambda x: s.isf(x, m), lines))
        if (len(lines) > 0):
            to = ulist.select("file", lines, select, max_size=20)
            if (not to == ""):
                m = "g " + to
            else:
                m = ""
    return m


def goto(m):
    if (s.st(m, "goto ", "go ", "gt ")):
        cons.goto = True
        m = "g " + s.cf(m, "goto ", "go ", "gt ")
    elif (s.st(m, "goto_not_reset ")):
        cons.goto = True
        cons.not_reset = True
        m = "g " + s.cf(m, "goto_not_reset ")
    return m


def prev_file(m):
    if (m == "pf"):
        p = cons.p
        parent = fileio.get_parent(p)
        files = filelistfind.list_dir_(parent)
        i = files.index(p)
        if (0 < i <= len(files) - 1):
            i -= 1
        to = files[i]
        m = "g " + to
    return m


def next_file(m):
    if (m == "nf"):
        p = cons.p
        parent = fileio.get_parent(p)
        files = filelistfind.list_dir_(parent)
        i = files.index(p)
        if (0 <= i < len(files) - 1):
            i += 1
        to = files[i]
        m = "g " + to
    return m


def h123(m):
    if (s.st(m, "g") and not s.ct(m, " ") and not tr.is_eis_key(m)):
        if (s.end(m, "1", "2", "3")):
            idx = s.sl(m, 1)
            k = s.cl(s.cf(m, "g"), 1)
            if (tar.is_key(k)):
                dir_ = tar.rp(k)
                dir_ = s.cv(dir_, tar.rp("home"), tar.rp("h" + idx))
                m = "g " + dir_
        else:
            if (not m in ["gl"]):
                k = s.cf(m, "g")
                if (tar.is_key(k)):
                    dir_ = tar.rp(k)
                    if (fileio.is_absolute_path(dir_)):
                        m = "g " + dir_
    elif (m in [":h1", ":h2", ":h3"]):
        m = s.cf(m)
        m = tar.rp(m)
        p = cons.p
        p00 = p
        for k in ["h1", "h2", "h3"]:
            p = s.cv(p, tar.rp(k), m)
        if (not p00 == p):
            m = "g " + p
        else:
            m = cons.ignore_cmd
    elif (s.is_wrapped(m, "h_all()")):
        m = s.unwrap(m, "h_all()")
        m1 = m
        m2 = s.cv(m, "1", "2")
        m3 = s.cv(m, "1", "3")
        m = ".. " + m1 + ";" + m2 + ";" + m3
    elif (m in [":h1 ", ":h2 ", ":h3 "]):
        if (env.has_find_condition()):
            if (cons.view_all):
                m = ".. " + s.trim(m) + ";a;" + cons.find_condition + "[]"
            else:
                m = ".. " + s.trim(m) + ";" + cons.find_condition + "[]"
        else:
            m = s.trim(m)
    return m


def vtba_sub(m):
    return cons.file_system.vtba_sub(m)


def vtba_sub__(m):
    if (s.st(m, "g ")):
        to = s.cf(m, "g ")
        to = tar.rp(to)
        home = tar.rp("home")
        if (s.st(to, home + s.sep(home)) or to == home):
            p = cons.p
            vtba = fileio.get_vtba(p)
            if (not vtba == None and not vtba == home):
                to = s.cv(to, home, vtba)
                m = "g " + to
    return m


def dot_dot(m):
    if (s.st(m, "..") and not s.ct(m, " ")):
        m = s.cf(m, "..")
        m = s.sep() + m
        if (s.ct(cons.p, m)):
            m = "g " + s.crt(cons.p, m)
        else:
            m = cons.ignore_cmd
    return m


def f_plus(m):
    if (m == "f+"):
        lines = filelistfind.list_files()
        fileio.insert_line(cons.fhf, lines)
        ulog.logl("add lines in " + cons.fhf, lines)
        m = cons.ignore_cmd
    return m


def code_line(m):
    if (not s.is_find_command(m)):
        if (s.match(m, ".*\\(.*\\.java:\\d+\\)")):
            m = s.find_wrapped(m, "()")
            n = s.lf(m, ":")
            i = s.clf(m, ":")
            m = ".. f.{0};{1}".format(n, i)
        elif (is_file_and_line(m)):
            m = do_file_and_line(m)
    return m


def message_code(m):
    if (not s.is_find_command(m)):
        if (s.is_message_code(m)):
            m = s.lf(m, "=")
            clz = s.lf(m, ".")
            m = s.cv(m, ".", "_")
            m = ".. f.{0}.java;fs {1};1[]".format(clz, m)
        elif (s.is_locale_code(m)):
            m = s.rt(m, "MessageCode.")
            m = s.lf(m, ",")
            m = s.lf(m, ")")
            m = s.cv(m, "_", ".")
            m = ".. glo;fs {0};1[]".format(m)
    return m


def is_file_and_line(m):
    n_ = s.n(m, ":")
    if (n_ >= 2):
        for i in range(n_ - 2):  # @UnusedVariable
            m = s.crt(m, ":")
        line = s.rt(m, ":")
        file = s.crt(m, ":")
        if (fileio.is_absolute_path(file) and s.is_number(line)):
            return True
    return False


def do_file_and_line(m):
    n_ = s.n(m, ":")
    if (n_ >= 2):
        for i in range(n_ - 2):  # @UnusedVariable
            m = s.crt(m, ":")
        line = s.rt(m, ":")
        file = s.crt(m, ":")
        if (fileio.is_absolute_path(file) and s.is_number(line)):
            m = ".. g {0};{1}".format(file, line)
    return m


def a_up(m):
    if (m == "a up"):
        do_a_up()
        m = cons.ignore_cmd
    return m


def a_find(m):
    if (s.st(m, "a ")):
        m = s.cf(m, "a ")
        if (len(m) >= 3):
            m = do_a_find(m)
            if (m):
                m = "g " + m
            else:
                m = cons.ignore_cmd
    return m


def i_find(m):
    if (s.st(m, "i ")):
        m = s.cf(m, "i ")
        m = do_i_find(m)
        if (m):
            m = "g " + m
        else:
            m = cons.ignore_cmd
    return m


def m_dir(m):
    m = do_lastop(m, ":dir", "colon_dir")
    if (m == ":v"):
        if (cons.m_dirs):
            ulog.logl("m_dirs", cons.m_dirs)
        else:
            log("no m_dirs")
        m = cons.ignore_cmd
    elif (s.st(m, ":dir ")):
        m00 = m
        m = s.cf(m, ":dir ")
        cons.m_dirs = s.sp(m, " ")
        ulog.logl("m_dirs", cons.m_dirs)
        fileio.insert_line(env.lastop_f("colon_dir"), m00)
        m = cons.ignore_cmd
    elif (not cons.m_dirs == None and s.st(m, ":")):
        m = s.cf(m, ":")
        cmds = []
        for dir_ in cons.m_dirs:
            msg = "\nrun \"{0}\" in \"{1}\"\n".format(m, tar.rp(dir_))
            cmd = "log {0}[];;log_tab 4;;g {1};;{2}[];;log_tab c".format(msg, dir_, m)
            cmds += [cmd]
        m = ".. " + s.conn(cmds, ";;")
    return m


def bf_zj(m):
    if (m == "bf"):
        m = ".. gbf;zj;g;g[]"
    return m


def support(m):
    for k in [";s", ";d", ";b"]:
        support_name = {
            ";s" : "Support",
            ";d" : "DO",
            ";b" : "Bug",
        }
        if (m == k):
            m = ".. g rnp/{0};zj;g[]".format(support_name[k])
        elif (m in [k + " ", k + "h"]):
            m = "g rnp/{0}".format(support_name[k])
        elif (s.st(m, k) and not tr.is_eis_key(m)):
            m = s.trim(s.cf(m, k))
            dir_ = tar.rp("rnp/" + support_name[k])
            files = filelistfind.list_dir_(dir_, con=m)
            if (len(files) == 1):
                file = files[0]
            else:
                files = s.cv_(files, fileio.get_file_name)
                file = ulist.select(s.lower(support_name[k]), files, max_size=-1)
                if (file == None or file == ""):
                    return cons.ignore_cmd
                file = dir_ + s.sep(dir_) + file
            m = ".. g {0}[];tou".format(file)
    return m


def back(m):
    if (m in ["b2", "back"]):
        m = "g " + cons.last_p
    return m


def gex(m):
    if (m == "gex"):
        if (s.st(cons.p, tar.rp("udf/modules"))):
            p = cons.p
            p = s.crtw(p, "module")
            n = fileio.get_file_name(p)
            to = tar.rp("eudfml/" + n)
            m = "g " + to
        elif (s.end(cons.p, ".java")):
            fsn = fileio.get_file_simple_name(cons.p)
            cn = fsn + ".class"
            f = cons.alogs_dir + s.sep(cons.alogs_dir) + "classes.log"
            l = fileio.lwc(f)
            l = s._filter_(l, s.end, s.sep(cons.alogs_dir) + cn)
            if (len(l) > 0):
                to = ulist.select("classes", l)
                m = "g " + to
    return m


def gw20(m):
    if (m == "gw20"):
        p = cons.p
        if (s.st(p, cons.yoda)):
            p = s.cf(p, cons.yoda)
            p = "D:\\jedi\\branches\\wildfly20_upgrade" + p
            m = "g " + p
        else:
            p = s.cf(p, "D:\\jedi\\branches\\wildfly20_upgrade")
            p = cons.yoda + p
            m = "g " + p
    return m


def fmk(m):
    if (m == "fmk"):
        m = " fmk"
    elif (s.st(m, "fmk ")):
        m = "g " + s.cf(m, "fmk ")
    elif (m == "f.mk"):
        m = "fmk " + cons.p
    elif (m == "fmk "):
        m = " fmkh"
    return m


def handle(m):
    go(m)


def go(m):
    try:
        to_dir = filelistfind.rp(cons.p, m)
        if (to_dir != None):
            do_go(to_dir)
            log("switch to: " + cons.p)
            if (not cons.goto):
                filelistfind.view(cons.p)
    finally:
        cons.goto = False


def do_go(p):
    cons.p = p
    filelistfind.cd(cons.p)
    env.reset()
    insert_fhf(cons.p)


def insert_fhf(p):
    fileio.insert_line(cons.fhf, p)


def reset_working_dir():
    p = cons.p
    go = False
    while not fileio.exists(p):
        p = fileio.get_parent(p)
        go = True
    if (go):
        do_go(p)


def do_a_up():
    filelist_dir = cons.alogs_dir + s.sep(cons.alogs_dir) + "filelist"
    files = filelistfind.list_dir_(filelist_dir)
    a_up_cache = dict()
    for dir_ in ["D:\\jedi\\yoda", "D:\\jedi\\src", "D:\\jedi\\branches"]:
        for file in files:
            do_a_up_file(file, dir_, a_up_cache)
    log()
    do_a_up_save(a_up_cache)
    log()


def do_a_up_save(a_up_cache):
    for prefix in a_up_cache.keys():
        prefix_file = do_a_up_to_prefix_file(prefix)
        if (not fileio.exists(prefix_file)):
            fileio.mkdir(fileio.get_parent(prefix_file))
        fileio.w(prefix_file, a_up_cache[prefix])
        cons.do_a_up_line_file_count += 1
        if (cons.do_a_up_line_file_count % 100 == 0):
            log("a up files: " + str(cons.do_a_up_line_file_count))


def do_a_up_file(file, dir_, a_up_cache):
    lines = fileio.l(file)
    for line in lines:
        do_a_up_line(line, dir_, a_up_cache)


def do_a_up_line(line, dir_, a_up_cache):
    if (s.st(line, dir_)  and not s.st(line, "D:\\jedi\\yoda\\export") and s.end(line, ".java", ".xml")):
        n = fileio.get_file_simple_name(line)
        prefix = s.lower(n)
        if (len(n) > 3):
            prefix = s.lower(s.sf(n, 3))
        prefix_list = []
        if (a_up_cache.__contains__(prefix)):
            prefix_list = a_up_cache[prefix]
        else:
            a_up_cache[prefix] = prefix_list
        if (not line in prefix_list):
            prefix_list += [line]
        cons.do_a_up_line_count += 1
        if (cons.do_a_up_line_count % 10000 == 0):
            log("a up lines: " + str(cons.do_a_up_line_count))


def do_a_find(m):
    prefix = s.sf(m, 3)
    prefix_file = do_a_up_to_prefix_file(prefix)
    lines = fileio.l(prefix_file)
    lines = s.filter_(lines, m, s.isf)
    line = ulist.select("find in all [" + m + "]", lines, max_size=-1)
    return line


def do_i_find(m):
    prefix = m
    prefix_file = do_i_to_prefix_file(prefix)
    lines = fileio.l(prefix_file)
    lines = s.rmdup(lines)
    line = ulist.select("find in all [" + m + "]", lines)
    return line


def do_a_up_to_prefix_file(prefix):
    prefix = list(prefix)
    prefix = s.conn(prefix, "\\")
    prefix_file = "D:\\index\\javaindex_a_up\\" + prefix + "\\prefix_files.txt"
    return prefix_file


def do_i_to_prefix_file(prefix):
    prefix = list(prefix)
    prefix = s.conn(prefix, "\\")
    prefix_file = "D:\\index\\javaindex\\" + prefix + "\\files.txt"
    return prefix_file


def do_lastop(m, k, n):
    if (m == k):
        m = fileio.get_first_line(env.lastop_f(n))
    elif (m == k + " "):
        lines = fileio.l(env.lastop_f(n))
        m = ulist.select(":dir", lines)
    elif (m == k + "f"):
        m = "g " + env.lastop_f(n)
    return m

