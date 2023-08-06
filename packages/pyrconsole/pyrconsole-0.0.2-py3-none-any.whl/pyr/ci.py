import ustring         as s
from   ulog            import log

import ulog            as ulog
import ulist           as ulist
import cons            as cons
import fileio          as fileio
import ms              as ms
import env             as env
import ustring_ops     as ops
import rvar            as rvar
import ids             as ids
import tar             as tar
import filelistfind    as filelistfind
import ulog_format     as ulog_format


def translate(m):
    m00 = m
    m = slash(m)
    m = lasoff(m)
    m = cvic(m)
    m = ci_cmds(m)
    m = i(m)
    m = mg(m)
    m = id_(m)
    m = ci_file(m)
    m = cipa(m)
    m = cie_space(m)
    m = cie(m)
    m = cqu(m)
    m = ch(m)
    m = in_clipboard(m)
    m = to_ci(m)
    m = resolve_bug(m)
    m = m_plus(m)
    m = cdo(m)
    m = cbug(m)
    m = cpjar(m)
    m = cpear(m)
    m = cplo(m)
    m = mysql(m)
    m = ci_ops(m)
    ulog.log_trans(m00, m)
    return m


def lasoff(m):
    if (m == "lasoff"):
        cons.lasoff = True
        m = cons.ignore_cmd
    elif (m == "lason"):
        cons.lasoff = False
        m = cons.ignore_cmd
    return m


def cvic(m):
    if (s.st(m, " cv ") and s.end(m, " .")):
        m = " cvic " + s.cl(s.cf(m, " cv "), " .")
    return m


def ci_cmds(m):
    cmds = ["gg"]
    for cmd in cmds:
        if (s.st(m, cmd + " ")):
            m = s.cf(m, cmd + " ")
            m = ".. ci {0};{1}".format(m, cmd)
    return m


def i(m):
    if (m == "i"):
        m = "m"
    return m


def mg(m):
    if (m == "mg"):
        if (len(cons.m_list) > 0):
            text = s.conn(cons.m_list)
            set_text(text)
            logci(text)
            m = cons.ignore_cmd
        else:
            log("no m list.")
            m = cons.ignore_cmd
    elif (m == "mgc"):
        cons.m_list = []
        log("clean m list.")
        m = cons.ignore_cmd
    return m


def id_(m):
    if (m == "id"):
        do_id()
        m = cons.ignore_cmd
    return m


def do_id():
    text = get_text()
    text = s.format_paragraph(text)
    set_text(text)
    logci(text)


def ci_file(m):
    if (m == "ci"):
        if (not cons.cal_result == None):
            m = "ci cal_result"
        elif (env.has_find_condition()):
            m = "ci find_result"
        else:
            m = "ci file_path"
    elif (m == "cifmt"):
        m = "ci find_result format"
    elif (m == "cin"):
        m = "ci file_name"
    elif (m == "cisn"):
        m = "ci file_simple_name"
    elif (m == "cic"):
        m = "ci file_content"
    elif (m == "cicfmt"):
        m = "ci file_content format"
    elif (m == "ciy"):
        m = "ci yoda_path"
    elif (m == "civ"):
        m = "ci vtba_path"
    elif (m == "civ2"):
        m = "ci vtba_path_2"
    elif (m == "civ3"):
        m = "ci vtba_path_3"
    elif (m == "cifix"):
        m = "ci fix_bug"
    elif (m == "cip"):
        m = "ci package"
    elif (m == "ciw20"):
        m = "ci http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_branches/wildfly20_upgrade" + s.cv(s.cf(cons.p, cons.yoda), "\\", "/")
    elif (ids.is_ids(m, "ci", "cin", "cisn")):
        m = "ci " + m
    return m


def cipa(m):
    if (m == "cipa" or s.st(m, "cipa ")):
        m = "ci " + m
    return m


def cie_space(m):
    for op in cons.ops:
        if (s.st(m, " " + op + " ") or m == " " + op):
            m = "ci cie" + m
    return m


def cie(m):
    if (s.st(m, "cie ")):
        m = "ci " + m
    return m


def cqu(m):
    if (m == "c."):
        m = "c." + get_text()
    elif (m == "c. "):
        m = "c." + get_text() + " "
    
    if (s.st(m, "c.")):
        m = "ci cqo " + s.cf(m, "c.")
    return m


def ch(m):
    if (m == "ch" or s.st(m, "ch ")):
        m = "ci " + m
    return m


def in_clipboard(m):
    m = in_clipboard_ci_wrap(m)
    return m


def to_ci(m):
    if (m == "to_mc"):
        k = get_text()
        a = s.lf(k, "_")
        b = s.clf(k, "_")
        m = "ci public static final String {0}_{1} = \"{0}.{1}\";".format(a, b)
    return m


def resolve_bug(m):
    if (m == "rev"):
        m = ".. rnt;fs Revision:;ci; clf  []"
    elif (m == "svn"):
        m = ".. rnt;fs  : ;ci[]"
    return m


def m_plus(m):
    if (m == "m+"):
        text = get_text()
        lines = s.sp(text)
        fileio.insert_line(cons.chf, lines)
        ulog.logl("add lines in " + cons.chf, lines)
        m = cons.ignore_cmd
    return m


def ci_ops(m):
    if (cons.ci_ops.__contains__(m)):
        m = s.cv(cons.ci_ops[m], "xxx", get_text())
    return m


def cdo(m):
    if (m == "cdo"):
        m = chf_st("DO-", 10)
    return m


def cbug(m):
    if (m == "cbug"):
        m = chf_st("VITR00", 20)
    return m


def chf_st(k, len_):
    lines = fileio.l(cons.chf)
    lines = s._filter_(lines, lambda x: s.st(x, k) and s.get_length(x) > len_)
    lines = s.cv_(lines, s.trim)
    lines = s.rmdup(lines)
    line = ulist.select("ci", lines)
    if (not line == None and not line == ""):
        return "ci " + line
    else:
        return cons.ignore_cmd


def cpjar(m):
    if (m == "cpjar"):
        jar_map = {
            "vtclient.jar" : "yoda/export/m3o/dist",
            "vtcommon.jar" : "yoda/export/dist",
            "vtfc.jar"     : "yoda/export/dist",
        }
        keys = list(jar_map.keys())
        key = ulist.select("jar", keys)
        if (not key == None and not key == ""):
            m = "ci " + "copy {0}/{1} to VTBA_HOME/wildfly/modules/com/vitria/vtlibs/main".format(jar_map[key], key)
        else:
            m = cons.ignore_cmd
    return m


def cpear(m):
    if (m == "cpear"):
        ear_map = {
            "vtdomainservice.jar" : "yoda/export/m3o/dist",
            "vtvirtualserver.jar" : "yoda/export/m3o/dist",
            "vtcore.jar"          : "yoda/export/m3o/dist",
            "vtfeedserver.jar"    : "yoda/export/m3o/dist",
        }
        keys = list(ear_map.keys())
        key = ulist.select("jar", keys)
        if (not key == None and not key == ""):
            m = "ci " + "copy {0}/{1} to VTBA_HOME/wildfly/standalone/deployments/vtm3oserver.ear!/lib".format(ear_map[key], key)
        else:
            m = cons.ignore_cmd
    return m


def cplo(m):
    if (m == "cplo"):
        lo_map = {
            "virtualserver.properties" : "yoda/m3o/server/locale/en_US",
            "domainservice.properties" : "yoda/m3o/server/locale/en_US",
            "client.properties"        : "yoda/m3o/server/locale/en_US",
        }
        keys = list(lo_map.keys())
        key = ulist.select("property file", keys)
        if (not key == None and not key == ""):
            m = "ci " + "copy {0}/{1} to VTBA_HOME/locale/en_US".format(lo_map[key], key)
        else:
            m = cons.ignore_cmd
    return m


def mysql(m):
    if (m == "my"):
        cons.ci_mysql = True
        log("ci mysql")
        m = cons.ignore_cmd
    if (cons.ci_mysql):
        if (cons.ci_mysql_map.__contains__(m)):
            m = "ci " + cons.ci_mysql_map[m]
        elif (s.st(m, "sv ")):
            m = s.cf(m, "sv ")
            m = "ci show variables like '%{0}%';".format(m)
        elif (s.st(m, "ss ")):
            m = s.cf(m, "ss ")
            m = "ci show global status like '%{0}%';".format(m)
        elif (s.st(m, "sg ")):
            m = s.cf(m, "sg ")
            m = "ci SET GLOBAL {0}={1};".format(s.lf(m, " "), s.clf(m, " "))
    return m


def slash(m):
    if (m == "c/"):
        m = "c.st(/) "
    elif (m == "f/"):
        m = "f.st(/) "
    return m


def in_clipboard_ci_wrap(m):
    if (s.is_wrapped(m, "ci()")):
        m = s.unwrap(m, "ci()")
        if (s.end(m, "xxx")):
            m = s.cl(m, "xxx")
        else:
            m = m + " "
        m = m + get_text()
    return m


def handle(m):
    text = ""

    if (m == "view"):
        text = get_text()
        lines = text.split("\n")
        ulog.logl("in clipboard", lines)
        log()
        return

    if (m == "file_path"):
        text = cons.p
    elif (m == "cal_result"):
        text = cons.cal_result
    elif (m == "find_result"):
        text = do_find_result(m)
    elif (m == "find_result format"):
        text = do_find_result(m, format_=True)
    elif (m == "file_name"):
        text = fileio.get_file_name(cons.p)
    elif (m == "file_simple_name"):
        text = fileio.get_file_simple_name(cons.p)
    elif (m == "file_content"):
        text = fileio.get_file_content(cons.p)
    elif (m == "file_content format"):
        text = ulog_format.format_lines(fileio.get_file_content(cons.p))
    elif (m == "yoda_path"):
        text = s.to_linux_path(s.cv(cons.p, cons.yoda, "yoda"))
    elif (is_vtba(m)):
        text = do_vtba(m)
    elif (m == "fix_bug"):
        text = get_text()
        text = "fix {0} - {1}".format(s.lf(text, " "), s.clf(text, " "))
    elif (m == "package"):
        text = s.get_package(cons.p)
    elif (s.st(m, "cqo ")):
        text = do_cqo(m)
    elif (m == "ch" or s.st(m, "ch ")):
        text = do_ch(m)
    elif (s.st(m, "cipa ")):
        text = do_cipa_st(m)
    elif (m == "cipa"):
        text = do_cipa(m)
    elif (s.st(m, "cie ")):
        text = do_cie(m)
    elif (ids.is_ids(m, "ci", "cin", "cisn")):
        text = do_ids(m)
    elif (m == "list"):
        text = do_list(m)
    else:
        text = rvar.rvar(m)

    if (not text == ""):
        text = s.cv_line_sep(text)
        set_text(text)
        logci(text)
        insert_chf(text)
        cons.m_list += s.sp(text)


def do_find_result(m, format_=False):  # @UnusedVariable
    found_file = cons.found_files[0]
    found_lines = cons.found_lines[found_file]
    lines_in_one_line = ""
    for (line_number, line) in found_lines:  # @UnusedVariable
        if (format_ and ulog_format.is_format_log_line(line)):
            line = ulog_format.format_log_line(line)
        lines_in_one_line = lines_in_one_line + line + cons.line_sep
    text = s.cl(lines_in_one_line, cons.line_sep)
    return text


def is_vtba(m):
    return m == "vtba_path" or m == "vtba_path_2" or m == "vtba_path_3"


def do_vtba(m):
    to = {
        "vtba_path"   : "VTBA_HOME",
        "vtba_path_2" : "%VTBA_HOME%",
        "vtba_path_3" : "$VTBA_HOME",
    }
    p = cons.p
    from_s = None
    for k in ["home", "h1", "h2", "h3"]:
        if (s.st(p, tar.rp(k))):
            from_s = tar.rp(k)
            break
    if (from_s == None):
        from_s = fileio.get_vtba(p)
    r = s.to_linux_path(s.cv(p, from_s, to[m]))
    return r


def do_cqo(m):
    m = s.cf(m, "cqo ")
    select = s.end(m, " ")
    if (select):
        m = s.cl(m, " ")
    file_path = cons.chf
    lines = fileio.l(file_path)
    lines = list(filter(lambda x: s.isf(x, m) and not s.ct(x, "LINE_SEP"), lines))
    text = ""
    if (len(lines) > 0):
        text = ulist.select("ci", lines, select)
    return text


def do_ch(m):
    m = s.trim(s.cf_eq(m, "ch"))
    select = True
    file_path = cons.chf
    lines = fileio.l(file_path)
    lines = list(filter(lambda x: s.isf(s.cv_line_sep(x), m), lines))
    if (len(lines) > 0):
        text = ulist.select("ci", lines, select, max_size=10)
    return text


def do_cipa_st(m):
    m = s.cf(m, "cipa ")
    ci_content = get_text()
    cons.r_variables[m] = ci_content
    log("set system clipboard to variable: " + m)
    return ""


def do_cipa(m):  # @UnusedVariable
    ci_content = get_text()
    fileio.w(cons.p, [ci_content])
    log("set system clipboard to: " + cons.p)
    return ""


def do_cie(m):
    m = s.cf(m, "cie ")
    text = get_text()
    text = ops.do_ops(text, m)
    return text


def do_ids(m):
    files = filelistfind.list_files()
    files = ids.get_selected(files, m, "ci", "cin", "cisn")
    if (s.end(m, "ci")):
        func = fileio.get_file_path
    elif (s.end(m, "cin")):
        func = fileio.get_file_name
    elif (s.end(m, "cisn")):
        func = fileio.get_file_simple_name
    files = s.cv_(files, func)
    text = s.conn(files)
    return text


def do_list(m):  # @UnusedVariable
    files = filelistfind.list_files()
    text = s.conn(files)
    return text


def get_text():
    try:
        import win32clipboard  # @UnresolvedImport
        import win32con  # @UnresolvedImport
        win32clipboard.OpenClipboard()
        d = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        d = d.replace("\r\n", "\n")
        win32clipboard.CloseClipboard()
    except TypeError:
        d = ""
    return d


def set_text(aString):
    import win32clipboard  # @UnresolvedImport
    import win32con  # @UnresolvedImport
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(aString, win32con.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()


def logci(text):
    lines = text.split("\n")
    ulog.logl("add to system clipboard", lines)
    log()


def insert_chf(text):
    if (not cons.lasoff):
        fileio.insert_line(cons.chf, text)

