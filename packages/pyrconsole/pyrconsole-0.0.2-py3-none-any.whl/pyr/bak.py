import ustring         as s
from   ulog            import log

import cons            as cons
import ulog            as ulog


def translate(m):
    m00 = m
    m = bak_pyr(m)
    ulog.log_trans(m00, m)
    return m


def bak_pyr(m):
    if (m == "kg"):
        m = "bak kg"
    return m


def handle(m):
    if (m == "kg"):
        kg()


def kg():
    do_bak_pyr()


def do_bak_pyr():
    log("TODO")

