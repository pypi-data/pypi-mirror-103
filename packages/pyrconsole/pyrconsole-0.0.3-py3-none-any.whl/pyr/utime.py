import ustring         as s
from   ulog            import log

import cons            as cons
import ulog            as ulog
import run             as run
import env             as env
import ids             as ids
import filelistfind    as filelistfind
import fileio          as fileio
import filecopy        as filecopy
import filedelete      as filedelete


def translate(m):
    m00 = m
    m = now(m)
    m = ms_to_time(m)
    m = time_to_ts(m)
    ulog.log_trans(m00, m)
    return m


def now(m):
    if (m == "now"):
        ts = s.now4()
        log(ts)
        cons.cal_result = ts
        m = cons.ignore_cmd
    elif (m == "nowts"):
        ts = str(s.nowts())
        log(ts)
        cons.cal_result = ts
        m = cons.ignore_cmd
    return m


def ms_to_time(m):
    if (s.is_number(m) and len(m) == 13 and m[0] == "1"):
        ts = do_ms_to_time(m)
        log(ts)
        cons.cal_result = ts
        m = cons.ignore_cmd
    return m


def do_ms_to_time(m, format_="%Y-%m-%d %H:%M:%S"):
    ts = float(m) / 1000
    import time
    ts = time.strftime(format_, time.localtime(ts))
    ts = str(ts)
    return ts


def time_to_ts(m):
    if (len(m) == 19 and s.match(m, "\\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d:\\d\\d:\\d\\d")):
        import time
        ts = time.strptime(m, '%Y-%m-%d %H:%M:%S')
        ts = time.mktime(ts)
        ts = str(int(round(ts * 1000)))
        log(ts)
        cons.cal_result = ts
        m = cons.ignore_cmd
    return m
