import ustring         as s
from   ulog            import log

import cons            as cons
import ulog            as ulog
import env             as env
import fileio          as fileio
import ulist           as ulist

# if ends with "_", it means no space, like "bvxxx"
keys = [
    "fs",   "f",      "q",      "r",      "m",
    "mq",   "l",      "t",      "taoi",   " cv",
    "ex",   "select", "update", "delete", "create",
    " dup", "svn",    "s",      "fmk",    "bv_",
    "ssh",  "hdfs",   "ftp",    "mysql",  "sw_",
    "rn",   "f._",    "tar",    "g",
]

last_commands_mapping = {
    "b": {
        "rm" : "b-",
        "a"  : "b+",
        "n"  : "b=",
        " "  : "b:",
        "v"  : "bv",
    },
    "st": {
        "si" : "svni",
        "sl" : "slog",
    },
    "sd": {
        "si" : "svni",
        "sl" : "slog",
    },
    "sup": {
        "si" : "svni",
        "sl" : "slog",
    },
    "gmdr": {
        "csv" : "gmdrcsv",
        "sql" : "gmdrsql",
        "res" : "gmdrres",
        "hr"  : "gmdrhdfsreport",
        "en"  : "gmdrmdrpy",
        "re"  : "gmdrreport",
        "wo"  : "gmdrwork",
        "co"  : "gmdrconf",
        "ppk" : "gmdrppk",
        "ro"  : "gmdrroot",
        "ls"  : "gmdrlogstatistics",
        "ss"  : "gmdrsparkstatistics",
        "hs"  : "gmdrhdfsstatistics",
        "ns"  : "gmdrnodestatistics",
        "cl"  : "gmdrcleanandst",
    },
    "gm": {
        "csv" : "gmdrcsv",
        "sql" : "gmdrsql",
        "res" : "gmdrres",
        "hr"  : "gmdrhdfsreport",
        "en"  : "gmdrmdrpy",
        "re"  : "gmdrreport",
        "wo"  : "gmdrwork",
        "co"  : "gmdrconf",
        "ppk" : "gmdrppk",
        "ro"  : "gmdrroot",
        "ls"  : "gmdrlogstatistics",
        "ss"  : "gmdrsparkstatistics",
        "hs"  : "gmdrhdfsstatistics",
        "ns"  : "gmdrnodestatistics",
        "cl"  : "gmdrcleanandst",
    },
}


def translate(m):
    m00 = m
    m = record_last_op(m)
    m = get_last_op(m)
    ulog.log_trans(m00, m)
    return m


def record_last_op(m):
    for k in keys:
        st_k = None
        if (s.end(k, "_")):
            st_k = s.cl(k, "_")
            k = st_k
        else:
            st_k = k + " "
        if (s.st(m, st_k)):
            f = env.lastop_f(k + "_")
            fileio.insert_line(f, m)
    return m


def get_last_op(m):
    for k in keys:
        if (s.end(k, "_")):
            k = s.cl(k, "_")
        h_ = " " + k + "h"
        f = env.lastop_f(k + "_")
        if (m == h_ + "f"):  # open file
            m = ".. g {0};f[]".format(f)
        elif (m == h_ + "g"):  # go file
            m = "g {0}".format(f)
        elif (m == " " + k):  # use the latest one
            lines = fileio.l(f)
            if (len(lines) > 0):
                m = lines[0]
            else:
                m = cons.ignore_cmd
        elif (m == h_ or s.st(m, h_)):  # select
            lines = fileio.l(f)
            if (s.st(m, h_)):
                con = s.cf(m, h_)
                con = s.trimleft(con)
                lines = s._filter_(lines, s.isf, con)
            m = ulist.select(k, lines)
            if (m == None or m == ""):
                m = cons.ignore_cmd
            else:
                record_last_op(m)
    return m


def handle(m):
    pass


def last_command(m):
    if (m == " "):
        if (cons.space_command == None):
            m = cons.last_command
        else:
            m = cons.space_command
            cons.space_command = None
    elif(m not in ["-v", "-vp", "-vt", "vs", "vsa"]):
        m00 = m
        m = last_command_translate(m)
        if (not m == m00):
            pass
        else:
            cons.last_command = m
    return m


def last_command_translate(m):
    last = cons.last_command
    for k in last_commands_mapping:
        if (last == k):
            for op in last_commands_mapping[k]:
                if (m == op):
                    m = last_commands_mapping[k][op]
                if (s.st(m, op)):
                    m = s.trim(s.cf(m, op))
                    m = last_commands_mapping[k][op] + m
    return m


def do_get_last_input(k):
    f = env.lastop_f(k + "_")
    lines = fileio.l(f)
    if (len(lines) > 0):
        m = lines[0]
    else:
        m = cons.ignore_cmd
    return m


def do_put_last_input(k, line):
    f = env.lastop_f(k + "_")
    fileio.insert_line(f, line)

