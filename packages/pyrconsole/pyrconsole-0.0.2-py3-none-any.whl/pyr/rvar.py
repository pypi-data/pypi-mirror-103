import ustring         as s
from   ulog            import log

import cons            as cons
import ulog            as ulog
import ms              as ms
import fileio          as fileio
import env             as env


def translate(m):
    m00 = m
    m = rvar(m)
    ulog.log_trans(m00, m)
    return m


def rvar(m):
    if (not ms.is_multi_step(m)):
        return do_rvar(m)
    return m


def do_rvar(m):
    m = do_rvar_constants(m)
    m = do_rvar_variables(m)
    return m


def do_rvar_constants(m):
    m = s.cv(m, "%p%", cons.p)
    m = s.cv(m, "%n%", fileio.get_file_name(cons.p))
    m = s.cv(m, "%sn%", fileio.get_file_simple_name(cons.p))
    m = s.cv(m, "%d%", fileio.get_parent(cons.p))
    m = s.cv(m, "%today%", s.today())  # 2019-10-01
    m = s.cv(m, "%today2%", s.today2())  # 20191001
    m = s.cv(m, "%today3%", s.today3())  # 1001
    m = s.cv(m, "%now%", s.now4())  # 1001
    if (env.has_find_condition()):
        m = s.cv(m, "%fl%", cons.find_condition)
        m = s.cv(m, "%fl_noprefix%", s.clf(cons.find_condition, " "))
    return m


def do_rvar_variables(m):
    if (s.n(m, "%") >= 2):
        for (k, v) in cons.r_variables.items():
            m = s.cv(m, s.wrap(k, "%"), v)
    return m


def handle(m):
    pass

