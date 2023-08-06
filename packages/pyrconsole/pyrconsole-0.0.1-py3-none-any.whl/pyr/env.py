import ustring         as s
from   ulog            import log

import cons            as cons
import fileio          as fileio
import ulog            as ulog


def translate(m):
    m00 = m
    m = env_debug(m)
    m = env_clean(m)
    m = env_view(m)
    ulog.log_trans(m00, m)
    return m


def env_debug(m):
    if (m == "-v"):
        m = "env -v"
    elif (m == "-vt"):
        m = "env -vt"
    elif (m == "-vp"):
        m = "env -vp"
    return m


def env_clean(m):
    if (m == "c"):
        m = "env c"
    elif (m == "ca"):
        m = "env ca"
    return m


def env_view(m):
    if (m == "vs"):
        m = "env vs"
    elif (m == "vsa"):
        m = "env vsa"
    return m


def handle(m):
    if (m == "-v"):
        debug()
    elif (m == "-vt"):
        trace()
    elif (m == "-vp"):
        debug_performance()
    elif (m == "c"):
        clean()
    elif (m == "ca"):
        clean()
        cons.p = cons.rn_dir
    elif (m == "vs"):
        vs()
    elif (m == "vsa"):
        vsa()


def debug():
    cons.debug = True
    log("enable debug log")


def trace():
    cons.trace = True
    log("enable trace log")


def debug_performance():
    cons.debug_performance = True
    log("enable debug performance log")


def vs():
    log("Welcome to R Console [Python]")
    log()
    do_vs_log("working dir", s.get_input_p())
    do_vs_log("list condition", enrich_list_condition_display(cons.list_condition))
    do_vs_log("find condition", enrich_find_condition_display(cons.find_condition))


def vsa():
    vs()
    vs_find()
    vs_list()
    vs_env()
    vs_log()
    vs_ci()
    vs_sep()
    vs_cmds()
    vs_filesystem()


def vs_find():
    do_vs_log("find picked", cons.find_condition_picked)


def vs_list():
    do_vs_log("list filter", enrich_list_condition_display(cons.list_filter))
    do_vs_log("view all", cons.view_all)


def vs_env():
    do_vs_log("debug", str(cons.debug))
    do_vs_log("debugp", str(cons.debug_performance))


def vs_log():
    do_vs_log("silent", str(cons.silent))
    do_vs_log("tmp_silent", str(cons.tmp_silent))
    do_vs_log("alog", str(cons.alog))
    do_vs_log("nawlog", str(cons.nawlog))
    do_vs_log("tab", len(cons.log_tab))
    do_vs_log("debug_tab", len(cons.debug_log_tab))


def vs_ci():
    do_vs_log("ci_mysql", str(cons.ci_mysql))


def vs_sep():
    do_vs_log("sep", cons.sep)


def vs_cmds():
    do_vs_log("last_command", cons.last_command)
    do_vs_log("space_command", cons.space_command)


def vs_filesystem():
    t = cons.file_system.type_
    if (t == "local"):
        do_vs_log("file_system", "[{0}]".format(t))
    else:
        ip = cons.file_system.c().ip
        do_vs_log("file_system", "[{0}:{1}]".format(t, ip))


def do_vs_log(n, o, tab=0):
    m = "{0:20}{1}".format(n + ":", o)
    if (tab == 0):
        log(m)
    else:
        ulog.logt(tab, m)


def enrich_list_condition_display(list_condition):
    if (list_condition != None and len(list_condition) > 0):
        return "l " + list_condition
    return ""


def enrich_find_condition_display(find_condition):
    if (find_condition != None and len(find_condition) > 0):
        return find_condition
    return ""


def clean():
    # cons.silent = 0
    # cons.alog = 0
    cons.debug = False
    cons.trace = False
    cons.debug_performance = False
    reset()


def reset():
    if (not cons.not_reset):
        cons.view_all = False
        cons.list_max = cons.list_max_default
        cons.output_file = None
        cons.cal_result = None
        cons.tasklist_filter = None
        reset_list()
        reset_find()
        reset_copy()
        reset_ci()
    else:
        cons.not_reset = False


def reset_list():
    cons.list_condition = None
    cons.list_filter = None
    cons.list_level = None
    cons.listed_files = None


def reset_find():
    cons.find_condition = None
    cons.find_condition_key = None
    cons.find_condition_multiple_lines = None
    cons.find_condition_picked = []
    cons.found_files = None
    cons.found_file_root = None


def reset_copy():
    cons.copy_files = []


def reset_ci():
    cons.ci_mysql = False


def has_find_condition():
    return not cons.find_condition == None


def has_list_condition():
    return not cons.list_condition == None


def has_found_files():
    return not cons.found_files == None


def is_find_in_file():
    return has_find_condition() and is_in_file()


def is_in_file():
    return fileio.is_file(cons.p)


def is_in_dir():
    return fileio.is_dir(cons.p)


def clean_up():
    try:
        ulog.clean_up_rl()
    except:
        pass
    import os
    os._exit(0)


def lastop_f(n):
    return cons.lastop_dir + s.sep(cons.lastop_dir) + s.cv(n, " ", "_") + ".txt"


def record_last_p(m):
    if (m not in ["b2", "back"]):
        cons.last_p = cons.p
    return m

