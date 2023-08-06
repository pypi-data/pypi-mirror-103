import ustring         as s
from   ulog            import log

import os

import cons            as cons
import env             as env
import fileio          as fileio
import filelistfind    as filelistfind
import ids             as ids
import keyboard        as keyboard
import ulist           as ulist
import ulog            as ulog

eclipse       = "D:\\soft\\eclipse\\eclipse\\eclipse.exe"
ultraedit_dir = "C:\\Program Files (x86)\\IDM Computer Solutions\\UltraEdit"
ultraedit     = "Uedit32.exe"
explorer      = "explorer"


def translate(m):
    m00 = m
    m = fileopen_f(m)
    m = fileopen_find(m)
    m = fileopen_file(m)
    m = fileopen_line(m)
    m = fileopen_python_ex(m)
    ulog.log_trans(m00, m)
    return m


def fileopen_f(m):
    if (m == "f"):
        m = "fileopen f"
    return m


def fileopen_find(m):
    if (env.has_found_files() and (s.match(m, "\\d", "\\d\\d", "\\d\\d\\d", "\\d\\d\\d\\d") or m == "gl")):
        if (m == "gl"):
            if (fileio.is_file(cons.p)):
                m = str(len(cons.found_lines[cons.p]))
            else:
                m = str(len(cons.found_lines)) + "01"
        m = "fileopen " + m
    return m


def fileopen_file(m):
    if ((ids.is_pure_ids(m)) and not env.has_found_files() and fileio.is_dir(cons.p)):
        m = "fileopen " + m
    return m


def fileopen_line(m):
    if ((s.is_number(m) or m == "gl") and not env.has_found_files() and fileio.is_file(cons.p)):
        if (m == "gl"):
            m = str(fileio.get_file_count(cons.p))
        m = "fileopen " + m
    return m


def fileopen_python_ex(m):
    if (is_fileopen_python_ex(m)):
        m = "fileopen " + m
    return m


def is_fileopen_python_ex(m):
    m = s.trim(m)
    return s.st(m, "File ") and s.ct(m, ".py\", line")


def handle(m):
    if (m == "f"):
        do_fileopen_f(m)
    elif (env.has_found_files() and s.match(m, "\\d", "\\d\\d", "\\d\\d\\d", "\\d\\d\\d\\d")):
        do_fileopen_find(m)
    elif ((ids.is_pure_ids(m)) and not env.has_found_files() and fileio.is_dir(cons.p)):
        do_fileopen_file(cons.p, m)
    elif (s.is_number(m) and not env.has_found_files() and fileio.is_file(cons.p)):
        do_fileopen_line(cons.p, m)
    elif (is_fileopen_python_ex(m)):
        do_fileopen_python_ex(m)


def do_fileopen_f(m):  # @UnusedVariable
    open_file(cons.p)
    filelistfind.cd(cons.p)


def do_fileopen_find(m):
    if (len(cons.found_files) == 1):
        found_file_index = 0
        found_line_index = int(m) - 1
    else:
        if (s.match(m, "\\d")):
            found_file_index = int(m) - 1
            found_line_index = 0
        if (s.match(m, "\\d\\d")):
            found_file_index = int(m[0]) - 1
            found_line_index = int(m[1]) - 1
        if (s.match(m, "\\d\\d\\d")):
            found_file_index = int(m[0]) - 1
            found_line_index = int(m[1:3]) - 1
        if (s.match(m, "\\d\\d\\d\\d")):
            found_file_index = int(m[0:2]) - 1
            found_line_index = int(m[2:4]) - 1
    do_fileopen_find_open_line(found_file_index, found_line_index)


def do_fileopen_find_open_line(found_file_index, found_line_index):
    found_file = cons.found_files[found_file_index]
    try:
        ulog.tmp_silent()
        open_file(found_file)
    finally:
        ulog.no_tmp_silent()
    (line_number, line) = cons.found_lines[found_file][found_line_index]
    row = line_number
    col, chinese_characters = s.find_position(line, s.lf(cons.find_condition_key, " "))
    keyboard.go_line(found_file, row, col, chinese_characters=chinese_characters)
    log("open line \"{0},{1}\" in file: \"{2}\".".format(row, col, found_file))


def do_fileopen_file(p, m):
    indexes = ids.get_pure_ids(m)
    files = filelistfind.list_dir(p, cons.view_all)
    files_count = len(files)
    for index in indexes:
        if (0 <= index <= files_count):
            to_open_file = files[index]
            open_file(to_open_file)
        else:
            log("ERROR: No file with id \"{0}\". File Count is \"{1}\".".format(str(index + 1), str(files_count)))


def do_fileopen_line(p, m):
    try:
        ulog.tmp_silent()
        open_file(p)
    finally:
        ulog.no_tmp_silent()
    row = int(m)
    if (row < 1):
        row = 1
    file_count = fileio.get_file_count(p)
    if (row > file_count):
        row = file_count
    try:
        line = fileio.get_file_line(p, row)
        col = s.get_indent_size(line)
    except:
        col = 0
    keyboard.go_line(p, row, col)
    log("open line \"{0},{1}\" in file: \"{2}\".".format(row, col, p))


def do_fileopen_python_ex(m):
    p = s.c(m, "\"", "\"")
    line_number = s.c(m, "line ", ",")
    do_fileopen_line(p, str(line_number))


def is_eclipse_file(f):
    l = [
        ".java",
        ".py",
        ".xml",
        ".xsd",
        ".xsl",
        ".wsdl",
        ".properties",
        ".js",
        ".jsp",
        ".json",
        ".css"
    ]
    for ext in l:
        if (s.end(f, ext)):
            return True
    return False


def open_eclipse(f):
    cmd = "call {0} \"{1}\"".format(eclipse, f)
    os.system(cmd)
    log("open file: " + f)


def open_explorer(f):
    cmd = "call {0} \"{1}\"".format(explorer, f)
    os.system(cmd)
    log("open file: " + f)


def is_ultraedit_file(f):
    l = [".txt",
         ".csv",
         ".log",
         ".sql",
         ".lst",
         ".java",
         ".c",
         ".cpp",
         ".h",
         ".as",
         ".scala",
         ".r",
         ".xml",
         ".xsd",
         ".xsl",
         ".html",
         ".css",
         ".wsdl",
         ".js",
         ".jsp",
         ".json",
         ".ini",
         ".bat",
         ".cmd",
         ".sh",
         ".properties",
         ".conf",
         ".diff",
         ".patch",
         ".classpath",
         ".project",
         ".module",
         ".component",
         ".md",
         ".mf",
         ".vm",
         ".userlibraries",
         ".stg",
         ".part-00000",
         ".clj",
         ".py",
         ".bashrc",
         ".vli",
         ".cnf",
         ".cfg",
         ".out",
         ".jboss",
         ".was",
         ".weblogic",
         ".err",
         ".service",
         ".repo",
         "hosts",
         "messages",
         "iptables",
         "LICENSE",
         "stdout",
         "stderr",
         "_cut",
         "_errors",
         "simu",
         ]
    # is ultraedit file
    for ext in l:
        if (s.end(f, ext)):
            return True
    return False


def open_ultraedit(f):
    os.chdir(ultraedit_dir)
    cmd = "call {0} \"{1}\"".format(ultraedit, f)
    os.system(cmd)
    log("open file: " + f)


def open_file(f):
    cons.file_system.open_file(f)


def open_file__(f):
    if (is_eclipse_file(f)):
        open_eclipse(f)
    elif (is_ultraedit_file(f)):
        open_ultraedit(f)
    else:
        open_explorer(f)


def is_text_file(p):
    return cons.file_system.is_text_file(p)


def is_text_file__(p):
    return (is_eclipse_file(p) or is_ultraedit_file(p)) and fileio.is_file(p)

