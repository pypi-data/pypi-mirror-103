import ustring         as s
from   ulog            import log

import ulog            as ulog
import cons            as cons


def translate(m):
    m00 = m
    m = gsys(m)
    m = cv_in(m)
    m = cp_out(m)
    ulog.log_trans(m00, m)
    return m


def gsys(m):
    import tar
    if (cons.p == tar.rp("udf/modules/syslogmodule") and m == "mk"):
        cmds = []
        # copy jar
        cmds.append("gsys")
        cmds.append("gex")
        cp_(cmds, "components/syslog-common/dist/vtdfsyslog-common.jar", "down", sub_="syslog")
        # unzip
        cmds.append("x")
        cmds.append("c")
        cmds.append("l")
        cmds.append("g vtdfsyslog-common")
        # rm
        cmds.append("rm locale")
        cmds.append("g com")
        cmds.append("g vitria")
        cmds.append("rm dataflow")
        cmds.append("r")
        cmds.append("r")
        # jar
        cmds.append("jar")
        # copy to dest
        cmds.append("gf")
        to_dir = tar.rp("rnp/Support/0203 syslog source in stream builder/Syslog on Kafka sample received")
        cp_(cmds, "", to_dir, sub_="dist")
        cmds.append("1 : vtsyslog-parser")
        cmds.append("c")
        # copy to VTBA_HOME
        cp_(cmds, "vtsyslog-parser.jar", "home/viaops/libs")
        # clean
        cmds.append("gdn")
        cmds.append("l (syslog)")
        cmds.append("-")
        # back
        cmds.append("g " + to_dir)
        cmds.append("g dist")
        cmds.append("l[]")
        # cmd
        m = ".. " + s.conn(cmds, ";;")
    if (cons.p == "C:\\Users\\gzhou\\Desktop\\rename\\Project\\Support\\0203 syslog source in stream builder\\Syslog on Kafka sample received\\dist\\vtsyslog-parser.jar" and m == "up"):
        cmds = []
        # cc
        cmds.append("cc")
        # cv full
        cmds.append("g D:\\jedi\\branches\\SNMP_DO\\full\\8_libs\\syslog")
        cmds.append("-")
        cmds.append("log[]")
        cmds.append("cvnc[]")
        # cv update
        cmds.append("g D:\\jedi\\branches\\SNMP_DO\\update\\8_libs\\syslog")
        cmds.append("-")
        cmds.append("log[]")
        cmds.append("cv[]")
        # st
        cmds.append("g D:\\jedi\\branches\\SNMP_DO")
        cmds.append("log[]")
        cmds.append("st[]")
        # cmd
        m = ".. " + s.conn(cmds, ";;")
    return m


def cv_in(m):
    if (m == "cvin"):
        cmds = []
        # import
        import fileio
        # extract
        cmds.append("x")
        # go dir
        p = cons.p
        parent_dir = fileio.get_parent(p)
        n = fileio.get_file_simple_name(p)
        x_dir = parent_dir + s.sep(p) + n
        cmds.append("g " + x_dir)
        # copy
        cmds.append("cv ov ;a[]")
        # jar
        ext = fileio.get_file_ext(p)
        cmds.append("c")
        cmds.append(ext)
        cmds.append("gf")
        # copy
        cp_(cmds, "", parent_dir, overwrite_=True)
        # clean up
        cmds.append("g " + parent_dir)
        cmds.append("l (" + n + ")")
        cmds.append("-")
        # go file
        cmds.append("g " + p)
        # cmd
        m = ".. " + s.conn(cmds, ";;")
    return m


def cp_out(m):
    if (s.st(m, "cpout ")):
        # args
        m = s.cf(m, "cpout ")
        if (s.ct(m, " ")):
            to = s.lf(m, " ")
            filter_ = s.clf(m, " ")
        else:
            to = "down"
            filter_ = m
        
        cmds = []
        # import
        import fileio
        import tar
        # enrich args
        to = tar.rp(to)
        # extract
        cmds.append("x")
        # go dir
        p = cons.p
        parent_dir = fileio.get_parent(p)
        n = fileio.get_file_simple_name(p)
        x_dir = parent_dir + s.sep(p) + n
        cmds.append("g " + x_dir)
        # copy
        cmds.append("a")
        cmds.append("l " + filter_)
        cmds.append("cc")
        cmds.append("g " + to)
        cmds.append("cv[]")
        # clean up
        cmds.append("g " + parent_dir)
        cmds.append("l (" + n + ")")
        cmds.append("-")
        # go file
        cmds.append("g " + to)
        cmds.append("l " + filter_ + "[]")
        # cmd
        m = ".. " + s.conn(cmds, ";;")
    return m


def mv_(cmds, from_, to_, sub_=""):
    cp_(cmds, from_, to_, sub_, mv_=True)


def cp_(cmds, from_="", to_="", sub_="", mv_=False, overwrite_=False):
    if (not from_ == ""):
        cmds.append("g " + from_)
    if (mv_):
        cmds.append("cx")
    else:
        cmds.append("cc")
    cmds.append("g " + to_)
    if (not sub_ == ""):
        cmds.append("md " + sub_)
        cmds.append("gf")
        cmds.append("-")
    if (overwrite_):
        cmds.append("cv ov")
    else:
        cmds.append("cv")

