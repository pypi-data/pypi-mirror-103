import ustring         as s
from   ulog            import log

import cons            as cons
import fileio          as fileio
import ulist           as ulist
import ulog            as ulog

cr_s = "\"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe\"|--allow-outdated-plugins "
ie_s = "\"C:\\Program Files (x86)\\Internet Explorer\\iexplore.exe\"|"
ue_s = "\"C:\\Program Files (x86)\\IDM Computer Solutions\\UltraEdit\\Uedit32.exe\"|"
mx_s = ""


def translate(m):
    m00 = m
    m = ta(m)
    m = find_tar(m)
    ulog.log_trans(m00, m)
    return m


def ta(m):
    if (is_ta(m)):
        m = "tar " + m
    return m


def is_ta(m):
    return s.st(m, "ta ", "tdel ", "tacr ", "taie ", "taue ", "taoi ")


def find_tar(m):
    if (is_find_tar(m)):
        m = do_find_tar(m)
    return m


def is_find_tar(m):
    return s.st(m, "vt ", "ft ")


def do_find_tar(m):
    if (s.st(m, "vt ")):
        m = s.cf(m, "vt ")
        m = ".. gtar;;q st({0}|)[]".format(m)
    elif (s.st(m, "ft ")):
        m = s.cf(m, "ft ")
        m = ".. gtar;;q {0}[]".format(m)
    return m


def handle(m):
    if (is_ta(m)):
        do_ta(m)


def do_ta(m):
    if (s.st(m, "ta ")):
        do_tadd(m)
    elif (s.st(m, "tdel ")):
        do_tdel(m)
    elif (s.st(m, "tacr ")):
        do_tadd(m, type_="cr")
    elif (s.st(m, "taie ")):
        do_tadd(m, type_="ie")
    elif (s.st(m, "taue ")):
        do_tadd(m, type_="ue")
    elif (s.st(m, "taoi ")):
        do_taoi(m)


def do_taoi(m):
    m = s.cf(m, "taoi ")
    ip = s.lf(m, " ")
    port = s.clf(m, " ")
    tar_lines = ["m3|" + cr_s + "http://{0}:{1}/vitria-oi/app/?username=vtbaadmin&password=vitria".format(ip, port),
                 "ma3|" + mx_s + "http://{0}:{1}/vitria-oi/app/?username=vtbaadmin&password=vitria#admin".format(ip, port),
                 "mw3|" + mx_s + "http://{0}:{1}/vitria-oi/app/?username=vtbaadmin&password=vitria#workbench".format(ip, port),
                 "mq3|" + cr_s + "http://{0}:{1}/vitria-oi/app/?username=vtbaadmin&password=vitria#uri=/setting/qs".format(ip, port),
                 "madf3|" + cr_s + "http://{0}:{1}/vitria-oi/app/?username=vtbaadmin&password=vitria#uri=/setting/spark".format(ip, port),
                 "mdf3|" + cr_s + "http://{0}:{1}/vitria-oi/app/?username=vtbaadmin&password=vitria#uri=/setting/flow".format(ip, port),
                 "mas3|" + cr_s + "http://{0}:{1}/vitria-oi/app/?username=vtbaadmin&password=vitria#uri=/setting/as".format(ip, port),
                 "mqs3|" + cr_s + "http://{0}:{1}/vitria-oi/app/?username=vtbaadmin&password=vitria#uri=/setting/qs".format(ip, port)]
    if (s.end(port, "8443")):
        tar_lines = s.cv_(tar_lines, s.cv, "http", "https")
    do_add_tar_line(tar_lines)
    ulog.logkv(tar_lines, "tar", "|")


def do_tadd(m, type_=""):
    m = s.cf(m, "ta ", "tacr ", "taie ", "taue ")
    k = s.lf(m, " ")
    v = s.clf(m, " ")
    if (v == "."):
        v = cons.p
    v = rp(v)
    v = enrich_type(v, type_)
    tar_line = k + "|" + v
    do_add_tar_line(tar_line)
    ulog.logkv(tar_line, "tar", "|")


def enrich_type(v, type_):
    if (type_ == "cr"):
        v = cr_s + v
    elif (type_ == "ie"):
        v = ie_s + v
    elif (type_ == "ue"):
        v = ue_s + v
    return v


def do_tdel(m):
    m = s.cf(m, "tdel ")
    tar_line = do_del_tar_line(m)
    if (tar_line):
        k = s.lf(tar_line, "|")
        v = s.clf(tar_line, "|")
        log("remove tar: {0} = {1}".format(k, v))


def do_add_tar_line(tar_line):
    tar_list = fileio.l(cons.tar)
    if (isinstance(tar_line, list)):
        k = s.cv_(tar_line, s.lf, "|")
        tar_list = rm_tar_in_lines(tar_list, k)
        tar_list += tar_line
    else:
        tar_list = rm_tar_in_lines(tar_list, s.lf(tar_line, "|"))
        tar_list += [tar_line]
    tar_list = s.sort(tar_list, sort_key_func=lambda x:s.lower(s.lf(x, "|")))
    fileio.w(cons.tar, tar_list)

    
def rm_tar_in_lines(tar_list, k):
    if (isinstance(k, list)):
        k = s.cv_(k, s.al, "|")
    else:
        k = k + "|"
    found_list = s.filter_(tar_list, k, s.st)
    if (len(found_list) > 0):
        tar_list = ulist.rm(tar_list, found_list)
    return tar_list


def do_del_tar_line(k):
    tar_list = fileio.l(cons.tar)
    found_list = s.filter_(tar_list, k + "|", s.st)
    if (len(found_list) > 0):
        tar_list = ulist.rm(tar_list, found_list)
        fileio.w(cons.tar, tar_list)
        return found_list[0]
    return None


def get_tar_map():
    if (cons.tar_map == None):
        lines = fileio.l(cons.tar)

        rmap = dict()
        for line in lines:
            line = s.cl(line, "\n")
            key = s.lf(line, "|")
            value = s.clf(line, "|")
            rmap[key] = value

        cons.tar_map = rmap

    return cons.tar_map


def rp(k):
    import filesystem
    filesystem.fs_init()
    if (not s.is_http(k)):
        k = s.cv(k, "/", s.sep())
        if (s.ct(k, s.sep())):
            first = s.lf(k, s.sep())
            left = s.clf(k, s.sep())
            first = do_rp(first)
            k = first + s.sep(first) + left
        else:
            k = do_rp(k)
    return k


def do_rp(k):
    if (k == ".."):
        return fileio.get_parent(cons.p)
    if (k == "."):
        return cons.p
    tar_map = get_tar_map()
    if (tar_map.__contains__(k)):
        v = tar_map.get(k)
        return v
    return k


def is_key(k):
    tarMap = get_tar_map()
    return tarMap.__contains__(k)


def is_web_key(k):
    if (is_key(k)):
        v = rp(k)
        if (s.st(v, "http://", "https://")):
            return True
    return False


def is_dir_key(k):
    if (is_key(k)):
        v = rp(k)
        return fileio.is_dir(v)
    return False


def is_file_key(k):
    if (is_key(k)):
        v = rp(k)
        return fileio.is_file(v)
    return False


def rp_web(k):
    if (is_key(k)):
        v = rp(k)
        if (s.st(v, "http://", "https://")):
            return v
        elif (s.st(v, cons.mx)):
            v = s.clfw(v, "http")
            return "mx " + v
        elif (s.st(v, cons.ie)):
            v = s.clfw(v, "http")
            return "ie " + v
        elif (s.st(v, cons.ff)):
            v = s.clfw(v, "http")
            return "ff " + v
        elif (s.st(v, cons.cr)):
            v = s.clfw(v, "http")
            return "cr " + v
    return None


def get_root_key(p):
    if (s.ct(p, "/", "\\")):
        p = s.cv(p, "/", "\\")
        return s.lf(p, "\\")
    return p

