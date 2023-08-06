import ustring         as s
from   ulog            import log

import cons            as cons


def do_ops(line, cmds_s):  # cmd: "cf 1", "lf =" ...
    is_list = False
    if (isinstance(line, list)):
        line = s.conn(line)
        is_list = True
    cmds = s.get_parts(cmds_s, keys=["(;;)", ";;"])
    for cmd in cmds:
        op = get_ops(cmd)
        args = get_args(cmd)
        try:
            line_op_func = getattr(s, op)
        except:
            line_op_func = None
        if (line_op_func != None):
            if (op in cons.ops_as_one_line):
                line = s.do_line_op(line, line_op_func, args)
            else:
                line = s.do_lines_op(line, line_op_func, args)
    if (is_list):
        line = s.sp(line)
    return line


def get_ops(cmd):
    return s.lf(cmd, " ")


def get_args(cmd):
    if (s.ct(cmd, " ")):
        return s.clf(cmd, " ")
    return None

