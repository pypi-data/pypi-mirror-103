import ustring         as s
from   ulog            import log
from   ulog            import logd
from   ulog            import logp

import os

import cons            as cons
import env             as env
import fileio          as fileio
import fileopen        as fileopen
import ids             as ids
import tar             as tar
import ulist           as l
import ulog            as ulog
import ulog_format     as ulog_format


def translate(m):
    m00 = m
    m = pick_found_lines(m)
    m = with_without(m)
    m = list_operations(m)
    m = explorer_file(m)
    m = build_current_dir(m)
    ulog.log_trans(m00, m)
    return m


def with_without(m):
    for k in ["and", "or", "not", "is", "st", "end"]:
        if (s.st(m, k + " ")):
            m = s.cf(m, k + " ")
            if (k == "and"):
                pass
            elif (k == "is"):
                m = s.wrap(m, "()")
            else:
                m = s.wrap(m, k + "()")
            m = "/" + m
    if (s.st(m, "/")):
        m = s.cf(m, "/")
        m = "bh" + m
    if (s.st(m, "\\")):
        m = s.cf(m, "\\")
        m = "by" + m
    return m


def list_operations(m):
    if (m == "l"):
        m = "filelistfind " + m
    elif (m == "v"):
        m = "filelistfind " + m
    elif (m == "o" or s.st(m, "o=")):
        m = "filelistfind " + m
    elif (m == "a"):
        m = "filelistfind " + m
    elif (s.match(m, "a\\d")):
        m = "filelistfind " + m
    elif (m == "va"):
        m = "filelistfind " + m
    elif (m == "ls"):
        m = "filelistfind " + m
    elif (is_multiple_lines(m)):
        m = "filelistfind " + m
    elif (m == "mq" or s.st(m, "mq ")):
        m = "filelistfind " + m
    elif (s.st(m, "l ")):
        m = "filelistfind " + m
    elif (s.st(m, "q ", "f ", "fs ")):
        m = "filelistfind " + m
    elif (s.st(m, "bh", "by")):
        m = "filelistfind " + m
    elif (s.is_wrapped(m, "and()", "or()", "not()")):
        m = "filelistfind " + m
    elif (is_list_filter(m)):
        m = "filelistfind list_filter " + m
    return m


def explorer_file(m):
    if (m == "d"):
        return to_explorer_file(cons.p)
    elif (ids.is_ids(m, "d")):
        files = list_files()
        p = ids.get_selected(files, m, "d")[0]
        return to_explorer_file(p)
    return m


def to_explorer_file(p):
    if (os.path.isdir(p)):
        m = "run call explorer " + p
        log("open dir: " + p)
    else:
        m = "run call explorer /e,/select,\"{0}\"".format(p)
        log("open file: " + p)
    return m


def build_current_dir(m):
    if (s.iss(m, "b .", "buildCurrentDir")):
        m = "run ant"
    return m


def pick_found_lines(m):
    if (env.has_find_condition()):
        if (s.st(m, "pick")):
            if (s.st(m, "pick ")):
                m = s.cf(m, "pick ") + " key"
            else:
                m = s.cf(m, "pick") + "key"
            l = cons.found_lines[cons.p]
            l = s.cv_(l, lambda x:x[0])
            m = ids.get_selected(l, m, "key")
            cons.find_condition_picked = m
            m = "v"
        elif (m == "nopick"):
            cons.find_condition_picked = []
            m = "v"
    return m


def is_multiple_lines(m):
    return m in ["ml", "mlw", "mls", "noml"]


def handle(m):
    if (m == "l"):
        view(cons.p)
    elif (m == "v"):
        view(cons.p)
    elif (m == "o" or s.st(m, "o=")):
        do_o(m)
    elif (m == "a"):
        cons.view_all = True
        view(cons.p)
    elif (s.match(m, "a\\d")):
        cons.view_all = True
        cons.list_level = s.cf(m, "a")
        view(cons.p)
    elif (m == "va"):
        do_va()
    elif (m == "ls"):
        cons.view_all = False
        view(cons.p)
    elif (is_multiple_lines(m)):
        cons.find_condition_multiple_lines = to_ml(m)
        view(cons.p)
    elif (m == "mq" or s.st(m, "mq ")):
        do_mq(m)
    elif (s.st(m, "l ")):
        do_l(m)
    elif (s.st(m, "q ", "f ", "fs ")):
        do_q(m)
    elif (s.st(m, "bh", "by")):
        do_bh(m)
    elif (s.is_wrapped(m, "and()", "or()", "not()")):
        add_additional_key(m)
        view(cons.p)
    elif (s.st(m, "list_filter ")):
        cons.list_filter = s.cf(m, "list_filter ")
        view(cons.p)


def no_translate(m):  # @UnusedVariable
    # if (is_list_filter(m)):
    #     return True
    return False


def do_o(m):
    cons.output_file = do_o_file(m)
    fileio.clean_file(cons.output_file)
    do_va()
    print("output find logs to: " + cons.output_file)
    try:
        ulog.tmp_silent()
        fileopen.open_file(cons.output_file)
    finally:
        ulog.no_tmp_silent()
    cons.output_file = None


def do_o_file(m):
    if (s.st(m, "o=")):
        m = s.cf(m, "o=")
        m = s.cv(m, "/", s.sep())
        if (not s.ct(m, s.sep())):
            m = "gtm" + s.sep() + m
        dir_ = s.lf(m, s.sep())
        path_ = s.clf(m, s.sep())
        import translate as translate
        dir_ = translate.rp_eis(dir_)
        if (s.st(dir_, "g ")):
            dir_ = s.cf(dir_, "g ")
        dir_ = tar.rp(dir_)
        return dir_ + s.sep(dir_) + path_
    else:
        return cons.default_output_file


def do_va():
    if (env.has_find_condition() or env.is_in_file()):
        cons.view_all = True
    cons.list_max = -1
    view(cons.p)


def do_mq(m):
    if (s.st(m, "mq ")):
        m = "q " + s.cf(m, "mq ")
        cons.find_condition = m
        cons.find_condition_key = s.clf(m, " ")
    method_find_key = get_method_find_key()
    if (not s.end(cons.find_condition, " " + method_find_key)):
        cons.find_condition = cons.find_condition + " " + method_find_key
        cons.find_condition_key = s.clf(cons.find_condition, " ")
    view(cons.p)


def do_l(m):
    m = resolve_shortcuts(m)
    cons.list_condition = s.cf(m, "l ")
    cons.list_filter = None
    view(cons.p)


def do_q(m):
    m = resolve_shortcuts(m)
    cons.find_condition = m
    cons.find_condition_key = s.clf(m, " ")
    view(cons.p)


def do_bh(m):
    if(s.st(m, "bh")):
        m = s.cf(m, "bh")
        if (s.st(cons.find_condition, "fs ")):
            m = s.wrap(m, "and()")
    else:
        m = s.cf(m, "by")
        m = s.wrap(m, "not()")
    add_additional_key(m)
    view(cons.p)


def view(p):
    if (fileio.is_dir(p)):
        dir_view(p)
    else:
        cons.found_file_root = None
        cons.found_files = None
        cons.found_lines = None
        file_view(p)


def dir_view(p):
    if (env.has_find_condition()):
        dir_view_find(p)
    else:
        dir_view_list(p)


def dir_view_find(p):
    ulog.logc("find from: {0} ({1})".format(p, cons.find_condition))

    files = list_dir(p, cons.view_all)
    count = len(files)

    if (count == 0):
        log("    no matched files: " + cons.list_condition)
        cons.list_condition = None
    else:
        cons.found_file_index = 0
        cons.found_file_root = p
        cons.found_files = None
        cons.found_lines = None
        for full_path in files:
            file_view(full_path)

    if (cons.has_log_cache):  # not found any lines
        ulog.clean_log_cache()
        log("not found any lines: {0}".format(cons.find_condition))
        cons.find_condition = None


def dir_view_list(p):
    log("list from: " + p + ulog.list_filter_log_str())
    files = list_dir(p, cons.view_all, get_list_max())
    count = len(files)
    if (count == 0):
        log("    no matched files: " + s.as_str(cons.list_condition))
        cons.list_condition = None
    else:
        i = 0
        file_lengths = list(map(lambda fp: s.get_length(s.cf(fp, p + s.sep(p))), files))
        file_name_indent = min(max(file_lengths), 125) + 4

        for full_path in files:
            n = s.cf(full_path, p + s.sep(p))
            n = format_list_file_path(n)
            # index str
            i = i + 1
            index_str = str(i) + ":"
            # dir str
            dir_str = ""
            if (fileio.is_dir(full_path)):
                dir_str = "    <DIR>"
            # file timestamp str
            file_timestamp_str = fileio.get_file_timestamp_str(full_path)
            # size str
            size_str = fileio.get_file_size_str(full_path)
            # msg
            msg = "{0:4}{1:6}{2}{3:>10}{4:13}{5}"
            log(msg.format("", index_str, s.format_s(n, file_name_indent), size_str, dir_str, file_timestamp_str))

        if (count == get_list_max()):
            log("{0:10}{1}".format("", "......"))


def file_view(p):
    if (fileopen.is_text_file(p)):
        lines0 = fileio.l(p)
        lines_with_numbers = find_lines_with_numbers(lines0)
        size = len(lines_with_numbers)
        if (size == 0):
            if (cons.found_file_root == None):  # find in file
                if (env.has_find_condition()):  # not found lines in file
                    log("not found any lines: {0}".format(cons.find_condition))
                    cons.find_condition = None
                else:  # just view file, but no lines
                    pass
            return
        if (size > max_lines() and not cons.view_all):
            lines_with_numbers = lines_with_numbers[0:max_lines()]

        if (env.has_find_condition()):
            cons.found_file_index = cons.found_file_index + 1
            if (cons.found_file_root == None):  # find in file
                log("find from: {0} ({1})".format(fileio.get_parent(p), cons.find_condition))
                relative_path = fileio.get_file_name(p)
            else:  # find in dir
                relative_path = fileio.get_file_relative_path(p, cons.found_file_root)
            index_str = str(cons.found_file_index) + ":"
            size_str = str(size)
            log('{0:2}{1:3}found "{2}" places in "{3}":'.format("", index_str, size_str, relative_path))
            log()
            add_found_file(p)

        msg = "{0:4}{1:12}{2}"

        i = 0
        for (line_number, line) in lines_with_numbers:

            i = i + 1
            index_str = "{0}({1}):".format(str(i), str(line_number))
            add_found_line(p, line_number, line)

            if (ulog_format.is_format_log_line(line)):
                line = ulog_format.format_log_line(line, 16)
            log(msg.format("", index_str, line))

        if (size > max_lines() and not cons.view_all):
            log(msg.format("", "", "......"))

        log()


def max_lines():
    return cons.file_system.max_lines()


def find_lines_with_numbers(lines):  # starting with 1
    found_lines_with_numbers = []
    for i in range(len(lines)):
        line = lines[i]
        if (env.has_find_condition()):
            if (match_find_condition(i + 1, line)):
                found_lines_with_numbers.append((i + 1, line))
                if (cons.find_condition_multiple_lines):
                    find_lines_add_multiple_lines(found_lines_with_numbers, lines, i)
        else:
            found_lines_with_numbers.append((i + 1, line))
    if (keep_header() and found_lines_with_numbers[0][0] != 1):
        found_lines_with_numbers.insert(0, (1, lines[0]))
    return found_lines_with_numbers


def keep_header():
    return cons.file_system.keep_header()


def find_lines_add_multiple_lines(found_lines_with_numbers, lines, i):
    line = lines[i]
    left_indent_size = s.get_left_indent_size(line)
    idx = i
    while (idx < len(lines) - 1):
        idx += 1
        another_line = lines[idx]
        another_left_indent_size = s.get_left_indent_size(another_line)
        if (is_break_multiple_lines(line, another_line, another_left_indent_size, left_indent_size)):
            another_line_no_left_indent = s.cf(another_line, another_left_indent_size)
            if (another_line_no_left_indent in ["}", "},", "]", "],"]):
                found_lines_with_numbers.append((idx + 1, another_line))
            break
        else:
            found_lines_with_numbers.append((idx + 1, another_line))


def is_break_multiple_lines(line, another_line, another_left_indent_size, left_indent_size):  # @UnusedVariable
    if (cons.find_condition_multiple_lines == "mlw"):
        return another_left_indent_size < left_indent_size
    elif (cons.find_condition_multiple_lines == "mls"):
        return another_line == ""
    else:
        return another_left_indent_size <= left_indent_size


def get_list_max():
    if (cons.list_filter != None):
        return -1
    return cons.file_system.get_list_max()


def get_list_max__():
    return cons.list_max


def clean_found_file(p):
    cons.found_files = None


def add_found_file(p):
    if (cons.found_files == None):
        cons.found_files = []
    cons.found_files.append(p)


def add_found_line(p, line_number, line):
    if (env.has_find_condition()):
        if (cons.found_lines == None):
            cons.found_lines = dict()
        if (not cons.found_lines.__contains__(p)):
            found_lines_p = []
            cons.found_lines[p] = found_lines_p
        else:
            found_lines_p = cons.found_lines[p]
        found_lines_p.append((line_number, line))


def cd(p):
    cons.file_system.cd(p)


def cd__(p):
    if (not s.st(p, "\\\\")):
        if (os.path.isdir(p)):
            os.chdir(p)
        else:
            parentDir = fileio.get_parent(p)
            os.chdir(parentDir)


def list_current_dir(p):
    if (not cons.found_files is None):
        return cons.found_files
    elif (not cons.listed_files is None):
        return cons.listed_files
    else:
        return cons.file_system.list_current_dir(p)


def list_current_dir__(p):
    files = os_listdir(p)
    return list(map(lambda n: p + s.sep(p) + n, files))


def unwrap_list_condition_key(k):
    if (s.is_wrapped(k, "()")):
        k = s.unwrap(k, "()")
    elif (s.is_wrapped(k, "st()")):
        k = s.unwrap(k, "st()")
    elif (s.is_wrapped(k, "end()")):
        k = s.unwrap(k, "end()")
    elif (s.is_wrapped(k, "not()")):
        k = ""
    return k


def list_condition_key(view_all):
    if (not env.has_list_condition()):
        if (cons.list_level == None):
            return "**"
        else:
            return s.cl(s.get_repeat_string("*/", int(cons.list_level) + 1), "/")
    else:
        k = cons.list_condition
        if (s.ct(k, " ")):
            k = s.lf(k, " ")
        if (s.ct(k, "/")):
            k = s.lf(k, "/")
        k = unwrap_list_condition_key(k)
        if (view_all and not k == ""):
            if (cons.list_level == None):
                return "**/*" + k + "*"
            else:
                return s.get_repeat_string("*/", int(cons.list_level)) + "*" + k + "*"
        else:
            return "*" + k + "*"


def match_find_condition(line_number, line):  # line_number starting with 1
    if (env.has_find_condition()):
        if (len(cons.find_condition_picked) > 0):
            return line_number in cons.find_condition_picked
        k = cons.find_condition
        kk = cons.find_condition_key
        if (s.end(kk, " c")):  # case sensitive
            return s.ctic_con(line, kk)
        if (s.st(k, "q ")):
            return s.isf(line, kk)
        if (s.st(k, "f ")):
            return s.isf(line, kk)
        if (s.st(k, "fs ")):
            return s.ctic_con(line, kk)
    return True


def match_list_condition(file):
    if (env.has_list_condition()):
        n = s.rt(file, s.sep(file))
        return s.isf(n, cons.list_condition)
    return True


def list_dir(p, view_all=False, n=-1):
    start = s.nowts()
    search_key = p + s.sep(p) + list_condition_key(view_all)
    files_iter = do_iglob(search_key, recursive=view_all, dir_=p)
    files = []
    i = 0
    for file in files_iter:
        if (file == p + s.sep(p)):
            continue
        if (not match_list_condition(file)):
            continue
        i = i + 1
        files.append(file)
        if (i == n):
            break
    files = filter_list(files)
    if (files != None and len(files) > 0):
        cons.listed_files = files
    ulog.logtr("filelistfind.list_dir: {0} [{1} files]".format(search_key, len(files)))
    logp("filelistfind.list_dir".format(search_key, len(files)), start, suffix=" in {0} [{1} files]".format(search_key, len(files)))
    return files


def list_dir_(p, con=None, filter_=None, view_all=False, n=-1):
    old_list_condition = cons.list_condition
    old_list_filter = cons.list_filter
    try:
        cons.list_condition = con
        cons.list_filter = filter_
        return list_dir(p, view_all, n)
    finally:
        cons.list_condition = old_list_condition
        cons.list_filter = old_list_filter


def list_files():
    if (not cons.listed_files is None):
        return cons.listed_files
    elif (fileio.is_dir(cons.p)):
        return list_dir(cons.p, cons.view_all)
    else:
        return [cons.p]


def list_all_files():
    if (fileio.is_dir(cons.p)):
        try:
            return list_dir(cons.p, True)
        finally:
            cons.listed_files = None
    else:
        return [cons.p]


def filter_list(files):
    list_filter = cons.list_filter

    # time
    if (is_filter_by_time(list_filter)):
        isReverse = s.st(list_filter, "zy") or list_filter == "zy"
        files = fileio.sort_by_time(files, isReverse)
        if (list_filter == "sj"):
            return files
        else:
            if (s.match(list_filter, "(zj|zy)(\\d+)")):
                n = int(s.cf(list_filter, 2))
            else:
                n = 1
            return l.sf(files, n)

    # size
    if (is_filter_by_size(list_filter)):
        isReverse = s.st(list_filter, "zx") or list_filter == "zx"
        files = fileio.sort_by_size(files, isReverse)
        if (list_filter == "dx"):
            return files
        else:
            if (s.match(list_filter, "(zd|zx)(\\d+)")):
                n = int(s.cf(list_filter, 2))
            else:
                n = 1
            return l.sf(files, n)

    return files


def is_list_filter(m):
    return is_filter_by_time(m) or is_filter_by_size(m)


def is_filter_by_time(m):
    return m != None and (s.match(m, "(zj|zy)(\\d+)?") or s.iss(m, "sj"))


def is_filter_by_size(m):
    return m != None and (s.match(m, "(zd|zx)(\\d+)?") or s.iss(m, "dx"))


def format_path(to):
    to = s.cv(to, "/", s.sep())
    to = s.cv(to, "\\", s.sep())
    return to


def format_list_file_path(p):
    if (len(p) > 125):
        n = fileio.get_file_name(p)
        parent = s.cl(p, n)
        parent = parent[0: 125 - len(n) - 4] + "..."
        p = parent + s.sep(parent) + n
    return p


def rp(p, to):

    if (to == ".."):
        return rp_check(fileio.get_parent(p))

    if (to == "last"):
        files = list_current_dir(p)
        return rp_check(l.last(files))

    if (s.is_number(to)):
        toInt = int(to)
        files = list_current_dir(p)
        if (1 <= toInt <= len(files)):
            return rp_check(files[toInt - 1])

    if (fileio.is_absolute_path(to)):
        return rp_check(to)

    if (s.st(to, "\\\\")):
        return rp_check(to)

    if (is_sub_dir(p, to)):
        return rp_check(p + s.sep(p) + get_sub_dir(p, to))

    tarMap = tar.get_tar_map()
    if (tarMap.__contains__(to)):
        return rp_check(tarMap.get(to))

    to = format_path(to)
    if (s.ct(to, s.sep(to))):
        first = s.lf(to, s.sep(to))
        if (tarMap.__contains__(first)):
            first_ = tarMap.get(first)
            return rp_check(first_ + s.sep(first_) + s.clf(to, s.sep(to)))

    to_dir = p + s.sep(p) + to
    return rp_check(to_dir)


def rp_check(to_dir):
    return cons.file_system.rp_check(to_dir)


def rp_check__(to_dir):
    if (fileio.exists(to_dir)):
        return to_dir
    else:
        log("dir not exists: " + to_dir)
        return None


def is_sub_dir(p, to):
    if (fileio.is_dir(p) and len(to) > 1):
        sub_dir_names = os_listdir(p)
        ctic = list(filter(lambda n:s.ctic(n, to), sub_dir_names))
        return l.not_empty(ctic)
    return False


def get_sub_dir(p, to):
    sub_dir_names = os_listdir(p)
    issic = list(filter(lambda n:s.issic(n, to), sub_dir_names))
    if (l.not_empty(issic)):
        return l.first(issic)
    stic = list(filter(lambda n:s.stic(n, to), sub_dir_names))
    if (l.not_empty(stic)):
        return l.first(stic)
    endic = list(filter(lambda n:s.endic(n, to), sub_dir_names))
    if (l.not_empty(endic)):
        return l.first(endic)
    ctic = list(filter(lambda n:s.ctic(n, to), sub_dir_names))
    if (l.not_empty(ctic)):
        return l.first(ctic)
    return to


def os_listdir(p):
    return cons.file_system.os_listdir(p)


def os_listdir__(p):
    return os.listdir(p)


def get_method_find_key():
    files = list_files()
    method_find_key = None
    if (len(list(filter(lambda p:s.endic(p, ".py", ".scala"), files))) > 0):
        method_find_key = "def"
    else:
        method_find_key = "public##private##protected"
    if (s.st(cons.find_condition, "fs ")):
        method_find_key = s.wrap(method_find_key, "and()")
    return method_find_key


def add_additional_key(m):
    if (env.has_find_condition()):
        additional_find_key = get_additional_find_key(m)
        if (not s.end(cons.find_condition, " " + additional_find_key)):
            cons.find_condition = cons.find_condition + " " + additional_find_key
            cons.find_condition_key = s.clf(cons.find_condition, " ")
    elif (env.has_list_condition()):
        additional_list_key = get_additional_list_key(m)
        if (not s.end(cons.list_condition, " " + additional_list_key)):
            cons.list_condition = cons.list_condition + " " + additional_list_key
            cons.list_condition_key = cons.list_condition
    else:
        if (fileio.is_file(cons.p)):
            cons.find_condition = "q " + m
            cons.find_condition_key = s.clf(cons.find_condition, " ")
        else:
            cons.list_condition = m
            cons.list_condition_key = m


def get_additional_find_key(m):
    return m


def get_additional_list_key(m):
    return m


def resolve_shortcuts(m):
    if (s.st(m, "l ", "q ", "f ", "fs ")):
        op = s.lf(m, " ")
        args = s.clf(m, " ")
        if (cons.find_shortcuts.__contains__(args)):
            args = cons.find_shortcuts[args]
        m = op + " " + args
    return m


def to_ml(m):
    if (m == "noml"):
        m = None
    return m


def do_iglob(search_key, recursive=False, dir_=None):
    return cons.file_system.iglob(search_key, recursive=recursive, dir_=dir_)


def do_iglob__(search_key, recursive=False, dir_=None):  # @UnusedVariable
    import glob
    return glob.iglob(search_key, recursive=recursive)

