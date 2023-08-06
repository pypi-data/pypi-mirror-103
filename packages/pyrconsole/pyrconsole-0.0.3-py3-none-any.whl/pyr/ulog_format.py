import cons            as cons
import ustring         as s

max_line_length = 170


def is_format_log_line(line):
    if (cons.always_format_log_line):
        return True
    if (len(line) > max_line_length):
        return True
    if (s.st(line, "case class ") and not s.end(s.trim(line), ",")):
        return True
    if (s.ct(line, "$$LINE_SEP$$")):
        return True
    if (s.st(line, "tar: ")):
        return True
    if (s.end(line, " ")):
        return True
    return False


def format_log_line(line, indent_size=0):
    if (is_json(line)):
        return format_json(line, indent_size)
    elif (is_xml(line)):
        return format_xml(line, indent_size)
    line = ci_line_sep(line, indent_size)
    line = tab(line, indent_size)
    line = long_file_path(line, indent_size)
    line = server_log(line, indent_size)
    line = format_svn(line, indent_size)
    line = tar_line(line, indent_size)
    line = ssh_ps_lines(line, indent_size)
    line = wrap_if_necessary(line, indent_size)
    return line


def format_json_or_xml(line, indent_size=0):
    if (is_json(line)):
        return format_json(line, indent_size)
    elif (is_xml(line)):
        return format_xml(line, indent_size)
    else:
        return line


def is_json(line):
    return s.is_wrapped(line, "{}", "[]")


def format_json(line, indent_size=0):
    try:
        import json
        formatted_json = json.dumps(json.loads(line), sort_keys=True, indent=4)
        formatted_json = format_line_indents(formatted_json, indent_size)
        return formatted_json
    except:
        return line


def is_xml(line):
    return s.is_wrapped(line, "<>")


def format_xml(line, indent_size=0):
    try:
        import xml.dom.minidom
        xml = xml.dom.minidom.parseString(line)
        formatted_xml = xml.toprettyxml()
        formatted_xml = s.cf(formatted_xml, "<?xml version=\"1.0\" ?>\n")
        formatted_xml = format_line_indents(formatted_xml, indent_size)
        return formatted_xml
    except:
        return line


def format_line_indents(line, indent_size):
    return s.cv(line, "\n", "\n" + s.get_indent_string(indent_size))


def ci_line_sep(line, indent_size):
    return s.cv_line_sep(line, indent_size)


def tab(line, indent_size):  # @UnusedVariable
    line = s.cv(line, "\t", "    ")
    return line


def long_file_path(line, indent_size):
    if (len(line) > max_line_length and s.is_single_line(line) and is_absolute_path(line)):
        idx = line.rfind(s.sep(), 0, max_line_length)
        indent = s.get_repeat_string(" ", indent_size + 4)
        line = line[0:idx + 1] + "\n" + indent + line[idx + 1:len(line)]
    return line


def server_log(line, indent_size):
    if (s.match(s.lf(line, " "), "\\d\\d\\d\\d-\\d\\d-\\d\\d")):
        indent = s.get_repeat_string(" ", indent_size + 4 + len(s.lf(line, "[")))
        for k in ["]", ":", "."]:
            line = s.cv(line, k + " ", k + " \n" + indent)
    return line


def format_svn(line, indent_size):
    for k in ["svn st ", "svn diff "]:
        if (s.ct(line, k)):
            a = s.lfw(line, k)
            b = s.rt(line, k)
            indent = s.get_repeat_string(" ", indent_size + len(a))
            b = s.cv(b, " ", " \n" + indent)
            line = a + b
    return line


def tar_line(line, indent_size):
    for k in ["tar: "]:
        if (s.st(line, k)):
            n = len(s.lf(line, "=")) + 6 + indent_size
            line = s.cv(line, "|", "|\n" + s.get_indent_string(n))
    return line


def ssh_ps_lines(line, indent_size):
    if (len(line) > max_line_length and s.ct(line, " /")):
        import ssh
        if (ssh.is_ssh()):
            a = s.lf(line, " /")
            b = s.clf(line, " /")
            b = s.cv(b, " ", "\n" + s.get_indent_string(len(a) + 5 + indent_size))
            b = s.cv(b, ":/", ":\n" + s.get_indent_string(len(a) + 5 + indent_size + 4) + "/")
            line = a + " /" + b
    return line


def wrap_if_necessary(line, indent_size):  # @UnusedVariable
    if (s.end(line, " ")):
        line = s.wrap(line)
    return line


def is_absolute_path(f):
    return s.st(f, "/") or f[1] == ":"


def format_lines(lines):
    is_one_line = False
    if (isinstance(lines, str)):
        lines = s.sp(lines)
        is_one_line = True
    r = []
    for line in lines:
        if (is_format_log_line(line)):
            line = format_log_line(line)
        r += [line]
    lines = r
    if (is_one_line):
        lines = s.conn(lines)
    return lines

