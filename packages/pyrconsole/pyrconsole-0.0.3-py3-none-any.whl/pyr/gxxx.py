import ustring         as s
from   ulog            import log

import ulog            as ulog
import cons            as cons
import tar             as tar
import fileio          as fileio
import ulist           as ulist
import translate       as translate_
import ci              as ci

ops = {
    "b"   : "b ",
    "d"   : "d",
    "f"   : "f",
    "fue" : "fue",
    "ue"  : "fue",
    "gg"  : "gg",
    "m"   : "mq",
}


def translate(m):
    m00 = m
    m = gxxx_record(m)
    m = gxxx_(m)
    m = gxxx(m)
    ulog.log_trans(m00, m)
    return m


def gxxx_record(m):
    if (is_gxxx(m)):
        cons.gxxx = m
    elif (s.st(m, "g:") and not cons.gxxx == None):
        m = s.cf(m, "g:")
        if (m in ["fs", "f", "q"]):
            m = m + " " + ci.get_text()
        elif (ops.__contains__(m)):
            m = ops[m]
        m = ".. {0};;a;;{1}[]".format(cons.gxxx, m)
    return m


def gxxx_(m):  # no space
    if (not is_gxxx(m)):
        for op in ops.keys():
            if (s.end(m, op)):
                gxxx_op = s.cl(m, op)
                if (is_gxxx(gxxx_op)):
                    m = gxxx_op + " " + op
    return m


def gxxx(m):
    if (s.st(m, "g") and s.ct(m, " ")):
        gxxx_op = s.lf(m, " ")
        if (is_gxxx(gxxx_op)):
            cons.gxxx = gxxx_op
            m = do_gxxx(m)
    return m


def is_gxxx(k):
    return s.st(k, "g") and not s.ct(k, " ") and translate_.is_eis_key(k) and s.st(translate_.rp_eis(k), "g ", ".p ")


def do_gxxx(m):
    gxxx_op = s.lf(m, " ")
    m = s.clf(m, " ")
    if (s.ct(m, " ")):
        op = s.lf(m, " ")
        args = s.clf(m, " ")
        if (op in ["q", "f", "fs", "l", "li", "m", "mq", "r"]):
            m = ".. {0};;a;;{1} {2}[]".format(gxxx_op, to_op(op), args)
        else:
            m = ".. {0};;a;;{1} {2}[]".format(gxxx_op, "q", m)
    else:
        if (m in ops.keys()):
            m = ".. {0};;a;;{1}[]".format(gxxx_op, to_op(m))
        else:
            m = ".. {0};;a;;{1} {2}[]".format(gxxx_op, "q", m)
    return m


def to_op(op):
    if (ops.__contains__(op)):
        return ops[op]
    return op

