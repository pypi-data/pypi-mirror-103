import ustring         as s
from   ulog            import log
from   ulog            import logd

import cons            as cons
import filecopy        as filecopy
import filedelete      as filedelete
import filelistfind    as filelistfind
import tar             as tar
import ulist           as l
import ulog            as ulog
import uzip            as uzip


def translate(m):
    m00 = m
    m = tr_n(m)
    ulog.log_trans(m00, m)
    return m


def tr_n(m):
    if (m == "n"):
        n()
        m = cons.ignore_cmd
    return m


def n():
    try:
        ulog.set_log_tab(4, debug=True)
        p = cons.p
        n_lib()
        n_ear(p)
    finally:
        ulog.clean_log_tab(debug=True)


def n_lib():
    log("updating libs")
    do_n_lib()
    log("updated  libs")
    log()

    
def do_n_lib():
    logd("copying dist jars to jboss lib")
    cp("dist", "jmvv")
    cp("dist", "VTBA_HOME/runtime/common/lib")
    cp("dm", "jmvv")
    cp("dm", "VTBA_HOME/runtime/common/lib")
    
    logd("copying dist jars to jboss deploy")
    cp("dist", "jd", con="not(.xml)")
    cp("dm", "jd", con="not(.xml)")
    cp("spw/standalone/deployments", "jd")
    
    logd("copying dist jars to build lib")
    cp("dist", "VTBA_HOME/build/lib")
    cp("dm", "VTBA_HOME/build/lib")
    
    logd("copying locale files")
    cp("bwl", "locale")
    cp("msl", "locale")
    cp("mul", "locale")
    
    logd("copying sql files")
    cp("bwsql", "sqls")
    cp("mss", "sqls")
    
    logd("copying server bundles")
    cp("bsdist", "bs")
    logd("copying ui bundles")
    cp("budist", "bu")


def n_ear(p):
    log("updating server ear")
    do_n_ear(p)
    log("updated  server ear")


def do_n_ear(p):
    to_dir = cons.tmp + s.sep(cons.tmp) + "vtm3oserver"
    n = "vtm3oserver.ear"
    # copy and unzip
    unzip_(to_dir, n)
    # updating jars
    cons.copy_files = []
    cp("dm", to_dir + s.sep(to_dir) + "vtm3oserver\\lib")
    cp("dm", to_dir + s.sep(to_dir) + "vtm3oserver")
    cp("dmj", to_dir + s.sep(to_dir) + "vtm3oserver")
    # updating jars in stage
    cp("dm", "emstage/lib")
    cp("dm", "emstage")
    cp("dmj", "emstage")
    # zip
    if (len(cons.copy_files) > 0):
        zip_(to_dir, n)
    else:
        logd("ear no update")
    # clean
    filelistfind.cd(p)
    clean_(to_dir, n)


def unzip_(to_dir, n):
    try:
        ulog.tmp_silent()
        from_file = tar.rp("jd/" + n)
        ear_file = to_dir + s.sep(to_dir) + n
        to_file = ear_file
        filedelete.do_del_file(to_dir)
        filecopy.do_copy_file(from_file, to_file)
        uzip.do_unzip(ear_file)
    finally:
        ulog.no_tmp_silent()


def zip_(to_dir, n):
    try:
        ulog.tmp_silent()
        dir_ = to_dir + s.sep(to_dir) + "vtm3oserver"
        files = filelistfind.list_dir_(dir_)
        uzip.do_zip(files, p=dir_, m="ear", ext="ear")
        from_file = dir_ + s.sep(dir_) + n
        to_file = tar.rp("jd/" + n)
        filecopy.do_copy_file(from_file, to_file, overwrite=True)
    finally:
        ulog.no_tmp_silent()


def clean_(to_dir, n):
    try:
        ulog.tmp_silent()
        filedelete.do_del_file(to_dir)
    finally:
        ulog.no_tmp_silent()


def cp(from_dir, to_dir, con=None):
    to_dir = s.cv(to_dir, "VTBA_HOME", "home")
    from_dir = tar.rp(from_dir)
    to_dir = tar.rp(to_dir)
    filecopy.copy_files_in_dir(from_dir, to_dir, con=con)

