import ustring         as s
from   ulog            import log

import cons            as cons
import ulog            as ulog
import filelistfind    as filelistfind
import fileio          as fileio

src_definition = {
    "common": {
        "keys": {
            "tr"  : "def translate(",
            "han" : "def handle(",
        }
    },
    "cons": {
        "keys": {
            "br"        : "branches =",
            "ops"       : "# ops",
            "ci_ops"    : "ci_ops =",
            "mysql_map" : "ci_mysql_map = {",
            "go"        : "file_go_map = {",
            "cmds"      : "quick_cmds = {",
            "web_alias" : "web_alias = {",
            "run_cmds"  : "run_cmds = {",
        }
    },
    "ci": {
        "keys": {
            "my" : "def mysql(m):",
        }
    },
    "ustr": {
        "file": "ustring",
        "keys": {
            "fp"   : "def format_paragraph(s)",
            "isf"  : "def isf(s, p):",
            "ctic" : "def ctic_con(s, p):",
        }
    },
    "src": {
        "keys": {
            "def"          : "src_definition = {",
            "u"            : "u_ = {[=2]",
            "duiqi_parts"  : "duiqi_parts = {[=2]",
            "duiqi2_parts" : "duiqi2_parts = {[=2]",
            "sort_parts"   : "sort_parts = {[=2]",
        }
    },
    "fileli": {
        "file": "filelistfind",
        "keys": {
            "mf" : "def match_find_condition(line_number, line):",
        }
    },
    "filego": {
        "keys": {
            "h123" : "def h123(m):",
        }
    },
    "fileedit": {
        "keys": {
            "ql" : "def ql(m):",
            "r"  : "def do_replace_lines(m):",
        }
    },
    "ulog_format": {
        "keys": {
            "fl" : "def format_log_line(",
        }
    },
    "ulist": {
        "keys": {
            "select" : "def select(n",
        }
    },
    "translate": {
        "keys": {
            "eis"     : "def eis(m):",
            "est"     : "def est(m):",
            "est_key" : "def is_excluded_key(key):",
        }
    },
    "lastop": {
        "keys": {
            "keys"         : "keys = [",
            "last_command" : "def last_command_translate(m):",
        }
    },
    "ssh": {
        "keys": {
            "ssh"     : "def do_ssh_in_r(m):",
            "default" : "ssh_default =",
        }
    },
    "ftp": {
        "keys": {
            "ftp"     : "def do_ftp_in_r(m):",
            "default" : "ftp_default =",
        }
    },
    "mysql": {
        "keys": {
            "mysql"   : "def do_mysql_in_r(m):",
            "default" : "mysql_default =",
        }
    },
    "uhdfs": {
        "keys": {
            "hdfs"    : "def do_hdfs_in_r(m):",
            "default" : "hdfs_default =",
        }
    },
    "filesystem": {
        "keys": {
            "is": "not_cmds_is = [",
            "st": "not_cmds_st = [",
            "match": "not_cmds_match = [",
        }
    },
    "xiaomi": {
        "keys": {
            "huilv": "def do_huilv(m):",
        }
    },
    "cmds_complex": {
        "keys": {
            "comp": "def translate(m):",
        }
    },
    "fileopen": {
        "keys": {
            "ue": "# is ultraedit file",
        }
    },
}

u_ = {
    "ftpd"   : "ftp_default",
    "hdfsd"  : "uhdfs_default",
    "mysqld" : "mysql_default",
    "sshd"   : "ssh_default",
    "ubr"    : "cons_br",
    "ucc"    : "cmds_complex_comp",
    "uciops" : "cons_ci_ops",
    "ucmds"  : "cons_cmds",
    "uct"    : "ustr_ctic",
    "uctic"  : "ustr_ctic",
    "udq2p"  : "src_duiqi2_parts",
    "udqp"   : "src_duiqi_parts",
    "uei"    : "translate_eis",
    "ues"    : "translate_est",
    "uesk"   : "translate_est_key",
    "ufl"    : "ulog_format_fl",
    "ufp"    : "ustr_fp",
    "ufsis"  : "filesystem_is",
    "ufsma"  : "filesystem_match",
    "ufsst"  : "filesystem_st",
    "uftp"   : "ftp_ftp",
    "ugo"    : "cons_go",
    "uh123"  : "filego_h123",
    "uhdfs"  : "uhdfs_hdfs",
    "uhl"    : "xiaomi_huilv",
    "uisf"   : "ustr_isf",
    "ulas"   : "lastop_keys",
    "ulc"    : "lastop_last_command",
    "umf"    : "fileli_mf",
    "umy"    : "ci_my",
    "umymap" : "cons_mysql_map",
    "umysql" : "mysql_mysql",
    "uops"   : "cons_ops",
    "uql"    : "fileedit_ql",
    "ur"     : "fileedit_r",
    "urun"   : "cons_run_cmds",
    "usel"   : "ulist_select",
    "usop"   : "src_sort_parts",
    "usrc"   : "src_def",
    "ussh"   : "ssh_ssh",
    "uu"     : "src_u",
    "uue"    : "fileopen_ue",
    "uweb"   : "cons_web_alias",
}

duiqi_parts = {
    "ftp": [
        "\"359\": {",
        "\"local\": {",
        "ftp_sites_shortcuts = {",
        "months_map = {",
    ],
    "ssh": [
        "\"5106\": {",
        "\"7121\": {",
        "\"3133\": {",
        "\"3127\": {",
        "\"5128\": {",
        "\"2144\": {",
        "\"2150\": {",
        "\"282\": {",
        "\"283\": {",
        "\"199\": {",
        "\"199_pub\": {",
        "\"1110\": {",
        "\"178\": {",
        "\"167\": {",
        "\"1251\": {",
        "\"7163\": {",
        "\"3185\": {",
        "\"3186\": {",
        "\"3127_bj\": {",
        "\"3129\": {",
        "\"759\": {",
        "\"760\": {",
        "\"761\": {",
        "ssh_sites_shortcuts = {",
        "ssh_ppks = {",
        "ssh_quick_cmds = {",
        "ssh_quick_cmds_st = {",
    ],
    "mysql": [
        "\"local\": {",
        "\"local_viaops_config_db\": {",
        "mysql_sites_shortcuts = {",
        "mysql_quick_cmds = {",
        "mysql_column_types = {",
    ],
    "uhdfs": [
        "\"local\": {",
        "\"zhihui_test\": {",
        "\"282\": {",
        "hdfs_sites_shortcuts = {",
    ],
    "ci": [
        "jar_map = {",
        "ear_map = {",
        "lo_map = {",
        "to = {",
    ],
    "cons": [
        "find_shortcuts = {",
        "file_go_map = {",
        "file_open_map = {",
        "branches = {",
        "branches_sw = {",
        "ci_ops = {",
        "ci_mysql_map = {",
        "run_cmds = {",
        "quick_cmds = {",
        "quick_cmds_st = {",
        "web_alias = {",
    ],
    "daiban": [
        "b_trans_map = {",
    ],
    "filego": [
        "support_name = {",
    ],
    "gxxx": [
        "ops = {",
    ],
    "run": [
        "run_callbacks = {",
    ],
    "sa": [
        "map_ = {",
    ],
    "src": [
        "\"keys\": {[16]",
        "u_ = {[=2]",
    ],
    "uudp": [
        "\"3127\": {",
        "\"local\": {",
    ],
    "ustring": [
        "ju_hao[=1][duiqi =]",
    ],
    "xiaomi": [
        "gu_ben = {",
        "gu_jia = {",
        "huilv_help = {",
        "\"xm\": {",
        "\"tx\": {",
    ],
    "openweb": [
        "notification_models_help = {",
    ],
    "subconsole": [
        "wildfly_upgrade_cmds = {",
        "do_cmds = {",
    ],
    "cal": [
        "cal_help = {",
    ],
    "lastop": [
        "\"b\": {",
        "\"st\": {",
    ],
}

duiqi2_parts = {
    "filesystem": [
        "not_cmds_is = [",
        "not_cmds_st = [",
        "not_cmds_match = [",
    ],
    "cons": [
        "ops = [",
        "ops_as_one_line = [",
    ],
    "lastop": [
        "keys = [",
    ],
    "ustring": [
        "connectors = [",
    ],
}

sort_parts = {
    "rconsole": [
        "import cal",
    ],
    "cons": [
        "ci_ops = {",
        "quick_cmds = {",
    ],
    "src": [
        "u_ = {[=2]",
    ],
}


def translate(m):
    if(m not in ["fileopen f"]):
        m00 = m
        m = u(m)
        m = src(m)
        m = gpos(m)
        m = kc(m)
        m = format_src(m)
        ulog.log_trans(m00, m)
        return m
    return m


def u(m):
    if (u_.__contains__(m)):
        m = u_[m]
    return m


def src(m):
    for prefix in get_prefixes(m):
        r = do_src(prefix, m)
        if (r):
            m = r
            break
    return m


def gpos(m):
    if (s.st(m, "gpos ")):
        m = s.cf(m, "gpos ")
        f = s.lf(m, " ")
        k = s.clf(m, " ")
        m = ".. {0};fs {1};1[]".format(f, k)
    return m


def kc(m):
    if (s.st(m, "kc ")):
        m = s.cf(m, "kc ")
        log("kco f: " + m)
        m = ".. grc;fs commandKCODE_{0};1".format(m)
    return m


def format_src(m):
    if (m == "fsrc"):
        m = ".. dqsrc;dq2src;sosrc"
    m = duiqi(m)
    m = duiqi2(m)
    m = sort(m)
    return m


def duiqi(m):
    if (m == "dqsrc"):
        r = []
        for k in duiqi_parts.keys():
            r += [k + "g"]
            find_keys = duiqi_parts[k]
            for find_key in find_keys:
                if (s.has_wrapped(find_key, "[duiqi ]")):
                    duiqi_op = "duiqi " + s.find_wrapped(find_key, "[duiqi ]")
                    find_key = s.rm_wrapped(find_key, "[duiqi ]", no_space=True)
                else:
                    duiqi_op = "duiqi"
                if (s.end(find_key, "]")):
                    times_s = s.find_wrapped(find_key, "[]")
                    find_key = s.crt(find_key, "[")
                    if (s.st(times_s, "=")):
                        r += ["fs " + find_key, "pick " + s.cf(times_s, "="), ml_key(find_key), duiqi_op + "[]", "c"]
                    else:
                        times = int(times_s)
                        for i in range(times):
                            r += ["fs " + find_key, "pick " + str(i + 1), ml_key(find_key), duiqi_op + "[]", "c"]
                else:
                    r += ["fs " + find_key, ml_key(find_key), duiqi_op + "[]", "c"]
        m = ".. " + s.conn(r, ";") + ";b2"
    return m


def duiqi2(m):
    if (m == "dq2src"):
        r = []
        for k in duiqi2_parts.keys():
            r += [k + "g"]
            find_keys = duiqi2_parts[k]
            for find_key in find_keys:
                if (s.end(find_key, "]")):
                    times_s = s.find_wrapped(find_key, "[]")
                    find_key = s.crt(find_key, "[")
                    if (s.st(times_s, "=")):
                        r += ["fs " + find_key, "pick " + s.cf(times_s, "="), ml_key(find_key), "duiqi2[]", "c"]
                    else:
                        times = int(times_s)
                        for i in range(times):
                            r += ["fs " + find_key, "pick " + str(i + 1), ml_key(find_key), "duiqi2[]", "c"]
                else:
                    r += ["fs " + find_key, ml_key(find_key), "duiqi2[]", "c"]
        m = ".. " + s.conn(r, ";") + ";b2"
    return m


def sort(m):
    if (m == "sosrc"):
        r = []
        for k in sort_parts.keys():
            r += [k + "g"]
            find_keys = sort_parts[k]
            for find_key in find_keys:
                if (s.end(find_key, "]")):
                    times_s = s.find_wrapped(find_key, "[]")
                    find_key = s.crt(find_key, "[")
                    if (s.st(times_s, "=")):
                        r += ["fs " + find_key, "pick " + s.cf(times_s, "="), ml_key(find_key), "sort[]", "c"]
                    else:
                        times = int(times_s)
                        for i in range(times):
                            r += ["fs " + find_key, "pick " + str(i + 1), ml_key(find_key), "sort[]", "c"]
                else:
                    r += ["fs " + find_key, ml_key(find_key), "sort[]", "c"]
        m = ".. " + s.conn(r, ";") + ";b2"
    return m


def ml_key(find_key):
    if (s.end(find_key, "{", "[")):
        return "ml"
    else:
        return "mls"


def get_prefixes(m):
    prefixes = []
    prefixes += do_get_prefixes(m)
    prefixes += src_definition.keys()
    return prefixes


def do_get_prefixes(m):
    if (s.end(m, "f", "g", "tr", "han")):
        m = s.cl(m, "f", "g", "tr", "han")
        if (len(m) >= 3 or fileio.exists(get_pyr_src_file(m))):
            files = filelistfind.list_dir_(get_pyr_src_dir(), con=s.wrap(m, "st()"))
            if (len(files) > 0):
                if (src_definition.__contains__(m)):
                    return []
                else:
                    src_definition[m] = {"file": files[0]}
                return [m]
    return []


def do_src(prefix, m):
    if (s.st(m, prefix)):
        k = s.cf(m, prefix)
        k = s.cf(k, "_", " ")
        def_ = src_definition[prefix]
        if (def_.__contains__("file")):
            file = def_["file"]
            if (not s.end(file, ".py")):
                file = get_pyr_src_file(file)
                def_["file"] = file
        else:
            def_["file"] = get_pyr_src_file(prefix)
        file = def_["file"]
        if (k == "f"):
            return ".. g {0};f[]".format(file)
        elif (k == "g"):
            return "g {0}".format(file)
        search_key = get_search_key(prefix, k)
        if (search_key):
            pos = "1"
            if (s.end(search_key, "]")):
                pos = s.find_wrapped(search_key, "[=]")
                search_key = s.lf(search_key, "[")
            return ".. g {0};fs {1};{2}[]".format(file, search_key, pos)
    return None


def get_search_key(prefix, k):
    search_key = do_get_search_key(prefix, k)
    if (not search_key):
        search_key = do_get_search_key("common", k)
    return search_key


def do_get_search_key(prefix, k):
    def_ = src_definition[prefix]
    if (def_.__contains__("keys")):
        keys = def_["keys"]
        if (keys.__contains__(k)):
            return keys[k]
    return None


def get_pyr_src_file(n):
    return get_pyr_src_dir() + "\\" + n + ".py"


def get_pyr_src_dir():
    return cons.pyr_dir

