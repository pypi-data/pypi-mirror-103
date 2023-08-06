import ustring         as s
from   ulog            import log

import ulog            as ulog
import ulist           as ulist
import cons            as cons
import fileio          as fileio
import ms              as ms
import env             as env


def translate(m):
    m00 = m
    m = w(m)
    m = title(m)
    m = done(m)
    ulog.log_trans(m00, m)
    return m


def w(m):
    if (s.st(m, "w ")):
        m = s.cf(m, "w ")
        m = ".. ci {0};do[];c;v[]".format(m)
    elif (m == "wc"):
        m = ".. do_wc;[log;v]"
    elif (m == "do_wc"):
        m = "r [d];;"
    return m


def title(m):
    if (s.st(m, "ti ", "ti:")):
        m = ".. ci " + s.cf(m, "ti ", "ti:") + ";ti"
    return m


def done(m):
    if (s.st(m, "do ", "do:")):
        m = ".. ci " + s.cf(m, "do ", "do:") + ";do"
    return m


def handle(m):
    if (m == "touch"):
        touch(cons.p)
    elif (s.st(m, "lineop ")):
        m = s.cf(m, "lineop ")
        lineop(m)


def touch(p):
    fileio.set_file_timestamp(p, s.nowts_f())
    log("touch: " + p)


def lineop(m):
    if (m == "title"):
        do_title()
    elif (m == "done"):
        do_done()


def do_title():
    if (cons.found_files == None):
        return
    for p in cons.found_files:
        found_lines_p = cons.found_lines[p]
        lines = fileio.l(p)
        (line_number, line) = do_title_select(found_lines_p, lines)
        if (line != ""):
            lines.insert(line_number, cons.title_line)
            lines.insert(line_number - 1, cons.title_line)
            log(cons.title_line)
            log(line)
            log(cons.title_line)
            log()
            fileio.w(p, lines)
            cons.space_command = ".. c;{0}[]".format(str(line_number + 1))


def do_title_select(found_lines_p, p_lines):
    found_lines_p = list(filter(lambda x: is_titled(p_lines, x[0]), found_lines_p))
    if (len(found_lines_p) > 0):
        lines = list(map(lambda x: "[{0}] {1}".format(str(x[0]), x[1]), found_lines_p))
        line = ulist.select("title", lines)
        if (line != ""):
            return (int(s.c(line, "[", "]")), s.clf(line, " "))
    return (-1, "")


def is_titled(p_lines, line_number):
    line_number = line_number - 1
    if (0 < line_number < len(p_lines) - 1):
        if (p_lines[line_number - 1] == cons.title_line and p_lines[line_number + 1] == cons.title_line):
            return False
    return True


def do_done():
    if (cons.found_files == None):
        return
    for p in cons.found_files:
        found_lines_p = cons.found_lines[p]
        lines = fileio.l(p)
        (line_number, line) = do_done_select(found_lines_p, lines)
        line00 = line
        indent = s.get_indent(line)
        line = s.cf(line, indent)
        line_part = None
        if (s.st(line, "- ") and not s.st(line, "- [d]")):
            line_part = s.cf(line, "- ")
            line = indent + "- [d]" + line_part
            lines[line_number - 1] = line

        if (line00 != line):
            ulog.log_line_change(line00, line)
            log()
            fileio.w(p, lines)
            if (line_part):
                cons.space_command = ".. fs [d]{0};1[];c".format(line_part)


def do_done_select(found_lines_p, p_lines):
    found_lines_p = list(filter(lambda x: is_done(p_lines, x[0]), found_lines_p))
    if (len(found_lines_p) > 0):
        lines = list(map(lambda x: "[{0}] {1}".format(str(x[0]), x[1]), found_lines_p))
        line = ulist.select("done", lines)
        if (line != ""):
            return (int(s.c(line, "[", "]")), s.clf(line, " "))
    return (-1, "")


def is_done(p_lines, line_number):
    line_number = line_number - 1
    line = p_lines[line_number]
    return s.st(s.trim(line), "- ") and not s.st(s.trim(line), "- [d]")
