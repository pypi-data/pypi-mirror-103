import ustring         as s
from   ulog            import log

import cmds            as cmds
import cons            as cons
import filecopy        as filecopy
import fileio          as fileio
import tar             as tar
import ulist           as ulist
import ulog            as ulog

sa_file = tar.rp("dd/sast.txt")
map_ = {
    "ms"  : "bwfc, bwc, bwcomm, bwl, mscl, msts, msc, mscomm, mse, msvs, msds, msfs, mscomm, mja, mjs, msl",
    "udf" : "ucm, udf, udfa, uas",
    "uas" : "ucm, udf, udfa, uas",
    "usp" : "ual, usle, udb, uspark, ues, udc, usp, uss, uz",
    "adf" : "ual, usle, udb, uspark, ues, udc, usp, uss, uz",
    "sql" : "bwsql, mss",
    "uw"  : "uw, uws, uwt",
    "all" : "yoda",
}


def translate(m):
    m00 = m
    m = dst(m)
    m = sa(m)
    ulog.log_trans(m00, m)
    return m


def dst(m):
    if (m == "dst"):
        m = do_dsvn("st")
    elif (m == "dstf"):
        m = do_dstf()
    elif (m == "dsd"):
        m = do_dsvn("diff")
    elif (m == "dsdf"):
        m = do_dsdf()
    elif (m == "dsr"):
        m = do_dsvn("revert -R")
    elif (m == "dsinfo"):
        m = do_dsvn("info")
    elif (s.st(m, "dsc ")):
        m = do_dsc(m)
    elif (m == "mdf"):
        m = do_mdf()
    elif (m == "do_dfc"):
        m = do_dfc()
    elif (m == "do_dfc_clean"):
        m = do_dfc_clean()
    return m


def do_dsvn(k, suffix="", *a_cmds):
    lines = sa_list()
    lines = s.cv_(lines, to_path)
    st = "svn " + k + " " + s.conn(lines, " ") + suffix
    cmds = []
    cmds += ["g " + cons.yoda]
    cmds += [st + "[]"]
    cmds += a_cmds
    cmds += ["goto_not_reset " + cons.p]
    m = ".. " + s.conn(cmds, ";;")
    return m


def get_yodast():
    return cons.alogs_dir + s.sep(cons.alogs_dir) + "yodast.txt"


def get_yoda_patch():
    return cons.alogs_dir + s.sep(cons.alogs_dir) + "yoda.patch"


def get_rn_changes():
    return tar.rp("rn/util/code_changes")


def do_dstf(no_open=False):
    yodast = get_yodast()
    suffix = " > " + s.wrap(yodast)
    if (no_open):
        return do_dsvn("st", suffix)
    else:
        return do_dsvn("st", suffix, "g " + yodast, "f[]")


def do_dsdf(no_open=False):
    yoda_patch = get_yoda_patch()
    suffix = " > " + s.wrap(yoda_patch)
    if (no_open):
        return do_dsvn("diff", suffix)
    else:
        return do_dsvn("diff", suffix, "g " + yoda_patch, "fex[]")


def do_dsc(m):
    msg = s.cf(m, "dsc ")
    suffix = " -m " + s.wrap(msg)
    return do_dsvn("commit", suffix)


def do_mdf():
    # dstf
    cmds.put("do_dstf", do_dstf(True))
    do_dstf_copy = ".. g {0};cc;g {1};cv[]".format(get_yodast(), get_rn_changes())
    cmds.put("do_dstf_copy", do_dstf_copy)
    # dsdf
    cmds.put("do_dsdf", do_dsdf(True))
    do_dsdf_copy = ".. g {0};cc;g {1};cv[]".format(get_yoda_patch(), get_rn_changes())
    cmds.put("do_dsdf_copy", do_dsdf_copy)
    return ".. do_dfc_clean;do_dstf;do_dstf_copy;do_dsdf;do_dsdf_copy;[do_dfc;log;l]"


def do_dfc():
    lines = fileio.l(get_yodast())
    lines = s._filter_(lines, lambda x: s.st(x, "M ", "A "))
    lines = s._cv_(lines, lambda x: cons.yoda + s.sep(cons.yoda) + s.trim(s.cf(x, "M ", "A ")))
    lines = s._filter_(lines, lambda x: fileio.is_file(x))
    filecopy.copy_files_to_dir(lines, get_rn_changes(), root=cons.yoda)
    return cons.ignore_cmd


def do_dfc_clean():
    return ".. g {0};-".format(get_rn_changes())


def to_path(k):
    k = tar.rp(k)
    k = s.cf(k, cons.yoda + s.sep(cons.yoda))
    return k


def sa(m):
    if (m == "sa"):
        m = do_sa()
    if (s.st(m, "sa ")):
        m = do_sa_(m)
    return m


def do_sa():  # sa list
    lines = sa_list()
    log("sa: " + s.conn(lines, ", "))
    log()
    for line in lines:
        log("{0:11}{1}".format(line + ":", tar.rp(line)))
    return cons.ignore_cmd


def do_sa_(m):  # sa xxx
    m = s.cf(m, "sa ")
    lines = resolve_sa(m)
    do_set_sa(lines)
    return cons.ignore_cmd
 

def resolve_sa(m):
    if (s.st(m, "+")):
        return add_sa(m)
    elif (s.st(m, "-")):
        return remove_sa(m)
    elif (map_.__contains__(m)):
        return s.sp(map_[m], ", ")
    else:
        return s.sp(m, " ")


def add_sa(m):
    m = s.cf(m, "+")
    lines = sa_list()
    lines = ulist.add(lines, m)
    return lines

   
def remove_sa(m):
    m = s.cf(m, "-")
    lines = sa_list()
    lines = ulist.rm(lines, m)
    return lines


def do_set_sa(lines):
    fileio.w(sa_file, lines)
    do_sa()


def sa_list():
    return fileio.l(sa_file)
