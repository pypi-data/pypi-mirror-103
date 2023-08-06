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
import filerename      as filerename


def translate(m):
    m00 = m
    m = z(m)
    m = x(m)
    ulog.log_trans(m00, m)
    return m


def z(m):
    for k in ["z", "jar", "war", "ear"]:
        if (m == k or ids.is_ids(m, k)):
            zip_(cons.p, m, ext=k)
            m = cons.ignore_cmd
    return m


def x(m):
    if (m == "x" or ids.is_ids(m, "x")):
        unzip_(cons.p, m)
        m = cons.ignore_cmd
    return m


def zip_(p, m="z", ext="zip"):
    files = filelistfind.list_files()
    do_zip(files, p, m, ext)


def do_zip(files, p="", m="z", ext="zip"):
    if (isinstance(files, str)):
        p = fileio.get_parent(files)
        files = [files]
    k = ext
    if (ids.is_ids(m, k)):
        files = ids.get_selected(files, m, k)
    if (fileio.is_file(p)):
        p = fileio.get_parent(p)
    if (len(files) == 1):
        file = files[0]
        if (fileio.is_file(file)):
            n = fileio.get_file_name(p)
        else:
            n = fileio.get_file_name(file)
    else:
        n = fileio.get_file_name(p)
    option = "-cf"
    if (ext == "z"):
        ext = "zip"
        option = "-cMf"
    n += ("." + ext)
    f = p + s.sep(p) + n
    items = s.cv_(files, lambda x: s.wrap(fileio.get_file_name(x)))
    items = s.conn(items, " ")
    jar_cmd = "jar {0} \"{1}\" {2}".format(option, n, items)
    filelistfind.cd(p)
    run.r(jar_cmd)
    log("zipping: " + f)
    cons.mark_go_dir = f


def unzip_(p, m="x"):  # @UnusedVariable
    files = filelistfind.list_files()
    do_unzip(files, p, m)


def do_unzip(files, p="", m="x"):  # @UnusedVariable
    if (isinstance(files, str)):
        p = fileio.get_parent(files)
        files = [files]
    if (ids.is_ids(m, "x")):
        files = ids.get_selected(files, m, "x")
    for file in files:
        parent = fileio.get_parent(file)
        unzip_to_dir = parent + s.sep(parent) + fileio.get_file_simple_name(file)
        fileio.mkdir(unzip_to_dir)
        to_file = unzip_to_dir + s.sep(unzip_to_dir) + fileio.get_file_name(file)
        try:
            ulog.tmp_silent()
            filecopy.do_copy_file(file, to_file)
        finally:
            ulog.no_tmp_silent()
        option = "-xvf"
        n = fileio.get_file_name(file)
        jar_cmd = "jar {0} \"{1}\"".format(option, n)
        filelistfind.cd(unzip_to_dir)
        run.r(jar_cmd)
        fileio.mkdir(p)
        filelistfind.cd(p)
        log("unzipping: " + file)
        cons.mark_go_dir = unzip_to_dir
        try:
            ulog.tmp_silent()
            filedelete.do_del_file(to_file)
            move_to_parent(unzip_to_dir)
        finally:
            ulog.no_tmp_silent()


def move_to_parent(unzip_to_dir):
    n0 = fileio.get_file_name(unzip_to_dir)
    files = filelistfind.list_dir_(unzip_to_dir)
    if (len(files) == 1):
        file = files[0]
        n = fileio.get_file_name(file)
        if (n0 == n):
            from_file = file
            to_file = unzip_to_dir
            filerename.move_sub_files_to(from_file, to_file)
            filedelete.do_del_file(from_file)

