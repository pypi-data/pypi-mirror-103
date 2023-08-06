import ustring         as s
from   ulog            import log
from   ulog            import logd
from   ulog            import logp

import cal             as cal
import ci              as ci
import cmds            as cmds
import cons            as cons
import daiban          as daiban
import env             as env
import excel           as excel
import filebackup_     as filebackup_
import filecopy        as filecopy
import filecopy_n      as filecopy_n
import filedelete      as filedelete
import fileedit        as fileedit
import filego          as filego
import fileio          as fileio
import filelistfind    as filelistfind
import fileopen        as fileopen
import filerename      as filerename
import filesystem      as filesystem
import fileview        as fileview
import ftp             as ftp
import git             as git
import gxxx            as gxxx
import kco             as kco
import lastop          as lastop
import ms              as ms
import mysql           as mysql
import openweb         as openweb
import run             as run
import rvar            as rvar
import sa              as sa
import src             as src
import ssh             as ssh
import stock           as stock
import subconsole      as subconsole
import svn             as svn
import tar             as tar
import translate       as trans
import uhdfs           as uhdfs
import ulog            as ulog
import utime           as utime
import uudp            as uudp
import uzip            as uzip
import xiaomi          as xiaomi


class rconsole:

    def do_run(self):
        self.init()
        log("Welcome to R Console [Python]")
        log("")

        filesystem.fs_init()
        filelistfind.cd(cons.p)
        while True:
            cons.logd_el = False
            m = s.input_async(s.get_input_p() + ">")
            ulog.start_rl()
            ulog.do_w_rl(cons.p + ">" + m)
            if (m == ""):
                continue
            if (m == "q"):
                break
            try:
                self.do_run__(m)
            except:
                import traceback
                traceback.print_exc()
                log()
        filesystem.fs_clean_up()
        env.clean_up()
    
    def do_run__(self, m):
        m = env.record_last_p(m)
        m = cmds.record_next_prev_cmd(m)
        m = lastop.last_command(m)
        start = s.nowts()
        self.translate_and_handle(m)
        logp("rconsole.handle", start)
        log()
    
    def translate_and_handle(self, m):
        increase_log_tab_n = 0
        decrease_log_tab_n = 0
        nawlog = False
        awlog = False
        alog = False
        nalog = False
        if (not ms.is_multi_step(m)):
            m, increase_log_tab_n = ms.get_increase_logtab(m)
            m, decrease_log_tab_n = ms.get_decrease_logtab(m)
            nawlog = ms.is_nawlog(m)
            awlog = ms.is_awlog(m)
            alog = ms.is_alog(m)
            nalog = ms.is_nalog(m)
            m = ms.rm_log_marks(m)

        try:
            ulog.increase_log_tab(increase_log_tab_n, all_=True)
            ulog.nawlog(nawlog)
            ulog.alog(alog)
            m = self.translate(m)
            if (not m == ""):
                m00 = m
                if (ms.is_multi_step(m)):
                    silent = ms.is_ms_silent(m)
                    m = ms.rm_ms(m)
                    cmds = s.get_parts(m)
                    try:
                        ulog.silent(silent)
                        for cmd in cmds:
                            if (not silent):
                                ms.log_step(cmd)
                            logd(cmd, need_el=True)
                            logd()
                            self.translate_and_handle(cmd)
                    finally:
                        ulog.no_silent(silent)
                else:
                    self.handle(m)
                self.post_handle(m00)
        finally:
            ulog.nalog(nalog)
            ulog.awlog(awlog)
            ulog.decrease_log_tab(decrease_log_tab_n, all_=True)

    def translate(self, m):

        if (self.no_translate(m)):
            return m

        while True:
            m00 = m
            m = env.translate(m)
            m = lastop.translate(m)
            m = filesystem.translate(m)
            m = ssh.translate(m)
            m = ftp.translate(m)
            m = mysql.translate(m)
            m = uhdfs.translate(m)
            m = uudp.translate(m)
            m = cmds.translate(m)
            m = rvar.translate(m)
            m = ci.translate(m)
            m = cal.translate(m)
            m = sa.translate(m)
            m = git.translate(m)
            m = svn.translate(m)
            m = src.translate(m)
            m = tar.translate(m)
            m = uzip.translate(m)
            m = daiban.translate(m)
            m = utime.translate(m)
            m = run.translate(m)
            m = xiaomi.translate(m)
            m = subconsole.translate(m)
            m = filebackup_.translate(m)
            m = filecopy.translate(m)
            m = filecopy_n.translate(m)
            m = filedelete.translate(m)
            m = fileedit.translate(m)
            m = fileview.translate(m)
            m = fileopen.translate(m)
            m = filelistfind.translate(m)
            m = fileio.translate(m)
            m = filerename.translate(m)
            m = filego.translate(m)
            m = ulog.translate(m)
            m = kco.translate(m)
            m = stock.translate(m)
            m = excel.translate(m)
            m = gxxx.translate(m)
            m = openweb.translate0(m)
            m = trans.translate(m)
            m = openweb.translate(m)
            if (m == m00):
                break

        logd()
        return m

    def no_translate(self, m):
        if (filelistfind.no_translate(m)):
            return True
        return False

    def handle(self, m):
        if (m == cons.ignore_cmd):
            pass
        elif (s.st(m, "env ")):
            m = s.cf(m, "env ")
            env.handle(m)
        elif (s.st(m, "g ")):
            m = s.cf(m, "g ")
            filego.handle(m)
        elif (s.st(m, "run ")):
            m = s.cf(m, "run ")
            run.handle(m)
        elif (s.st(m, "rvar ")):
            m = s.cf(m, "rvar ")
            rvar.handle(m)
        elif (s.st(m, "ci ")):
            m = s.cf(m, "ci ")
            ci.handle(m)
        elif (s.st(m, "cal ")):
            m = s.cf(m, "cal ")
            cal.handle(m)
        elif (s.st(m, "ulog ")):
            m = s.cf(m, "ulog ")
            ulog.handle(m)
        elif (s.st(m, "s ")):
            m = s.cf(m, "s ")
            openweb.handle(m)
        elif (s.st(m, "tar ")):
            m = s.cf(m, "tar ")
            tar.handle(m)
        elif (s.st(m, "filelistfind ")):
            m = s.cf(m, "filelistfind ")
            filelistfind.handle(m)
        elif (s.st(m, "filecopy ")):
            m = s.cf(m, "filecopy ")
            filecopy.handle(m)
        elif (s.st(m, "filedelete ")):
            m = s.cf(m, "filedelete ")
            filedelete.handle(m)
        elif (s.st(m, "fileedit ")):
            m = s.cf(m, "fileedit ")
            fileedit.handle(m)
        elif (s.st(m, "fileview ")):
            m = s.cf(m, "fileview ")
            fileview.handle(m)
        elif (s.st(m, "fileopen ")):
            m = s.cf(m, "fileopen ")
            fileopen.handle(m)
        elif (s.st(m, "fileio ")):
            m = s.cf(m, "fileio ")
            fileio.handle(m)
        elif (s.st(m, "filerename ")):
            m = s.cf(m, "filerename ")
            filerename.handle(m)
        elif (s.st(m, "hdfs ")):
            m = s.cf(m, "hdfs ")
            uhdfs.handle(m)
        elif (s.st(m, "xiaomi ")):
            m = s.cf(m, "xiaomi ")
            xiaomi.handle(m)
        elif (s.st(m, "kco ")):
            m = s.cf(m, "kco ")
            kco.handle(m)
        elif (s.st(m, "stock ")):
            m = s.cf(m, "stock ")
            stock.handle(m)
        elif (s.st(m, "excel ")):
            m = s.cf(m, "excel ")
            excel.handle(m)
        else:
            run.handle_bat(m)

    def post_handle(self, m):
        if (cons.post_handle.__contains__(m)):
            func = cons.post_handle[m]
            func()
            cons.post_handle.pop(m)

    def init(self):
        if (not fileio.exists(cons.diary)):
            import os
            cons.cwd_dir = os.getcwd()
            cons.rn_dir = cons.cwd_dir
            cons.bat_dir = s.cwd_("bat")
            fileio.mkdir(cons.bat_dir)
            cons.tar = s.cwd_("typeandrun/Config.ini")
            cons.pyr_dir = cons.cwd_dir
            cons.alogs_dir = s.cwd_("alogs")
            fileio.mkdir(cons.alogs_dir)
            cons.lastop_dir = s.cwd_("alogs/lastop")
            fileio.mkdir(cons.lastop_dir)
            cons.chf = s.cwd_("alogs/lastop/ci_history.txt")
            cons.fhf = s.cwd_("alogs/lastop/p_history.txt")
            cc_dirs_dir = s.cwd_("alogs/ccReplace")
            cons.default_output_file = s.cwd_("alogs/output.log")
            cons.linux_files = s.cwd_("alogs/linux_files")
            fileio.mkdir(cons.linux_files)
            cons.latest_open_file = s.cwd_("alogs/linux_files/latest_open_file.txt")
            fileio.mkdir(cc_dirs_dir)
            cons.cc_dirs = s.cwd_("ccReplace/ccCtrlCCtrlVDirs.txt")
            if (s.is_linux()):
                cons.p = "/home"
            else:
                cons.p = "C:"

r = rconsole()
cons.r = r
r.do_run()

