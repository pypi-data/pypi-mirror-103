import ustring         as s
from   ulog            import log

import cons            as cons
import ids             as ids
import run             as run
import ulog            as ulog


def translate(m):
    if (m == "tl"):
        m = "run tasklist"
        cons.run_callback = tl_callback
    elif (s.st(m, "tl ")):
        cons.tasklist_filter = s.cf(m, "tl ")
        m = "run tasklist"
        cons.run_callback = tl_callback
    elif (m in ["kill", "ki"] or ids.is_ids(m, "ki")):
        m = do_kill(m)
    elif (m == "ns"):
        m = "run netstat -nao"
    elif (s.st(m, "ns ")):
        cons.tasklist_filter = s.cf(m, "ns ")
        m = "run netstat -nao"
        cons.run_callback = ns_callback
    return m


def tl_callback(lines):
    if (len(lines) > 0):
        h = lines[0:3]
        lines = lines[3:len(lines)]
        if (not cons.tasklist_filter == None):
            lines = s.filter_(lines, cons.tasklist_filter)
            cons.tasklist_filter = None

        def by_memory(x):
            x = s.cl(x, " K")
            x = s.rt(x, " ")
            x = s.cv(x, ",", "")
            x = int(x)
            return x

        lines = s.sort(lines, sort_key_func=by_memory, reverse=True)
        ulog.logt(10, h)
        ulog.logl("", lines)
        cons.tasklist_tasks = lines
        cons.run_callback = None


def do_kill(m):
    if (cons.tasklist_tasks):
        log()
        if (ids.is_ids(m, "ki")):
            to_kill_list = ids.get_selected(cons.tasklist_tasks, m, "ki")
        else:
            to_kill_list = cons.tasklist_tasks
        ulog.logl("kill tasks", to_kill_list)
        for m in to_kill_list:
            m = s.clf(m, "  ")
            m = s.trim(m)
            m = s.lf(m, " ")
            pid = m
            cmd = "taskkill /f /pid " + pid
            run.r(cmd)
        cons.tasklist_tasks = None
    return cons.ignore_cmd


def ns_callback(lines):
    if (len(lines) > 0):
        if (not cons.tasklist_filter == None):
            lines = s.filter_(lines, cons.tasklist_filter)
            cons.tasklist_filter = None
        ulog.log(lines)
        cons.run_callback = None

