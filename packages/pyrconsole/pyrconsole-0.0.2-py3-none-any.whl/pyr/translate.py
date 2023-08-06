import ustring         as s
from   ulog            import log
from   ulog            import logd

import ulog            as ulog
import tar             as tar
import fileio          as fileio
import cons            as cons
import openweb         as openweb

eis_file = cons.bat_dir   + "\\eis.bat"
co_file  = cons.alogs_dir + "\\set\\common.txt"
est_file = cons.bat_dir   + "\\est.bat"
rf_file  = cons.bat_dir   + "\\rss.bat"


def translate(m):
    if (exclude_trans(m)):
        return m

    m00 = m
    m = eis(m)
    if (not m00 == m):
        return m

    m00 = m
    m = co(m)
    if (not m00 == m):
        return m

    m00 = m
    m = before_est(m)
    if (not m00 == m):
        return m

    m00 = m
    m = est(m)
    if (not m00 == m):
        return m

    m00 = m
    m = rf(m)
    if (not m00 == m):
        return m

    m00 = m
    m = bat(m)
    if (not m00 == m):
        return m
    return m


def exclude_trans(m):
    if (m == cons.ignore_cmd):
        return True
    if (s.st(m, "cal ")):
        return True


def eis(m):
    m00 = m
    if (m == "r"):
        m = "g .."
        ulog.log_trans(m00, m)
        return m
    if (m == "g"):
        m = "g 1"
        ulog.log_trans(m00, m)
        return m

    eisMap = get_eis_map()
    while (eisMap.__contains__(m)):
        m00 = m
        m = eisMap.get(m)
        ulog.log_trans(m00, m)

    return m


def co(m):
    m00 = m

    coMap = get_co_map()
    while (coMap.__contains__(m)):
        m00 = m
        m = coMap.get(m)
        ulog.log_trans(m00, m)

    return m


def before_est(m):
    m = openweb.web_tar_0(m)
    return m


def est(m):
    m00 = m

    key = get_est_key(m)
    if (is_excluded_key(key)):
        return m

    if (s.st(m, "h ")):
        m = s.cf(m, "h ")
        return "hdfs downaws " + m
    if (s.st(m, "xm ")):
        m = s.cf(m, "xm ")
        return "xiaomi " + m

    estMap = get_est_map()
    matchedKeys = []
    for es in estMap.keys():
        if (s.st(m, es)):
            matchedKeys.append(es)

    if (len(matchedKeys) > 0):
        matchedKey = s.max_len_(matchedKeys)
        args = s.cf(m, matchedKey)
        if (s.nnl(args)):
            v = estMap.get(matchedKey)
            v = s.rm(v, ":noSpace", "::isChinese", ":notNumber")
            try:
                m = s.format_str(v, *s.get_parts(args, v, keys=[" "]))
            except ValueError as ve:
                logd("Cannot format: \"{0}\". Args is: \"{1}\". Reason is: \"{2}\"".format(v, args, ve))
                pass
            except IndexError as ie:
                logd("Cannot format: \"{0}\". Args is: \"{1}\". Reason is: \"{2}\"".format(v, args, ie))
                pass

    ulog.log_trans(m00, m)
    return m


def rf(m):
    m00 = m
    rfMap = get_rf_map()
    if (rfMap.__contains__(m)):
        m = rfMap.get(m)

    ulog.log_trans(m00, m)
    return m


def bat(m):
    m00 = m
    b = cons.bat_dir + s.sep(cons.bat_dir) + m + ".bat"
    import os
    if (os.path.exists(b)):
        lines = fileio.l(b)
        lines = list(filter(lambda x: s.ct(x, "--fa"), lines))
        if (len(lines) > 0):
            n = lines[0]
            n = s.cf(n, "call l ")
            n = s.lf(n, ";eq")
            to_dir = tar.rp(s.lf(n, " "))
            to_fn = s.clf(n, " ")
            import glob
            files = glob.glob(to_dir + '/**/' + to_fn, recursive=True)
            to = files[0]
            m = "g " + to

    ulog.log_trans(m00, m)
    return m


def get_eis_map():
    if (cons.eis_map == None):
        lines = fileio.l(eis_file)
        lines = list(filter(lambda x: s.ct(x, "=") and (not s.ct(x, "(") or (s.end(x, ")") and not s.ct(x, ":"))), lines))

        rmap = dict()
        for line in lines:
            line = s.cl(line, "\n")
            key = s.lf(line, "=")
            value = s.clf(line, "=")
            if (not rmap.__contains__(key)):
                rmap[key] = value

        cons.eis_map = rmap

    return cons.eis_map


def get_co_map():
    if (cons.co_map == None):
        lines = fileio.l(co_file)
        lines = list(filter(lambda x: s.ct(x, "=="), lines))

        rmap = dict()
        for line in lines:
            line = s.cl(line, "\n")
            key = s.trim(s.lf(line, "=="))
            value = s.trim(s.lf(s.clf(line, "=="), "//"))
            if (not rmap.__contains__(key)):
                rmap[key] = value

        cons.co_map = rmap

    return cons.co_map


def get_est_map():
    if (cons.est_map == None):
        lines = fileio.l(est_file)
        lines = list(filter(lambda x: s.ct(x, "=") and s.nend(x, "[R]"), lines))

        rmap = dict()
        for line in lines:
            line = s.cl(line, "\n")
            line = s.cl(line, "[Python]")
            key = s.lf(line, "=")
            value = s.clf(line, "=")
            if (not rmap.__contains__(key)):
                rmap[key] = value

        cons.est_map = rmap

    return cons.est_map


def get_rf_map():
    if (cons.rf_map == None):
        lines = fileio.l(rf_file)
        lines = list(filter(lambda x: ((not s.ct(x, "(") and not s.ct(x, "%")) or s.ct(x, "(noArgs)")), lines))

        rmap = dict()
        for line in lines:
            line = s.cl(line, "\n")
            line = s.trim(line)
            key = s.lf(line, ":")
            value = s.c(line, "\"", "\"")
            if (not rmap.__contains__(key)):
                rmap[key] = value

        cons.rf_map = rmap

    return cons.rf_map


def is_excluded_key(key):
    not_excluded_key = ["nl", "li", "ai", "rt", "crt"]
    if (key in not_excluded_key):
        return False

    reserved_keys = ["run", "buildCurrentDir"]
    if (key in reserved_keys):
        return True

    rf = get_rf_map()
    if (rf.__contains__(key)):
        return True

    return False


def to_args_list(v, args):
    if (s.ct(v, "{1}")):
        return args.split(" ")
    else:
        return [args]


def get_est_key(m):
    if (s.st(m, " ")):
        left_indent = s.get_left_indent(m)
        m = s.trim(m)
        key = s.lf(m, " ")
        return left_indent + key
    return s.lf(m, " ")


def is_eis_key(m):
    eis = get_eis_map()
    if (eis.__contains__(m)):
        return True
    return False


def rp_eis(m):
    eis = get_eis_map()
    if (eis.__contains__(m)):
        return eis.get(m)
    return m

