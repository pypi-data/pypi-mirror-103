import ustring         as s
from   ulog            import log


def is_multi_step(m):
    return is_ms(m) or is_ms_silent(m)


def is_ms_silent(m):
    return s.st(m, ".. ", "ms silent ")


def is_ms(m):
    return s.st(m, ". ", "ms ")


def rm_ms(m):
    return s.cf(m, ". ", ".. ", "ms silent ", "ms ")


def is_alog(m):
    return (s.st(m, "[") or s.end(m, "[]")) and not is_nawlog(m)


def is_nalog(m):
    return s.end(m, "]") and not s.end(m, "\\]") and not is_awlog(m)


def is_awlog(m):
    return s.end(m, "]]")


def is_nawlog(m):
    return s.st(m, "[[")


def get_increase_logtab(m):
    n = 0
    while (s.st(m, "{")):
        n += 4
        m = s.cf(m, "{")
    return m, n


def get_decrease_logtab(m):
    n = 0
    while (s.end(m, "}")):
        n += 4
        m = s.cl(m, "}")
    return m, n


def rm_logtab_marks(m):
    m = s.cf(m, "{")
    m = s.cl(m, "}")
    return m


def rm_log_marks(m):
    m = s.cv(m, "\\]", "_]_")
    m = s.cf(m, "[[")
    m = s.cf(m, "[")
    m = s.cl(m, "[]")
    m = s.cl(m, "]]")
    m = s.cl(m, "]")
    m = s.cv(m, "_]_", "]")
    return m


def log_step(cmd):
    log()
    log("next step: " + cmd)
    log()

