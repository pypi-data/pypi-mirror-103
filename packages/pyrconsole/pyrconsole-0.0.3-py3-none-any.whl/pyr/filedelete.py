import ustring         as s
from   ulog            import log

import cons            as cons
import env             as env
import filego          as filego
import fileio          as fileio
import filelistfind    as filelistfind
import ids             as ids
import ulist           as l
import ulog            as ulog


def translate(m):
    m00 = m
    m = jd_clean(m)
    m = del_list(m)
    ulog.log_trans(m00, m)
    return m


def jd_clean(m):
    if (m == "jdclean"):
        m = ".. rm deployed[];rm dodeploy[];rm isdeploying[];rm failed[]"
    if (m == "jdcleanall"):
        m = "hrun gjd jdclean"
    return m


def del_list(m):
    if (not env.has_find_condition()):
        if (m == "-"):
            m = "filedelete " + m
        if (env.is_in_dir()):
            if (ids.is_ids(m, "-")):
                m = "filedelete " + m
            if (s.st(m, "rm ")):
                m = "filedelete " + m
    return m


def handle(m):
    if (m == "-" or ids.is_ids(m, "-")):
        do_del_list(m)
        if (m == "-"):
            env.reset_list()
    elif (s.st(m, "rm ")):
        do_del_list(m, s.cf(m, "rm "))


def do_del_list(m, filter_str=""):
    files = filelistfind.list_files()
    if (not filter_str == ""):
        files = list(filter(lambda x: s.isf(fileio.get_file_name(x), filter_str), files))
    if (ids.is_ids(m, "-")):
        files = ids.get_selected(files, m, "-")
    do_backup_del_list(files)
    for file in files:
        do_del_file(file)
    if (cons.del_callback):
        cons.del_callback(files)
    filego.reset_working_dir()


def do_backup_del_list(files):
    cons.file_system.do_backup_del_list(files)


def do_del_files(files):
    for file in files:
        do_del_file(file)


def do_del_file(file):
    if (fileio.exists(file)):
        if (fileio.is_file(file)):
            do_del_file_file(file)
        else:
            do_del_file_dir(file)
    file_dir = fileio.get_parent(file)
    file_name = fileio.get_file_name(file)
    log("delete from: {0}".format(file_dir))
    log("    1:    {0}".format(file_name))


def do_del_file_file(f):
    cons.file_system.do_del_file_file(f)


def do_del_file_file__(f):
    import os
    os.remove(f)


def do_del_file_dir(f):
    cons.file_system.do_del_file_dir(f)


def do_del_file_dir__(f):
    import shutil
    shutil.rmtree(path=f)

