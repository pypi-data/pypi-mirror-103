import ustring         as s
from   ulog            import log

import ulog            as ulog
import cons            as cons


def translate(m):
    m00 = m
    m = quick_cmds(m)
    m = complex_cmds(m)
    m = cmds(m)
    m = next_(m)
    m = prev_(m)
    ulog.log_trans(m00, m)
    return m


def quick_cmds(m):
    if (cons.quick_cmds.__contains__(m)):
        m = cons.quick_cmds[m]
    for k in cons.quick_cmds_st.keys():
        if (s.st(m, k)):
            args = s.cf(m, k)
            m = cons.quick_cmds_st[k]
            m = s.cv(m, "xxx", args)
    return m


def complex_cmds(m):
    import cmds_complex
    return cmds_complex.translate(m)


def cmds(m):
    if (cons.cmds.__contains__(m)):
        m = cons.cmds[m]
    return m


def next_(m):
    if (m == "ncmd"):
        import re
        k = re.search("\\d+", cons.next_prev_cmd).group()
        k2 = str(int(k) + 1)
        cons.next_prev_cmd = s.cv(cons.next_prev_cmd, k, k2)
        m = cons.next_prev_cmd
    return m


def prev_(m):
    if (m == "pcmd"):
        import re
        k = re.search("\\d+", cons.next_prev_cmd).group()
        if (not k == "1"):
            k2 = str(int(k) - 1)
            cons.next_prev_cmd = s.cv(cons.next_prev_cmd, k, k2)
        m = cons.next_prev_cmd
    return m


def record_next_prev_cmd(m):
    if (m == "ncmd" or m == "pcmd"):
        if (cons.next_prev_cmd == None):
            cons.next_prev_cmd = cons.last_command
    return m


def put(k, v):
    cons.cmds[k] = v


def get(k):
    return cons.cmds[k]


def rm(k):
    cons.cmds.pop(k)

