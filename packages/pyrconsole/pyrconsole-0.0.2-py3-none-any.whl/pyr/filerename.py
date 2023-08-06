import ustring         as s
from   ulog            import log

import os

import ulog            as ulog
import ulist           as ulist
import cons            as cons
import filelistfind    as filelistfind
import fileedit        as fileedit
import env             as env
import fileio          as fileio
import tar             as tar
import ustring_ops     as ops
import ids             as ids


def translate(m):
    m00 = m
    m = rnlog(m)
    m = app_ext(m)
    m = fna(m)
    m = rename(m)
    m = rename_ids(m)
    m = w20(m)
    ulog.log_trans(m00, m)
    return m


def rnlog(m):
    if (m == "rnlog"):
        m = "rn " + m + " "
    return m


def app_ext(m):
    if (s.st(m, "appext ")):
        m = s.cf(m, "appext ")
        m = "rn al .{0} ".format(m)
    return m


def fna(m):
    if (s.ct(m, "fna ")):
        left = s.lf(m, "fna ")
        m = s.clf(m, "fna ")
        m = s.to_camel_words(m)
        m = s.cv(m, " ", "_")
        m = "filerename " + left + "rn al _" + m
    return m


def rename(m):
    if (is_rename(m)):
        m = "filerename " + m
    return m


def is_rename(m):
    return s.st(m, "rn ") or ids.is_ids(m, "rn")


def rename_ids(m):
    if (is_rename_ids(m)):
        m = "filerename " + m
    return m


def is_rename_ids(m):
    return ids.is_ids(m, "rn", ":")


def w20(m):
    if (m == "wild"):
        if (fileio.exists(tar.rp("home/wildfly_20"))):
            m = ".. ghome;l (wildfly);rn al _9[];l (wildfly_20);rn cl _20[];c;[log;l]"
        elif (fileio.exists(tar.rp("home/wildfly_9"))):
            m = ".. ghome;l (wildfly);rn al _20[];l (wildfly_9);rn cl _9[];c;[log;l]"
    return m


def handle(m):
    do_rename(m)


def do_rename(m):
    # rn a b
    # rn lf a
    # 1 2 3 rn a b
    # 123rn a b
    # 123: a
    # 1 2 3 : lf a
    # with_ext: "rn rnlog " 
    try:
        m = with_ext(m)
        files = filelistfind.list_files()
        files = get_rename_files(m, files)
        m = get_rename_condition(m)
        fileedit.set_replace_condition("r " + m)
        for file in files:
            do_rename_file(file)
        fileedit.reset_replace_condition()
        env.reset_list()
    finally:
        reset_with_ext()


def with_ext(m):
    if (s.has_p(m, "with_ext")):
        cons.rename_with_ext = True
        m = s.rm_p(m, "with_ext")
    elif (s.get_right_indent_size(m) == 1):
        cons.rename_with_ext = True
        m = s.trimright(m)
    return m


def reset_with_ext():
    cons.rename_with_ext = False


def get_rename_files(m, files):
    if (is_rename_ids(m)):
        files = ids.get_selected(files, m, "rn", ":")
    return files


def get_rename_condition(m):
    if (ids.is_ids(m, ":")):
        m = s.clf(m, ": ")
        op = s.lf(m, " ")
        if (not op in cons.ops):
            m = "use " + m
    else:
        m = s.clf(m, "rn ")
    return m


def do_rename_file(file):
    if (cons.rename_with_ext):
        file_name = fileio.get_file_name(file)
        to_file_name = fileedit.do_replace_line(file_name)
        if (file_name != to_file_name):
            file_parent = fileio.get_parent(file)
            from_file = file
            to_file = file_parent + s.sep(file_parent) + to_file_name
            os.rename(from_file, to_file)
            log("rename: " + from_file)
            log("     -> " + to_file)
    else:
        file_simple_name = fileio.get_file_simple_name(file)
        to_file_simple_name = fileedit.do_replace_line(file_simple_name)
        if (file_simple_name != to_file_simple_name):
            file_parent = fileio.get_parent(file)
            file_ext = fileio.get_file_ext(file)
            if (file_ext != ""):
                file_ext = "." + file_ext
            from_file = file
            to_file = file_parent + s.sep(file_parent) + to_file_simple_name + file_ext
            os.rename(from_file, to_file)
            log("rename: " + from_file)
            log("     -> " + to_file)


def move_sub_files_to(from_dir, to_dir):
    files = filelistfind.list_dir_(from_dir)
    for file in files:
        move_file_to(file, to_dir)


def move_file_to(file, to_dir):
    n = fileio.get_file_name(file)
    to_file = to_dir + s.sep(to_dir) + n
    from_file = file
    os.rename(from_file, to_file)

