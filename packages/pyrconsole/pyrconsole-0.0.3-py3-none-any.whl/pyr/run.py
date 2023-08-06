import ustring         as s
from   ulog            import log
from   ulog            import logd

import os

import ci              as ci
import cons            as cons
import fileio          as fileio
import tar             as tar
import ulog            as ulog

run_callbacks = {
    "jps" : "run.jps_callback",
}


def translate(m):
    m00 = m
    m = r_br(m)
    m = r_runt(m)
    m = r_st(m)
    m = r_is(m)
    m = r_map(m)
    m = r_fc(m)
    m = r_tl(m)
    m = r_js(m)
    ulog.log_trans(m00, m)
    return m


def r_br(m):
    if (m == "br"):
        m = "br " + ci.get_text()
    if (s.st(m, "br ")):
        m = s.cf(m, "br ")
        m = s.clfw(m, "VITR00")
        if (s.ct(m, " ")):
            m = s.lf(m, " ")
        m = s.cf(m, "VITR00")
        m = "br " + m
    return m


def r_runt(m):
    if (s.st(m, "runt ")):
        m = s.cf(m, "runt ")
        m = "run inthread start " + m
    return m


def r_st(m):
    ops = ["set",
           "bug",
           "br"]
    for op in ops:
        if (s.st(m, op + " ")):
            m = "run " + m
    return m


def r_is(m):
    ops = ["set",
           "hostname",
           "jps",
           "bds",
           "todf"]
    for op in ops:
        if (m == op):
            m = "run " + m
    return m


def r_map(m):
    if (cons.run_cmds.__contains__(m)):
        m = "run " + cons.run_cmds[m]
    return m


def r_fc(m):
    if (s.st(m, "fc ")):
        m = s.cf(m, "fc ")
        keep_dir = s.has_p(m, "kd")
        if (keep_dir):
            m = s.rm_p(m, "kd")
        no_parent = s.has_p(m, "np")
        if (no_parent):
            m = s.rm_p(m, "np")
        if (m == "-"):  # fc -
            if (keep_dir):
                m = ".. r;run {0} /cmd=delete \"{1}\";md {2};gf".format(cons.fast_copy, cons.p, fileio.get_file_name(cons.p))
            else:
                m = ".. r;run inthread start {0} /cmd=delete \"{1}\"".format(cons.fast_copy, cons.p)
            log("fast delete: " + cons.p)
        elif (s.st(m, "- ")):
            from_dir = cons.p
            to_dir = tar.rp(s.cf(m, "- "))
            if (not no_parent):
                to_dir = to_dir + s.sep(to_dir) + fileio.get_file_name(from_dir);
            fileio.mkdir(to_dir)
            log("fast copy: " + from_dir)
            log("        -> " + to_dir)
            cons.mark_go_dir = to_dir
            m = "run inthread start {0} /cmd=force_copy \"{1}\" /to=\"{2}\"".format(cons.fast_copy, from_dir, to_dir)
    return m


def r_tl(m):
    import tasklist as tasklist
    return tasklist.translate(m)


def r_js(m):
    if (cons.jps_processes):
        no_open = s.end(m, " ")
        m = s.trim(m)
        import ids
        if (ids.is_ids(m, "js")):
            processes = ids.get_selected(cons.jps_processes, m, "js")
            for process in processes:
                pid = s.trim(s.lf(process, " "))
                n = s.trim(s.clf(process, " "))
                lines = r("jstack " + pid)
                lines = s._cv_(lines, lambda x: s.cv(x, "\t", "    "))
                f = s.alogs_("thread_dumps" + s.sep() + n + s.sep() + n + "_" + pid + ".txt")
                fileio.mkdir(fileio.get_parent(f))
                if (fileio.exists(f)):
                    import filedelete
                    try:
                        ulog.tmp_silent()
                        filedelete.do_del_file(f)
                    finally:
                        ulog.no_tmp_silent()
                fileio.w(f, lines)
                if (not no_open):
                    import fileopen
                    fileopen.open_file(f)
                    m = cons.ignore_cmd
                else:
                    m = "g " + f
                cons.mark_go_dir = f
    return m


def handle(m):
    init_run_callbacks(m)
    if (cons.run_callback == None):
        run_command(m)
    else:
        cons.run_callback(r(m))
        cons.run_callback = None


def init_run_callbacks(m):
    if (run_callbacks.__contains__(m)):
        cons.run_callback = s._func_(run_callbacks[m])
    

def handle_bat(m):
    bat_file = "{0}{1}{2}.bat".format(cons.bat_dir, s.sep(cons.bat_dir), m)
    if (fileio.exists(bat_file)):
        handle(m)


def run_command(m):
    if (s.st(m, "inthread ")):
        m = s.cf(m, "inthread ")
        import threading
        t = threading.Thread(target=do_run_command_t, args=(m,))
        t.start()
    else:
        do_run_command(m)


def do_run_command(m):
    logd("run: " + m)
    f = os.popen(m, "r")
    while (True):
        line = f.readline()
        if (line):
            log(s.clean_line_sep(line))
        else:
            break


def do_run_command_t(m):
    logd("run: " + m)
    os.system(m)
    

def do_run_command_with_result(m):
    try:
        logd("run: " + m)
        f = os.popen(m, "r")
        r = []
        while (True):
            line = f.readline()
            if (line):
                r += [s.clean_line_sep(line)]
            else:
                break
        return r
    finally:
        f.close()


def ex(m):  # no output
    m = s.cf(m, "run ")
    do_run_command(m)


def r(m):  # with output
    m = s.cf(m, "run ")
    r_l = do_run_command_with_result(m)
    if (r_l == [""]):
        r_l = []
    return r_l


def jps_callback(lines):
    lines = s.filter_(lines, "jps", s.nctic)
    lines = s.sort(lines, sort_key_func=lambda x:int(s.lf(x, " ")))
    lines = s.duiqi(lines, " ")
    cons.jps_processes = lines
    ulog.logl("java processes", lines)

