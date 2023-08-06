import ustring         as s
from   ulog            import log
from   ulog            import logc
from   ulog            import logt

import cons            as cons
import fileio          as fileio
import filego          as filego
import ulog            as ulog
import filelistfind    as filelistfind
import fileopen        as fileopen
import ulist           as l
import env             as env
import ids             as ids
import ulist           as ulist
import ustring_ops     as ops


def translate(m):
    m00 = m
    m = bat(m)
    m = count_size(m)
    ulog.log_trans(m00, m)
    return m


def bat(m):
    if (is_bat(m)):
        m = "fileview " + m
    return m


def is_bat(m):
    return s.st(m, "v ")


def count_size(m):
    if (is_count_size(m)):
        m = "fileview " + m
    return m


def is_count_size(m):
    return m in ["as", "as "]  # all size


def handle(m):
    if (is_bat(m)):
        do_bat(m)
    elif (is_count_size(m)):
        do_count_size(m)


def do_bat(m):
    m = s.cf(m, "v ")
    bat_file = cons.bat_dir + s.sep(cons.bat_dir) + m + ".bat"
    if (fileio.exists(bat_file)):
        log("view: " + bat_file)
        log()
        lines = fileio.l(bat_file)
        logt(4, lines)
        log()
    else:
        log("file not found: " + bat_file)


def do_count_size(m):  # @UnusedVariable
    if (m == "as "):
        files = filelistfind.list_files()
    else:
        files = filelistfind.list_all_files()
    size = 0
    for file in files:
        if (fileio.is_file(file)):
            size += fileio.get_file_size(file)
    size_s = fileio.format_file_size(size)
    log("total: " + size_s)

