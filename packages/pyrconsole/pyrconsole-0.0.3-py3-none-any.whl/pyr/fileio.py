import ustring         as s
from   ulog            import log
from   ulog            import logd
from   ulog            import logtr

import os

import cons            as cons
import env             as env
import filelistfind    as filelistfind
import ulist           as ulist
import ulog            as ulog


def translate(m):
    m00 = m
    m = quit_all(m)
    m = run_all(m)
    m = to_pieces(m)
    m = fileio_md(m)
    m = fileio_set_ts(m)
    m = fileio_encoding(m)
    ulog.log_trans(m00, m)
    return m


def to_pieces(m, size=10000):
    if (m == "top" and s._r_("fileopen.is_text_file", cons.p)):
        f = cons.p
        fi = open(f, "r", errors='ignore')
        parent = get_parent(f)
        n = get_file_name(f)
        o_dir = parent + s.sep(parent) + n + ".pieces"
        mkdir(o_dir)
        i = 1
        o = o_dir + s.sep(o_dir) + str(i) + ".txt"
        fo = open(o, "a", errors='ignore')
        count = 0
        while (True):
            line = fi.readline()
            if (line):
                fo.write(line)
                count += 1
                if (count == size):
                    count = 0
                    fo.close()
                    log(o)
                    i += 1
                    o = o_dir + s.sep(o_dir) + str(i) + ".txt"
                    fo = open(o, "a", errors='ignore')
            else:
                break
        fo.close()
        log(o)
        cons.mark_go_dir = o_dir
    return m


def fileio_md(m):
    if (s.st(m, "md ")):
        m = "fileio " + m
    return m


def fileio_set_ts(m):
    if (s.st(m, "set_ts ")):
        m = "fileio " + m
    return m


def fileio_encoding(m):
    if (m == "gbk"):
        cons.encodings.pop(cons.p)
    elif (m in ["nogbk", "utf8", "utf"]):
        cons.encodings[cons.p] = "UTF-8"
    elif (m in ["view encodings", "venc"]):
        ulog.log_dict("encodings", cons.encodings)
    return m


def handle(m):
    if (s.st(m, "md ")):
        do_md(m)
    elif (s.st(m, "set_ts ")):
        do_set_ts(m)


def do_md(m):
    m = s.cf(m, "md ")
    make_dir = s.format_sep(cons.p + s.sep(cons.p) + m)
    mkdir(make_dir)
    cons.mark_go_dir = make_dir
    log("mkdir: " + make_dir)


def do_set_ts(m):
    m = s.cf(m, "set_ts ")
    import time
    ts = time.strptime(m, '%Y-%m-%d %H:%M:%S')
    set_file_timestamp(cons.p, time.mktime(ts))
    log("set ts of \"{0}\" to \"{1}\"".format(cons.p, m))


def get_file_path(f):
    return f


def get_file_name(f):
    return s.rt(f, s.sep(f))


def get_file_name__(f):
    return s.rt(f, s.sep(f))


def get_file_simple_name(f):
    return s.crt(get_file_name(f), ".")


def get_file_ext(f):
    file_name = get_file_name(f)
    if (s.ct(file_name, ".")):
        return s.rt(file_name, ".")
    else:
        return ""


def get_file_content(f):
    return s.conn(l(f), "\n")


def get_file_relative_path(p, root):
    return s.rt(p, root + s.sep(root))


def l(f, encoding=None):
    return cons.file_system.l(f, encoding=encoding)


def lwc(f, encoding=None):  # with cache
    k = [f, "{0} [{1}]".format(f, encoding)][not encoding == None]
    if (not cons.lines_cache.__contains__(k)):
        cons.lines_cache[k] = l(f, encoding)
    return cons.lines_cache[k]


def do_l__(f, encoding=None):
    if (not encoding == None):
        cons.encodings[f] = encoding
    if (exists(f)):
        lines = None
        if (cons.encodings.__contains__(f)):
            lines = do_l(f, encoding=cons.encodings[f])
        else:
            fi = open(f, "r", errors='ignore')
            try:
                logtr("get   lines from file \"{0}\" with encoding \"{1}\".".format(f, "gbk"))
                lines = s.no_line_sep(do_readlines(f, fi))
            except UnicodeDecodeError as e:
                logtr("cannot get lines from file \"{0}\". Reason is \"{1}\".".format(f, str(e)))
            finally:
                fi.close()
            if (lines == None):
                lines = do_l(f, encoding="UTF-8")
    else:
        lines = []
    return lines


def do_l(f, encoding="UTF-8"):
    fi = open(f, "r", encoding=encoding, errors='ignore')
    try:
        logtr("get   lines from file \"{0}\" with encoding \"{1}\".".format(f, str(encoding)))
        lines = s.no_line_sep(do_readlines(f, fi))
        return lines
    except UnicodeDecodeError as e:
        logtr("cannot get lines from file \"{0}\". Reason is \"{1}\".".format(f, str(e)))
    finally:
        fi.close()
    return None


def do_readlines(f, fi):
    if (not env.has_find_condition() and not cons.view_all and get_file_size(f) > 5 * cons.MB):
        lines = do_readlines_(fi, 60)
    else:
        lines = fi.readlines()
    return lines


def do_readlines_(fi, n=-1):
    lines = []
    i = 0
    while (True):
        line = fi.readline()
        if line is None:
            return lines
        i += 1
        if (n > 0 and i == n):
            return lines
        lines.append(line)


def w(f, lines):
    cons.file_system.w(f, lines)


def w__(f, lines):
    if (cons.encodings.__contains__(f)):
        do_w(f, lines, encoding=cons.encodings[f])
    elif (f == cons.rnt and s.is_chinese(lines[0])):
        cons.encodings[f] = "UTF-8"
        do_w(f, lines, encoding=cons.encodings[f])
    else:
        meet_ex = False
        fi = open(f, "w")
        try:
            logtr("write lines from file \"{0}\" with encoding \"{1}\".".format(f, "gbk"))
            for line in lines:
                fi.write(line + "\n")
        except:
            meet_ex = True
        finally:
            fi.close()
        if (meet_ex):
            do_w(f, lines, encoding="UTF-8")


def do_w(f, lines, encoding="UTF-8"):
    fi = open(f, "w", encoding=encoding)
    try:
        logtr("write lines from file \"{0}\" with encoding \"{1}\".".format(f, str(encoding)))
        cons.encodings[f] = encoding
        for line in lines:
            fi.write(line + "\n")
    finally:
        fi.close()


def append_line(f, line):
    fi = open(f, "a")
    fi.write(line + "\n")
    fi.close()


def append_line_no_dup(f, line):
    if (exists(f)):
        lines = l(f)
        if (not line in lines):
            append_line(f, line)
    else:
        append_line(f, line)


def append_lines(f, lines):
    for line in lines:
        append_line(f, line)


def append_lines_no_dup(f, lines_add):
    if (exists(f)):
        lines = l(f)
        for line in lines_add:
            if (not line in lines):
                lines += [line]
        w(f, lines)
    else:
        w(f, lines_add)


def insert_line(f, line):
    lines = l(f)
    if (isinstance(line, list)):
        line = s.cv_(line, s.cv, "\n", "$$LINE_SEP$$")
        lines = ulist.rm(lines, line)
        line.reverse()
        for line_ in line:
            lines.insert(0, line_)
    else:
        line = s.cv(line, "\n", "$$LINE_SEP$$")
        lines = ulist.rm(lines, line)
        lines.insert(0, line)
    w(f, lines)


def get_first_line(f):
    lines = l(f)
    if (not lines == None and len(lines) > 0):
        return lines[0]
    else:
        return None


def clean_file(f):
    fi = open(f, "w+")
    fi.close()


def get_file_count(f):
    try:
        count = 0
        fi = open(f, "r")
        for cur_line_number, line in enumerate(fi):  # @UnusedVariable
            count = count + 1
        fi.close()
        return count
    except:
        return 10000


def get_file_line(f, i):
    fi = open(f, "r")
    for cur_line_number, line in enumerate(fi):  # @UnusedVariable
        if (cur_line_number == i - 1):
            return line
    fi.close()
    return None


def get_parent(f):
    return cons.file_system.get_parent(f)


def get_parent__(f):
    return os.path.abspath(os.path.dirname(f) + s.sep(f) + ".")


def sort_by_time(files, isReverse=False):
    files.sort(key=lambda f: get_file_timestamp(f), reverse=not isReverse)
    return files


def sort_by_size(files, isReverse=False):
    files.sort(key=lambda f: get_file_size(f), reverse=not isReverse)
    return files


def get_file_timestamp(f):
    return cons.file_system.get_file_timestamp(f)


def get_file_timestamp__(f):
    return os.stat(f).st_mtime


def set_file_timestamp(f, ts):
    cons.file_system.set_file_timestamp(f, ts)

        
def set_file_timestamp__(f, ts):
    os.utime(f, (ts, ts))


def get_file_size(f):
    return cons.file_system.get_file_size(f)


def get_file_size__(f):
    return os.path.getsize(f)


def get_file_timestamp_str(f):
    return cons.file_system.get_file_timestamp_str(f)


def get_file_timestamp_str__(f):
    mtime = get_file_timestamp(f)
    import time
    mtime_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))
    return mtime_str


def get_file_size_str(f):
    return cons.file_system.get_file_size_str(f)


def get_file_size_str__(f):
    if (is_file(f)):
        fsize = get_file_size(f)
        fsize_str = format_file_size(fsize)
        return fsize_str
    else:
        return ""


def format_file_size(size):
    if (size < cons.size_rate * cons.MB):
        return '%.2f' % float(size / cons.KB) + ' KB'
    elif (cons.size_rate * cons.MB <= size < cons.size_rate * cons.GB):
        return '%.2f' % float(size / cons.MB) + ' MB'
    elif (cons.size_rate * cons.GB <= size < cons.size_rate * cons.TB):
        return '%.2f' % float(size / cons.GB) + ' GB'
    elif (cons.size_rate * cons.TB <= size):
        return '%.2f' % float(size / cons.TB) + ' TB'


def is_absolute_path(f):
    return s.st(f, "/") or (len(f) > 1 and f[1] == ":")


def is_file(f):
    return cons.file_system.is_file(f)


def is_file__(f):
    return os.path.isfile(f)


def is_dir(f):
    return cons.file_system.is_dir(f)


def is_dir__(f):
    return os.path.isdir(f)


def exists(f):
    return cons.file_system.exists(f)


def exists__(f):
    return os.path.exists(f)


def get_vtba(f):
    while (not exists(f + s.sep(f) + "wildfly")):
        f00 = f
        f = get_parent(f)
        if (f00 == f):
            return None
    return f


def mkdir(make_dir):
    parent = get_parent(make_dir)
    if (not exists(parent)):
        mkdir(parent)
    if (not exists(make_dir)):
        do_mkdir(make_dir)


def do_mkdir(f):
    cons.file_system.mkdir(f)


def do_mkdir__(f):
    os.mkdir(f)


def get_shared_root(files):
    if (not files == []):
        root = get_parent(files[0])
        while (True):
            if (is_root(root, files)):
                break
            root = get_parent(root)
        return root
    return None


def is_root(root, files):
    if (isinstance(files, list)):
        for file in files:
            if (not is_root(root, file)):
                return False
        return True
    else:
        file = files
        return file == root or s.st(file, root + s.sep(root))


def is_quit_all():
    f = s.alogs_("quit_all.txt")
    if (exists(f)):
        ts = int(get_file_timestamp(f) * 1000)
        nts_ = s.nowts()
        return exists(f) and ts > nts_ - 1 * 1000
    return False


def quit_all(m):
    if (m == "qa"):
        f = s.alogs_("quit_all.txt")
        set_file_timestamp(f, float(s.nowts()) / 1000)
    return m


def run_all(m):
    if (s.st(m, "rra ")):
        f = s.alogs_("run_all.txt")
        cmd = s.cf(m, "rra ")
        w(f, [cmd])
    return m


def is_run_all():
    f = s.alogs_("run_all.txt")
    if (exists(f)):
        ts = int(get_file_timestamp(f) * 1000)
        nts_ = s.nowts()
        r = exists(f) and ts > nts_ - 1 * 1000
        if (r):
            if (not cons.is_run_all_ts == None and cons.is_run_all_ts > nts_ - 1100):
                return False
            cons.is_run_all_ts = nts_
            return True
    return False


def get_run_all_cmd():
    f = s.alogs_("run_all.txt")
    if (exists(f)):
        lines = l(f)
        if (len(lines) > 0):
            return lines[0]
    return False

