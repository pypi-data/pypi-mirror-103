import ustring         as s
from   ulog            import log
from   ulog            import logc

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
import cmds            as cmds
import ci              as ci


def translate(m):
    m00 = m
    m = ve(m)
    m = sort_lines(m)  # sort or duiqi
    m = replace_lines(m)
    m = del_lines(m)
    m = dup_lines(m)
    m = e(m)
    m = fue(m)
    m = fec(m)
    m = fex(m)
    m = clean_file(m)
    m = ql(m)
    m = combine_files(m)
    ulog.log_trans(m00, m)
    return m


def ve(m):
    if (s.st(m, "ve ")):
        m = s.cf(m, "ve ")
        m = "e " + s.bat_(m)
    return m


def replace_lines(m):
    if (is_replace_lines(m)):
        m = "fileedit " + m
    return m


def is_replace_lines(m):
    return s.st(m, "r ")


def del_lines(m):
    if (is_del_lines(m)):
        if (m == "-" or ids.is_ids(m, "-") or s.st(m, "rm ")):
            m = "fileedit " + m
    return m


def e(m):
    if (is_e(m)):
        m = "fileedit " + m
    elif (is_f(m)):
        m = "fileedit " + (s.cl(m, "f") + "e")
    return m


def fue(m):
    if (is_fue(m)):
        m = "fileedit " + m
    return m


def fec(m):
    if (is_fec(m)):
        m = "fileedit " + m
    return m


def fex(m):
    if (is_fex(m)):
        m = "fileedit " + m
    return m


def is_e(m):
    return s.st(m, "e ") or ids.is_ids(m, "e")


def is_f(m):
    return ids.is_ids(m, "f")


def is_fue(m):
    return m == "fue" or ids.is_ids(m, "fue", "ue")


def is_fec(m):
    return m == "fec" or ids.is_ids(m, "fec", "ec")


def is_fex(m):
    return m == "fex" or ids.is_ids(m, "fex", "ex")


def is_del_lines(m):
    return (m == "-" and env.is_find_in_file()) or ((ids.is_ids(m, "-") or s.st(m, "rm ")) and env.is_in_file())


def dup_lines(m):
    if (is_dup_lines(m)):
        m = "fileedit " + m
    return m


def is_dup_lines(m):
    return (m == "dup" or s.st(m, "dup ") or ids.is_ids(m, "dup")) and fileopen.is_text_file(cons.p)


def sort_lines(m):
    if (is_sort_lines(m)):
        m = "fileedit " + m
    return m


def is_sort_lines(m):
    return (m in ["sort", "duiqi", "duiqi2", "r noel"] or s.st(m, "sort ", "duiqi ", "duiqi2 ")) and fileopen.is_text_file(cons.p)


def clean_file(m):
    if (is_clean_file(m)):
        m = "fileedit " + m
    return m


def is_clean_file(m):
    return m == "cf"


def ql(m):
    if (m == "ql"):
        m = ".. log qingli\n[];{remove_long_lines[];eis_sort;est_sort;rdoc_sort};[log;log pyr backup;log];{tbak_local};b2"
    elif (m == "qla"):
        m = ".. [log fsrc;log];{fsrc};[log ql;log];{ql};[log;log tbak;log];{tbak};[log;log rbak;log];{rbak}"
    elif (m == "remove_long_lines"):
        do_remove_long_lines()
        m = cons.ignore_cmd
    elif (m == "eis_sort" or s.st(m, "eis_sort ") or m == "eis_sort "):
        m = do_section_sort(m, "eis")
    elif (m == "est_sort" or s.st(m, "est_sort ") or m == "est_sort "):
        m = do_section_sort(m, "est")
    elif (m == "rdoc_sort"):
        m = do_section_sort(m, "rdoc", ["go file operations:"], go_file="rd")
    return m


def combine_files(m):
    if (m == "combine" or s.st(m, "combine ")):
        files = filelistfind.list_files()
        if (len(files) > 1):
            n = fileio.get_file_simple_name(files[0])
            ext = fileio.get_file_ext(files[0])
            if (m == "combine"):
                n = s.lf(n, "_")
                n += "_combined"
            else:
                n = s.cf(m, "combine ")
            parent = fileio.get_parent(files[0])
            to = parent + s.sep(parent) + n + "." + ext
            do_combine_files(files, to)
            log("combined files to: " + to)
        m = cons.ignore_cmd
    return m


def do_combine_files(files, to):
    lines = []
    for file in files:
        lines += fileio.l(file)
    fileio.w(to, lines)


def do_section_sort(m, k="eis", keys=None, go_file=None):
    f = s.bat_(k)
    if (keys == None):
        keys = s._filter_(fileio.l(f), lambda x: s.st(x, "// "))
    if (s.st(m, k + "_sort ")):
        keys = [s.cf(m, k + "_sort ")]
    if (m == k + "_sort "):
        keys = [ci.get_text()]
    cmds = []
    if (go_file == None):
        go_file = k
    for key in keys:
        if (key == "// tmp" and k == "eis"):
            cmd = "{0};fs {1};pick 3;mls;va;sort".format(go_file, key)
        else:
            cmd = "{0};fs {1};mls;va;sort".format(go_file, key)
        cmds += [cmd]
    m = ".. " + s.conn(cmds, ";")
    ts_before = fileio.get_file_timestamp(f)

    def post_section_sort():
        ts_after = fileio.get_file_timestamp(f)
        if (ts_after > ts_before + 1):
            ulog.loga("esort: " + fileio.get_file_simple_name(f))
        else:
            ulog.loga("esort no change: " + fileio.get_file_simple_name(f))

    cons.post_handle[m] = post_section_sort
    return m


def do_remove_long_lines():
    dir_ = cons.lastop_dir
    files = filelistfind.list_dir_(dir_)
    for file in files:
        do_remove_long_lines_file(file)


def do_remove_long_lines_file(file):
    lines = fileio.l(file)
    lines00 = lines
    lines = s._filter_(lines, lambda x: len(x) < 1000)
    lines = s._filter_(lines, lambda x: not s.st(x, "$$LINE_SEP$$"))
    if (len(lines) < len(lines00)):
        fileio.w(file, lines)
        log("rm lone lines in: " + file);


def handle(m):
    if (is_del_lines(m)):
        do_del_lines(m)
    elif (is_dup_lines(m)):
        do_dup_lines(m)
    elif (is_sort_lines(m)):
        do_sort_lines(m)
    elif (is_e(m)):
        do_e(m)
    elif (is_fue(m)):
        do_fue(m)
    elif (is_fec(m)):
        do_fec(m)
    elif (is_fex(m)):
        do_fex(m)
    elif (is_clean_file(m)):
        do_clean_file(m)
    elif (is_replace_lines(m)):
        do_replace_lines(m)


def do_replace_lines(m):
    set_replace_condition(m)
    dir_view_replace()
    reset_replace_condition()


def set_replace_condition(m):
    m = s.cf(m, "r ")
    op = s.lf(m, " ")
    m = keep_ts(m)
    if (op in cons.ops):
        cons.replace_ops = m
    else:
        cons.replace_condition_camel = s.end(m, " .")
        m = s.cl(m, " .")
        parts = s.get_parts(m, no_el=False)
        cons.replace_condition_from = s.encode_for_replace(parts[0])
        cons.replace_condition_to = s.encode_for_replace(parts[1])


def keep_ts(m):
    cons.keep_timestamp = s.has_p(m, "keep_ts")
    if (cons.keep_timestamp):
        m = s.rm_p(m, "keep_ts")
    return m


def reset_replace_condition():
    cons.replace_ops = None
    cons.replace_condition_from = None
    cons.replace_condition_to = None
    cons.replace_condition_camel = False
    cons.keep_timestamp = False


def dir_view_replace():
    files = filelistfind.list_files()
    for full_path in files:
        file_view_replace(full_path)


def file_view_replace(p):
    if (fileopen.is_text_file(p)):
        lines = fileio.l(p)
        if (is_do_replace_all_lines_as_one_line()):
            lines = do_replace_all_lines_as_one_line(lines)
            log()
            fileio.w(p, lines)
            ulog.logl("", lines)
        else:
            lines_with_numbers = filelistfind.find_lines_with_numbers(lines)
            logc("replace in file: " + p)
            logc()
            changed = False
            try:
                for (line_number, line) in lines_with_numbers:
                    line_replaced = do_replace_line(line)
                    if (not line == line_replaced):
                        lines[line_number - 1] = line_replaced
                        log("{0:4}{1:7}{2}".format("", str(line_number) + ":", line))
                        log("{0:4}{1:7}{2}".format("", "  ->", s.cv(line_replaced, "\n", "\n" + s.get_indent_string(11))))
                        changed = True
            finally:
                ulog.clean_log_cache()
                if (changed):
                    log()
                    fileio.w(p, lines)


def do_replace_line(line):
    if (cons.replace_ops != None):
        return ops.do_ops(line, cons.replace_ops)
    else:
        if (cons.replace_condition_camel):
            return s.cvic(line, cons.replace_condition_from, cons.replace_condition_to)
        else:
            line = s.cv(line, cons.replace_condition_from, cons.replace_condition_to)
            return line


def is_do_replace_all_lines_as_one_line():
    if (cons.replace_ops):
        if (s.ct(cons.replace_ops, " ")):
            op = s.lf(cons.replace_ops, " ")
            return op in cons.ops_as_one_line
    return False


def do_replace_all_lines_as_one_line(lines):
    return ops.do_ops(lines, cons.replace_ops)


def do_del_lines(m):
    set_delete_condition(m)
    file_view_delete(cons.p)
    reset_delete_condition()


def set_delete_condition(m):
    cons.delete_condition = m


def reset_delete_condition():
    if (cons.delete_condition == "-" and env.has_find_condition()):
        env.reset_find()
    cons.delete_condition = None


def file_view_delete(p):
    if (fileopen.is_text_file(p)):
        lines = fileio.l(p)
        lines_with_numbers = filelistfind.find_lines_with_numbers(lines)
        logc("remove lines:")
        logc()
        try:
            delete_condition = cons.delete_condition
            delete_condition_key = None
            delete_lines_ids = []  # starting with 0
            selected_ids = None
            if (ids.is_ids(delete_condition, "-")):
                selected_ids = ids.get_ids(delete_condition, "-")
            if (s.st(delete_condition, "rm ")):
                delete_condition_key = s.cf(delete_condition, "rm ")
            idx = 0
            for (line_number, line) in lines_with_numbers:
                need_delete = False
                if (delete_condition == "-"):
                    delete_lines_ids.append(line_number - 1)
                    need_delete = True
                elif (selected_ids != None and selected_ids.__contains__(idx)):
                    delete_lines_ids.append(line_number - 1)
                    need_delete = True
                elif (delete_condition_key != None and s.isf(line, delete_condition_key)):
                    delete_lines_ids.append(line_number - 1)
                    need_delete = True
                if (need_delete):
                    log("{0:4}{1:8}{2}".format("", str(line_number) + ":", line))
                idx = idx + 1
            lines = ulist.remove_lines(lines, delete_lines_ids)
        finally:
            if (cons.has_log_cache):  # not deleted any lines
                ulog.clean_log_cache()
            else:
                log()
                fileio.w(p, lines)


def do_dup_lines(m):
    lines = fileio.l(cons.p)
    lines_with_numbers = filelistfind.find_lines_with_numbers(lines)
    found_lines = []
    start_position = lines_with_numbers[0][0]
    found_lines_count = len(lines_with_numbers)
    for (line_number, line) in lines_with_numbers:  # @UnusedVariable
        found_lines += [line]
    if (ids.is_ids(m, "dup")):
        found_lines = ids.get_selected(found_lines, m, "dup")
        m = ids.rm_ids(m, "dup")
        first_found_line = found_lines[0]
        start_position = lines.index(first_found_line) + 1
        found_lines_count = len(found_lines)
    text = s.conn(found_lines)
    text = ops.do_ops(text, m)
    dup_lines = s.sp(text)
    new_lines = []
    new_lines += lines[0:start_position - 1]
    new_lines += dup_lines
    new_lines += lines[start_position - 1 + found_lines_count: len(lines)]
    fileio.w(cons.p, new_lines)
    log(dup_lines)
    env.reset_find()


def do_sort_lines(m):
    lines = fileio.l(cons.p)
    lines_with_numbers = filelistfind.find_lines_with_numbers(lines)
    found_lines = []
    start_position = lines_with_numbers[0][0]
    found_lines_count = len(lines_with_numbers)
    for (line_number, line) in lines_with_numbers:  # @UnusedVariable
        found_lines += [line]
    sort_lines = do_sort_lines_(found_lines, s.cf(m, "r "))
    if (not found_lines == sort_lines):
        new_lines = []
        new_lines += lines[0:start_position - 1]
        new_lines += sort_lines
        new_lines += lines[start_position - 1 + found_lines_count: len(lines)]
        fileio.w(cons.p, new_lines)
        log(sort_lines)
        log()
    env.reset_find()


def do_sort_lines_(l, m):
    if (s.trim(ulist.last(l)) in ["}", "},", "]", "],"]):
        first = ulist.first(l)
        last = ulist.last(l)
        l = l[1:len(l) - 1]
        l = ops.do_ops(l, m)
        r = []
        r += [first]
        r += l
        r += [last]
        l = r
    elif (s.st(l[1], "------")):
        first = l[0:2]
        l = l[2:len(l)]
        l = ops.do_ops(l, m)
        r = []
        r += first
        r += l
        l = r
    elif (s.end(l[0], ":")):
        first = l[0:1]
        l = l[1:len(l)]
        l = ops.do_ops(l, m)
        r = []
        r += first
        r += l
        l = r
    else:
        l = ops.do_ops(l, m)
    return l


def do_e(m):
    m = s.cf(m, "e ")
    not_open = s.end(m, " ")
    m = s.trim(m)
    m = ids.to_ids_from_pure(m, "e")
    if (ids.is_ids(m, "e")):
        files = filelistfind.list_files()
        files = ids.get_selected(files, m, "e")
    else:
        if (fileio.is_absolute_path(m)):
            files = [m]
        else:
            files = [cons.p + s.sep(cons.p) + m]
    for file in files:
        do_e_one(file, not_open=not_open)


def do_e_one(file, not_open=False):
    if (not fileio.exists(file)):
        fi = open(file, "w")
        fi.close()
    if (not not_open):
        fileopen.open_file(file)
    cons.mark_go_dir = file


def do_fue(m):
    if (ids.is_ids(m, "fue", "ue")):
        files = filelistfind.list_files()
        files = ids.get_selected(files, m, "fue", "ue")
    else:
        files = [cons.p]
    for file in files:
        fileopen.open_ultraedit(file)


def do_fec(m):
    if (ids.is_ids(m, "fec", "ec")):
        files = filelistfind.list_files()
        files = ids.get_selected(files, m, "fec", "ec")
    else:
        files = [cons.p]
    for file in files:
        fileopen.open_eclipse(file)


def do_fex(m):
    if (ids.is_ids(m, "fex", "ex")):
        files = filelistfind.list_files()
        files = ids.get_selected(files, m, "fex", "ex")
    else:
        files = [cons.p]
    for file in files:
        fileopen.open_explorer(file)


def do_clean_file(m):  # @UnusedVariable
    fileio.clean_file(cons.p)
    log("clean file: " + cons.p)

