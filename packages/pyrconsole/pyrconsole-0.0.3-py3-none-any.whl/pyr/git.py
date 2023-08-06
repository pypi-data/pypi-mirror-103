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


def translate(m):
    m00 = m
    if (is_git_dir(cons.p)):
        if (s.st(m, "git ")):
            if (s.st(m, "git st ")):
                cons.run_callback = st_callback
            m = "run " + m
        elif (is_git_op(m, "st")):
            m = get_git_op(m, "st", "status")
            cons.run_callback = st_callback
        elif (is_git_op(m, "sd")):
            m = get_git_op(m, "sd", "diff")
        elif (is_git_op(m, "sup")):
            m = get_git_op(m, "sup", "up")
        elif (is_git_op(m, "sr")):
            m = get_git_op(m, "sr", "revert", "-R *")
        elif (s.st(m, "sc ")):
            m = get_sc(m)
        elif (m == "giti"):
            m = "run git info"
        elif (is_sw_short(m)):
            m = get_sw_short(m)
        elif (s.st(m, "sw ")):
            m = get_sw(m)
        elif (m == "s+-" or m == "sadd"):
            m = get_add(m)
        elif (m == "sdi"):
            m = ".. log diff files: %p% with base[];runt TortoiseGitProc.exe /command:diff /path:%p%"
        elif (ids.is_ids(m, "sdi")):
            m = get_sdi(m)
        elif (m in ["glog", "slog"]):
            m = ".. log open git log: %p%[];runt TortoiseGitProc.exe /command:log /path:%p%"
    ulog.log_trans(m00, m)
    return m


def is_git_op(m, op):
    return m == op or (ids.is_ids(m, op) and fileio.is_dir(cons.p))


def get_git_op(m, op, git_op, dir_params=""):
    if (m == op or s.st(m, op + " ")):
        if (fileio.is_dir(cons.p)):
            if (dir_params == ""):
                m = "run git " + git_op
            else:
                m = "run git " + git_op + " " + dir_params
        else:
            m = "run git " + git_op + " " + fileio.get_file_name(cons.p)
    elif (ids.is_ids(m, op) and fileio.is_dir(cons.p)):
        files = filelistfind.list_files()
        files = ids.get_selected(files, m, op)
        files = list(map(lambda fp: s.cf(fp, cons.p + s.sep(cons.p)), files))
        m = "run git " + git_op + " " + s.conn(files, " ")
    return m


def get_sc(m):
    msg = s.cf(m, "sc ")
    if (fileio.is_dir(cons.p)):
        m = "run git commit -m \"{0}\"".format(msg)
    else:
        m = "run git commit \"{0}\" -m \"{1}\"".format(fileio.get_file_name(cons.p), msg)
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
        m = "run git sw " + url
        log("git switch: " + cons.p)
        log("         -> " + url)
        log()
    else:
        log("git branch not found: " + m)
        m = cons.ignore_cmd
    return m


def get_add(m):  # @UnusedVariable
    st_lines = run.r("git st")
    add_lines = ulist.filter_list(st_lines, "?", s.st)
    if (add_lines):
        add_lines = ops.do_ops(add_lines, "cf 1;;trim;;wrap")
        add_s = "run git add " + s.conn(add_lines, " ")
        run.ex(add_s)
    del_lines = ulist.filter_list(st_lines, "!", s.st)
    if (del_lines):
        del_lines = ops.do_ops(del_lines, "cf 1;;trim;;wrap")
        del_s = "run git del " + s.conn(del_lines, " ")
        run.ex(del_s)
    return cons.ignore_cmd


def get_sdi(m):
    files = filelistfind.list_files()
    files = ids.get_selected(files, m, "sdi")
    files = s.cv_(files, s.nl, "log diff files: LINE with base[];runt TortoiseGitProc.exe /command:diff /path:LINE")
    m = ".. " + s.conn(files, ";")
    return m


def st_callback(lines):
    if (len(lines) > 0):
        ulog.logl("", lines)
        cons.listed_files = ops.do_ops(lines, "clf  ;;trim;;af " + (cons.p + s.sep(cons.p)))
        cons.mark_go_dir = cons.listed_files[0]


def is_git_dir(f):
    return s.st(f, "D:\\huazhi\\projects\\git")
    '''
    while (not fileio.exists(f + s.sep(f) + ".git")):
        f00 = f
        f = fileio.get_parent(f)
        if (f00 == f):
            return False
    return True
    '''

