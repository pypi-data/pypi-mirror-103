import cons            as cons
import ustring         as s

import ulog_format     as ulog_format


def translate(m):
    m00 = m
    m = trans_log(m)
    m = go_rl(m)
    m = tr_log_tab(m)
    log_trans(m00, m)
    return m


def trans_log(m):
    if (m == "log"):
        m = "ulog \"\""
    elif (s.st(m, "log ")):
        m = "u" + m
    return m


def go_rl(m):
    if (m == "rl"):
        m = "g " + cons.rl_file
    return m


def tr_log_tab(m):
    if (s.st(m, "log_tab ")):
        m = s.cf(m, "log_tab ")
        if (m == "c"):
            clean_log_tab()
        elif (m == "v"):
            view_log_tab()
        else:
            set_log_tab(int(m))
        m = cons.ignore_cmd
    return m


def handle(m):
    log(s.unwrap(m))


def log(s=""):
    if (not is_silent() and not is_tmp_silent()):
        log_one(s)
    else:
        if (is_alog() and not is_nawlog() and not is_tmp_silent()):
            log_one(s)


def loga(s=""):
    do_log_one(s)


def log_format(s=""):
    if (isinstance(s, list)):
        for i in s:
            do_log_format(i)
    else:
        do_log_format(s)
    
    
def do_log_format(s=""):
    if (ulog_format.is_format_log_line(s)):
        s = ulog_format.format_log_line(s, 0)
    log(s)


def log_one(s=""):
    if (isinstance(s, list)):
        for i in s:
            log(i)
    else:
        if (not cons.output_file == None):
            append_line(cons.output_file, s)
        else:
            do_log_cache()
            do_log_one(s)


def do_log_cache():
    if (cons.has_log_cache):
        for s in cons.log_cache:
            do_log_one(s)
        clean_log_cache()


def do_log_one(s, debug=False):
    if (not isinstance(s, str)):
        s = str(s)
    log_s = log_tab(debug=debug) + s
    print(log_s)
    do_w_rl(log_s)
    log_callback(log_s)
    cons.logd_el = (s == "")


def log_callback(m):
    for k in ["zip", "jar", "war", "ear"]:
        if (s.ct(m, "Building " + k + ": ")):
            cons.mark_go_dir = s.rt(m, "Building " + k + ": ")


def do_w_rl(m):
    if (cons.rl_start and not cons.rl_clean_up):
        try:
            rl = get_rl()
            rl.write(m + "\n")
            rl.flush()
        except:
            pass


def get_rl():
    if (cons.rl == None):
        d = cons.alogs_dir + "\\RConsole\\logs"
        n = len(s._r_("filelistfind.list_dir_", d))
        n += 1
        f = d + "\\" + str(n) + ".log"
        cons.rl_file = f
        cons.rl = open(f, "a")
    return cons.rl


def start_rl():
    cons.rl_start = True


def clean_up_rl():
    cons.rl.close()
    cons.rl = None
    cons.rl_clean_up = True
    s._r_("filedelete.do_del_file", cons.rl_file)


def append_line(f, line):
    fi = open(f, "a")
    fi.write(log_tab() + line + "\n")
    fi.close()


def logd(s="", need_el=False):
    if (cons.debug):
        if (need_el and not cons.logd_el):
            do_log_one("", debug=True)
        if (ulog_format.is_format_log_line(s)):
            s = ulog_format.format_log_line(s, 0)
        do_log_one(s, debug=True)


def logtr(s=""):
    if (cons.trace):
        do_log_one(s)


def logp(n, start, suffix=""):
    if (cons.debug_performance):
        if (not cons.logd_el):
            do_log_one("")
        do_log_one("{0} cost: {1} ms{2}".format(n, str(s.nowts() - start), suffix))
        do_log_one("")


def logc(s=""):  # put in cache first
    cons.log_cache.append(s)
    cons.has_log_cache = True


def logt(n=0, s=""):  # use log tab
    try:
        set_log_tab(n)
        log(s)
    finally:
        clean_log_tab()


def logdt(n=0, s=""):  # use log tab
    try:
        set_log_tab(n, debug=True)
        logd(s)
    finally:
        clean_log_tab(debug=True)


def logkv(l, n="", sp=" "):
    if (isinstance(l, str)):
        l = [l]
    keys = s.cv_(l, s.lf, sp)
    indent = s.max_len(keys)
    if (n != ""):
        n = n + ": "
    msg = "{0}{1:" + str(indent) + "} = {2}"
    for l_ in l:
        line = msg.format(n, s.lf(l_, sp), s.clf(l_, sp))
        if (ulog_format.is_format_log_line(line)):
            line = ulog_format.format_log_line(line, 0)
        log(line)


def logh(n, m):
    log()
    log(n + ":")
    log()
    l = []
    for k in m:
        l += ["{0:20}{1}".format(k, m[k])]
    logl("", l)
    log()


def clean_log_cache():
    cons.log_cache = []
    cons.has_log_cache = False


def log_trans(m00, m):
    if (m00 != m and cons.debug):
        m00 = s.wrap_sp(m00)
        m = s.wrap_sp(m)
        logd("{0:4}{1}".format("", m00), need_el=True)
        logd("{0:>4}{1}".format("-> ", format_trans(m)))


def format_trans(m):
    if (s.st(m, ". ", ".. ") and len(m) > 170):
        pass
        # m = s.cv(m, ";;", ";;\n       ")
        # m = format_trans_svn(m)
    return s.encode_for_replace_back(m)


def format_trans_svn(m, keys=None):
    l = s.sp(m)
    r = []
    svn_key = None
    svn_keys = get_svn_keys()
    if (keys):
        svn_keys = keys
    for svn_key_ in svn_keys:
        if (s.ct(m, svn_key_)):
            svn_key = svn_key_
    if (svn_key):
        for line in l:
            if (s.st(line, svn_key)):
                line = s.cf(line, svn_key)
                line = s.sp(line, " ")
                line = s.conn(line, "\n" + s.get_indent_string(len(svn_key)))
                line = svn_key + line
            r += [line]
        return s.conn(r, "\n")
    return m


def get_svn_keys():
    if (cons.svn_keys == None):
        indent = s.get_indent_string(7)
        cons.svn_keys = ["svn st ", "svn diff ", "svn revert -R "]
        cons.svn_keys = s.cv_(cons.svn_keys, s.af, indent)
    return cons.svn_keys


def log_line_change(m00, m):
    if (m00 != m):
        m00 = s.wrap_sp(m00)
        m = s.wrap_sp(m)
        log("{0:4}{1}\n{2:>4}{3}".format("", m00, "-> ", m))


def logl(n, l):
    if (not n == ""):
        log(n + ":")
        log()
    i = 0
    for line in l:
        i = i + 1
        if (ulog_format.is_format_log_line(line)):
            line = ulog_format.format_log_line(line, 10)
        log("{0:4}{1:6}{2}".format("", str(i) + ":", line))


def log_dict(n, d):
    if (len(d) > 0):
        keys = list(d.keys())
        keys.sort()
        indent = max(s.cv_(keys, s.get_length))
        l = []
        for key in keys:
            msg = "{0:" + str(indent) + "} = {1}"
            l += [msg.format(key, d[key])]
        logl(n, l)


def list_filter_log_str():
    if (not cons.list_condition == None):
        return " ({0})".format(cons.list_condition)
    return ""


def silent(silent):
    if (silent):
        cons.silent = cons.silent + 1


def no_silent(silent):
    if (silent):
        cons.silent = cons.silent - 1


def is_silent():
    return cons.silent > 0


def tmp_silent():
    cons.tmp_silent = cons.tmp_silent + 1


def no_tmp_silent():
    cons.tmp_silent = cons.tmp_silent - 1


def is_tmp_silent():
    return cons.tmp_silent > 0


def alog(alog):
    if (alog):
        cons.alog = cons.alog + 1


def nalog(alog):
    if (alog):
        cons.alog = cons.alog - 1


def is_alog():
    return cons.alog > 0


def nawlog(alog):
    if (alog):
        cons.nawlog = cons.nawlog + 1


def awlog(alog):
    if (alog):
        cons.nawlog = cons.nawlog - 1


def is_nawlog():
    return cons.nawlog > 0


def log_tab(debug=False):
    if (debug):
        return cons.debug_log_tab
    else:
        return cons.log_tab


def set_log_tab(n, debug=False):
    if (debug):
        cons.debug_log_tab = s.get_repeat_string(" ", n)
    else:
        cons.log_tab = s.get_repeat_string(" ", n)


def view_log_tab(debug=False):
    if (debug):
        log("debug log tab: " + str(len(cons.debug_log_tab)))
    else:
        log("log tab: " + str(len(cons.log_tab)))


def clean_log_tab(debug=False):
    if (debug):
        cons.debug_log_tab = ""
    else:
        cons.log_tab = ""


def get_current_log_tab(debug=False):
    if (debug):
        return len(cons.debug_log_tab)
    else:
        return len(cons.log_tab)


def increase_log_tab(n, debug=False, all_=False):
    if (all_):
        increase_log_tab(n)
        increase_log_tab(n, debug=True)
    else:
        if (n > 0):
            n_ = get_current_log_tab(debug=debug)
            n_ += n
            set_log_tab(n_, debug=debug)


def decrease_log_tab(n, debug=False, all_=False):
    if (all_):
        decrease_log_tab(n)
        decrease_log_tab(n, debug=True)
    else:
        if (n > 0):
            n_ = get_current_log_tab(debug=debug)
            n_ -= n
            if (n_ < 0):
                n_ = 0
            set_log_tab(n_, debug=debug)


def silent_run(func, *args):
    try:
        tmp_silent()
        func(*args)
    finally:
        no_tmp_silent()

