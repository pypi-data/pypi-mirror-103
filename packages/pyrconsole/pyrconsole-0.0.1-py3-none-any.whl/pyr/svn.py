import ustring         as s
from   ulog            import log

import ulog            as ulog
import ulist           as ulist
import cons            as cons
import fileio          as fileio
import ids             as ids
import filelistfind    as filelistfind
import run             as run
import ustring_ops     as ops
import ci              as ci
import tar             as tar


def translate(m):
    m00 = m
    if (s.st(m, "svn ")):
        if (s.st(m, "svn st ")):
            cons.run_callback = st_callback
        m = "run " + m
    elif (is_svn_op(m, "st")):
        m = get_svn_op(m, "st", "st")
        cons.run_callback = st_callback
    elif (is_svn_op(m, "sd")):
        m = get_svn_op(m, "sd", "diff")
    elif (is_svn_op(m, "sup")):
        m = get_svn_op(m, "sup", "up")
    elif (is_svn_op(m, "sr")):
        m = get_svn_op(m, "sr", "revert", "-R *")
    elif (s.st(m, "sc ")):
        m = get_sc(m)
    elif (is_svnr(m)):
        m = get_svnr(m)
    elif (m == "svni"):
        m = "run svn info"
    elif (is_sw_short(m)):
        m = get_sw_short(m)
    elif (s.st(m, "sw ")):
        m = get_sw(m)
    elif (m == "s+-" or m == "sadd"):
        m = get_add(m)
    elif (m == "sdi"):
        m = ".. log diff files: %p% with base[];runt TortoiseProc.exe /command:diff /path:%p%"
    elif (ids.is_ids(m, "sdi")):
        m = get_sdi(m)
    elif (m == "slog"):
        m = ".. log open svn log: %p%[];runt TortoiseProc.exe /command:log /path:%p%"
    elif (is_comp(m)):
        m = do_comp(m)
    ulog.log_trans(m00, m)
    return m


def is_svn_op(m, op):
    return m == op or (ids.is_ids(m, op) and fileio.is_dir(cons.p))


def get_svn_op(m, op, svn_op, dir_params=""):
    if (m == op or s.st(m, op + " ")):
        if (fileio.is_dir(cons.p)):
            if (dir_params == ""):
                m = "run svn " + svn_op
            else:
                m = "run svn " + svn_op + " " + dir_params
        else:
            m = "run svn " + svn_op + " " + fileio.get_file_name(cons.p)
    elif (ids.is_ids(m, op) and fileio.is_dir(cons.p)):
        files = filelistfind.list_files()
        files = ids.get_selected(files, m, op)
        files = list(map(lambda fp: s.cf(fp, cons.p + s.sep(cons.p)), files))
        m = "run svn " + svn_op + " " + s.conn(files, " ")
    return m


def get_sc(m):
    msg = s.cf(m, "sc ")
    if (fileio.is_dir(cons.p)):
        m = "run svn commit -m \"{0}\"".format(msg)
    else:
        m = "run svn commit \"{0}\" -m \"{1}\"".format(fileio.get_file_name(cons.p), msg)
    return m


def is_svnr(m):
    return s.st(m, "svnr ") or m == "svnr"


def get_svnr(m):
    if (m == "svnr"):
        m = ci.get_text()
    else:
        m = s.cf(m, "svnr ")
    m = "run svn up -r {0}".format(m)
    return m


def is_sw_short(m):
    return m in cons.branches_sw.keys()


def get_sw_short(m):
    return "sw " + cons.branches_sw[m]


def get_sw(m):
    m = s.cf(m, "sw ")
    if (cons.branches.__contains__(m)):
        br = cons.branches[m]
        p = s.cf(cons.p, cons.yoda)
        p = s.cf(p, 1)
        p = s.to_linux_path(p)
        url = br + p
        m = "run svn sw " + url
        log("svn switch: " + cons.p)
        log("         -> " + url)
        log()
    else:
        log("svn branch not found: " + m)
        m = cons.ignore_cmd
    return m


def get_add(m):  # @UnusedVariable
    st_lines = run.r("svn st")
    add_lines = ulist.filter_list(st_lines, "?", s.st)
    if (add_lines):
        add_lines = ops.do_ops(add_lines, "cf 1;;trim;;wrap")
        add_s = "run svn add " + s.conn(add_lines, " ")
        run.ex(add_s)
    del_lines = ulist.filter_list(st_lines, "!", s.st)
    if (del_lines):
        del_lines = ops.do_ops(del_lines, "cf 1;;trim;;wrap")
        del_s = "run svn del " + s.conn(del_lines, " ")
        run.ex(del_s)
    return cons.ignore_cmd


def get_sdi(m):
    files = filelistfind.list_files()
    files = ids.get_selected(files, m, "sdi")
    files = s.cv_(files, s.nl, "log diff files: LINE with base[];runt TortoiseProc.exe /command:diff /path:LINE")
    m = ".. " + s.conn(files, ";")
    return m


def st_callback(lines):
    if (len(lines) > 0):
        ulog.logl("", lines)
        cons.listed_files = ops.do_ops(lines, "clf  ;;trim;;af " + (cons.p + s.sep(cons.p)))
        cons.mark_go_dir = cons.listed_files[0]


def is_svn_dir(f):
    while (not fileio.exists(f + s.sep(f) + ".svn")):
        f00 = f
        f = fileio.get_parent(f)
        if (f00 == f):
            return False
    return True


def is_comp(m):
    if (s.st(m, "comp")):
        m = s.trim(s.cf(m, "comp"))
        return ids.is_pure_ids(m) or tar.is_dir_key(tar.get_root_key(m)) or fileio.is_absolute_path(m)
    return False


def do_comp(m):
    m = s.trim(s.cf(m, "comp"))
    if (ids.is_pure_ids(m)):
        if (s.ct(m, " ")):
            m = m + " k"
        else:
            m = m + "k"
        files = filelistfind.list_files()
        files = ids.get_selected(files, m, "k")
        if (len(files) == 2):
            f1 = files[0]
            f2 = files[1]
            m = do_comp_(f1, f2)
        else:
            m = cons.ignore_cmd
    else:
        f1 = cons.p
        n = fileio.get_file_name(f1)
        files = filelistfind.list_dir_(tar.rp(m), "(" + n + ")", view_all=True)
        if (len(files) == 1):
            f2 = files[0]
            m = do_comp_(f1, f2)
        else:
            m = cons.ignore_cmd
    return m


def do_comp_(f1, f2):
    log("diff files: " + f1)
    log("      with: " + f2)
    return "runt TortoiseProc.exe /command:diff /path:\"{0}\" /path2:\"{1}\"".format(f2, f1)

