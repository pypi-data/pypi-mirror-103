import ustring         as s
from   ulog            import log
from   ulog            import logd

import cons            as cons
import env             as env
import filedelete      as filedelete
import fileio          as fileio
import filelistfind    as filelistfind
import fileopen        as fileopen
import ids             as ids
import tar             as tar
import ulist           as l
import ulist           as ulist
import ulog            as ulog


def translate(m):
    m00 = m
    m = auto(m)
    m = cc(m)
    m = dup_files(m)
    m = h123(m)
    ulog.log_trans(m00, m)
    return m


def auto(m):
    if (s.st(m, "cv ")):
        m = s.cv(m, "_auto_", ";a")
    return m


def cc(m):
    if (m == "cc"):
        m = "filecopy " + m
    elif (m == "cx"):
        m = "filecopy " + m
    elif (m == "ccc"):
        m = "filecopy " + m
    elif (m == "ccv"):
        m = "filecopy " + m
    elif (m == "cv"):
        m = "filecopy " + m
    elif (m == "cvnc"):
        m = "filecopy " + m
    elif (m == "cv ov"):
        m = "filecopy " + m
    elif (m == "cv ;a"):
        m = "filecopy " + m
    elif (m == "cv ;a ov" or m == "cv ov ;a"):
        m = "filecopy " + m
    elif (m == ":cv"):
        m = "filecopy " + m
    elif (ids.is_ids(m, "cc")):
        m = "filecopy " + m
    elif (ids.is_ids(m, "cx")):
        m = "filecopy " + m
    elif (s.st(m, "mv ")):
        m = "filecopy " + m
    elif (s.st(m, "get ")):
        m = "filecopy " + m
    elif (s.st(m, "put ")):
        m = "filecopy " + m
    return m


def dup_files(m):
    if (is_dup_files(m)):
        m = "filecopy " + m
    return m


def is_dup_files(m):
    return (m == "dup" or s.st(m, "dup ") or ids.is_ids(m, "dup")) and not fileopen.is_text_file(cons.p)


def h123(m):
    if (m == "hsync"):
        f = cons.p
        for k in ["h1", "h2", "h3"]:
            oi = tar.rp(k)
            if (s.st(f, oi)):
                in_h = k
        for k in ["h1", "h2", "h3"]:
            if (not k == in_h):
                oi = tar.rp(k)
                from_file = f
                to_file = s.cv(f, tar.rp(in_h), tar.rp(k))
                do_copy_file(from_file, to_file)
    return m


def handle(m):
    if (m == "cc"):
        cc_add()
        ccv()
    elif (m == "cx"):
        cc_add_x()
        ccv()
    elif (m == "ccc"):
        ccc()
        ccv()
    elif (m == "ccv"):
        ccv()
    elif (m == "cv"):
        cv()
        ccc()
    elif (m == "cvnc"):
        cv()
    elif (m == "cv ov"):
        cv(overwrite=True)
        ccc()
    elif (m == "cv ;a"):
        cv(auto_find=True)
        ccc()
    elif (m == "cv ;a ov" or m == "cv ov ;a"):
        cv(overwrite=True, auto_find=True)
        ccc()
    elif (m == ":cv"):  # cv and not clean cc
        cv()
    elif (ids.is_ids(m, "cc")):
        cc_add_select(m)
        ccv()
    elif (ids.is_ids(m, "cx")):
        cc_add_select_x(m)
        ccv()
    elif (is_dup_files(m)):
        do_dup_files(m)
        env.reset_list()  # reset list
    elif (s.st(m, "mv ")):
        do_move_files(m)
    elif (s.st(m, "get ")):
        do_get_files(m)
    elif (s.st(m, "put ")):
        do_put_files(m)


def cc_add():
    p = cons.p
    if (fileio.is_file(p)):
        files = [p]
    else:
        files = filelistfind.list_files()
    files = cons.file_system.enrich_cc(files)
    fileio.append_lines(cons.cc_dirs, files)


def cc_add_x():
    p = cons.p
    if (fileio.is_file(p)):
        files = [p]
    else:
        files = filelistfind.list_files()
    files = s.cv_(files, s.al, "(X)")
    files = cons.file_system.enrich_cc(files)
    fileio.append_lines(cons.cc_dirs, files)


def cc_add_select(m):
    files = filelistfind.list_files()
    files = ids.get_selected(files, m, "cc")
    files = cons.file_system.enrich_cc(files)
    fileio.append_lines(cons.cc_dirs, files)


def cc_add_select_x(m):
    files = filelistfind.list_files()
    files = ids.get_selected(files, m, "cx")
    files = list(map(lambda x: x + "(X)", files))
    files = cons.file_system.enrich_cc(files)
    fileio.append_lines(cons.cc_dirs, files)


def ccc():
    fileio.clean_file(cons.cc_dirs)


def ccv():
    files = fileio.l(cons.cc_dirs)
    ulog.logl("clipboard", files)


def cv(overwrite=False, auto_find=False):
    files = fileio.l(cons.cc_dirs)
    delete_files = ulist.filter_list(files, "(X)", s.end)
    files = list(map(lambda x: s.cl(x, "(X)"), files))
    copy_files_to_dir(files, cons.p, overwrite=overwrite, auto_find=auto_find)
    try:
        ulog.tmp_silent()
        for file in delete_files:
            filedelete.do_del_file(s.cl(file, "(X)"))
    finally:
        ulog.no_tmp_silent()


def do_dup_files(m):
    files = filelistfind.list_files()
    files = ids.get_selected(files, m, "dup")
    m = ids.rm_ids(m, "dup")
    for file in files:
        do_dup_one(m, file)


def do_dup_one(m, file):
    if (m == "dup"):
        n = fileio.get_file_simple_name(file)
        n2 = n + "_dup"
        do_dup_file(file, n, n2)
    elif (s.st(m, "dup ")):
        m = s.cf(m, "dup ")
        if (s.ct(m, " ")):  # dup xxx yyy
            do_dup_file(file, s.lf(m, " "), s.clf(m, " "))
        else:  # xxx
            do_dup_file(file, fileio.get_file_simple_name(file), m)


def do_dup_file(from_file, a, b):
    parent = fileio.get_parent(from_file)
    ext = fileio.get_file_ext(from_file)
    n = fileio.get_file_simple_name(from_file)
    n2 = s.cv(n, a, b)
    to_file = parent + s.sep(parent) + n2 + "." + ext
    do_copy_file(from_file, to_file)


def do_move_files(m):
    m = s.cf(m, "mv ")
    to_dir = cons.p
    if (s.ct(m, " ")):
        from_dir = tar.rp(s.lf(m, " "))
        list_condition = s.clf(m, " ")
    else:
        from_dir = tar.rp(m)
        list_condition = None
    files = filelistfind.list_dir_(from_dir, con=list_condition)
    copy_files_to_dir(files, to_dir)
    ulog.silent_run(filedelete.do_del_files, files)


def do_get_files(m):
    m = s.cf(m, "get ")
    to_dir = cons.p
    if (s.ct(m, " ")):
        from_dir = tar.rp(s.lf(m, " "))
        list_condition = s.clf(m, " ")
    else:
        from_dir = tar.rp(m)
        list_condition = None
    files = filelistfind.list_dir_(from_dir, con=list_condition)
    copy_files_to_dir(files, to_dir)


def do_put_files(m):
    m = s.cf(m, "put ")
    from_dir = cons.p
    if (s.ct(m, " ")):
        to_dir = tar.rp(s.lf(m, " "))
        list_condition = s.clf(m, " ")
    else:
        to_dir = tar.rp(m)
        list_condition = None
    files = filelistfind.list_dir_(from_dir, con=list_condition)
    copy_files_to_dir(files, to_dir)


def copy_files_to_dir(files, to, root=None, overwrite=False, auto_find=False):
    if (root == None):
        cons.cc_root = fileio.get_shared_root(files)
    else:
        cons.cc_root = root
    for file in files:
        copy_file_to_dir(file, to, overwrite=overwrite, auto_find=auto_find)
    if (cons.copy_callback):
        cons.copy_callback(files)


def copy_file_to_dir(file, to, overwrite=False, auto_find=False):
    if (auto_find):
        n = fileio.get_file_name(file)
        files = filelistfind.list_dir_(to, view_all=True, con=s.wrap(n, "()"))
        if (not files == None and len(files) > 0):
            if (len(files) == 1):
                to_file = files[0]
            else:
                to_file = ulist.select("file", files)
            do_copy_file(file, to_file, overwrite=overwrite)
    else:
        if (file == cons.cc_root):
            n = fileio.get_file_name(file)
        else:
            n = s.cf(file, cons.cc_root + s.sep(cons.cc_root))
        do_copy_file(file, to + s.sep(to) + n, overwrite=overwrite)


def do_copy_file(from_file, to_file, overwrite=False):
    if (not overwrite and fileio.exists(to_file)):
        from_ts = fileio.get_file_timestamp(from_file)
        to_ts = fileio.get_file_timestamp(to_file)
        if (to_ts + 10 >= from_ts):
            ulog.logtr("ignore same file: " + to_file)
            return
    
    log("copy from: {0}".format(fileio.get_parent(from_file)))
    log("     to:   {0}".format(fileio.get_parent(to_file)))
    log("     1:    {0}".format(fileio.get_file_name(from_file)))
    log("      ->   {0}".format(fileio.get_file_name(to_file)))
    cons.copy_files += to_file
    
    fileio.mkdir(fileio.get_parent(to_file))
    if (fileio.is_file(from_file)):
        do_copy_file_file(from_file, to_file)
    else:
        do_copy_file_dir(from_file, to_file)

    ts = fileio.get_file_timestamp(from_file)
    fileio.set_file_timestamp(to_file, ts)
    cons.mark_go_dir = to_file


def do_copy_file_file(from_file, to_file):
    cons.file_system.do_copy_file_file(from_file, to_file)


def do_copy_file_file__(from_file, to_file):
    import shutil
    shutil.copyfile(from_file, to_file)


def do_copy_file_dir(from_file, to_file):
    cons.file_system.do_copy_file_dir(from_file, to_file)


def do_copy_file_dir__(from_file, to_file):
    import shutil
    shutil.copytree(from_file, to_file, dirs_exist_ok=True)


def copy_files_in_dir(from_dir, to_dir, con=None):
    to_files = filelistfind.list_dir_(to_dir)
    to_file_names = s.cv_(to_files, fileio.get_file_name)
    from_files = filelistfind.list_dir_(from_dir)
    from_files = s._filter_(from_files, s.isf, con)
    from_files = s._filter_(from_files, lambda x: fileio.get_file_name(x) in to_file_names)
    copy_files_to_dir(from_files, to_dir)

