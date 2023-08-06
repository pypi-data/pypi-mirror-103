import ustring         as s
from   ulog            import log
from   abc             import abstractmethod

import os

import cons            as cons
import env             as env
import filebackup_     as filebackup_
import filecopy        as filecopy
import filedelete      as filedelete
import filego          as filego
import fileio          as fileio
import filelistfind    as filelistfind
import fileopen        as fileopen
import tar             as tar
import ulog            as ulog


def translate(m):
    m00 = m
    m = g(m)
    m = fs_translate(m)
    ulog.log_trans(m00, m)
    return m


def g(m):
    if (m == "g"):
        if (fileio.exists(cons.latest_open_file)):
            f = fileio.l(cons.latest_open_file)[0]
            clean_latest_open_file()
            m = "g " + f
    return m


def clean_latest_open_file():
    try:
        ulog.tmp_silent()
        filedelete.do_del_file(cons.latest_open_file)
    finally:
        ulog.no_tmp_silent()


def fs_translate(m):
    m = cons.file_system.translate(m)
    return m


def fs_init():
    if (cons.file_system == None):
        cons.local_file_system = local_file_system()
        cons.file_system = cons.local_file_system


def fs_clean_up():
    if (not cons.file_system.type_ == "local"):
        cons.file_system.clean_up()
        cons.file_system = cons.local_file_system


def fs_download_file(from_file, to_file):
    fs_set_do_copy_callback()
    s._r_(fs_to_python_file(fs_type(from_file)) + ".do_download_file__", from_file, to_file)


def fs_download_dir(from_file, to_file):
    fs_set_do_copy_callback()
    s._r_(fs_to_python_file(fs_type(from_file)) + ".do_download_dir__", from_file, to_file)


def fs_is_file(f):
    k = fs_host_as_key(f)
    return cons.file_systems[k].is_file(s.cf(f, k))


def fs_get_file_timestamp(f):
    k = fs_host_as_key(f)
    return cons.file_systems[k].get_file_timestamp(s.cf(f, k))


def fs_prepare_file_system(f):
    k = fs_host_as_key(f)
    if (not cons.file_systems.__contains__(k)):
        cons.file_systems[k] = s._r_(fs_to_python_file(fs_type(f)) + ".prepare_file_system", fs_ip(f))


def fs_host(f):
    return s.find_wrapped(f, "[]")


def fs_host_as_key(f):
    return s.wrap(fs_host(f), "[]")


def fs_ip(f):
    return s.clf(fs_host(f), ":")


def fs_type(f):
    return s.lf(fs_host(f), ":")


def fs_to_python_file(fs_type):
    if (fs_type == "hdfs"):
        return "uhdfs"
    return fs_type


def fs_set_do_copy_callback():
    if (cons.copy_callback == None):
        cons.copy_callback = fs_do_copy_callback


def fs_do_copy_callback(files):
    for f in files:
        k = fs_host_as_key(f)
        if (cons.file_systems.__contains__(k)):
            cons.file_systems.pop(k).clean_up()
    cons.copy_callback = None


class client:
    
    type = ""
    site = None
    ip = ""
    port = 0
    user = ""
    pwd = ""
    
    old_p = None
    old_sep = None
    
    def __init__(self, site):
        self.site = site
        self.ip = site["ip"]
        self.port = site["port"]
        self.user = site["user"]
        self.pwd = site["pwd"]
        self.old_p = cons.p
        cons.p = site["dir"]
        self.old_sep = cons.sep
        cons.sep = "/"
        self.init()
    
    def init(self):
        env.reset()
    
    def close(self):
        cons.p = self.old_p
        cons.sep = self.old_sep


class file_system:

    not_cmds_is = [
        "l",       "ls",   "v",      "a",      "g",
        "r",       "dx",   "zd",     "zx",     "sj",
        "zj",      "zy",   "f/",     "c/",     "cps",
        "-v",      "-vp",  "env -v", "fh",     "ch",
        "env -vp", "ca",   "env ca", "va",     "ns",
        "ci",      "-",    "cc",     "cv",     "ccc",
        "ccv",     "f",    "f.",     "fs.",    "q.",
        "mq.",     "gf",   "cic",    "cicfmt", "fmk",
        "f.mk",    "fmk ", "gl",
    ]
    
    not_cmds_st = [
        " ",         "l ",          "g ",        "q ",        "f ",
        "fs ",       "/",           "\\",        "w;",        "wo;",
        "bh",        "by",          "zd",        "zx",        "zj",
        "zy",        "env ",        "f.",        "c.",        "ci ",
        "run ",      "rvar ",       "cal ",      "ulog ",     "s ",
        "tar ",      "ns ",         "rm ",       "md ",       "filelistfind ",
        "filecopy ", "filedelete ", "fileedit ", "fileview ", "fileopen ",
        "fileio ",   "filerename ", "hdfs ",     "xiaomi ",   "kco ",
        "stock ",    "excel ",      "  File ",   "mq ",       "and",
        "or",        "not",         "is",        "st",        "end",
        "..",        "fmk",
    ]
    
    not_cmds_match = [
        " \\d+", "\\d+-", "(\\d+ )+-", "\\d+cc",       "(\\d+ )+cc",
        "\\d+",  "\\d+f", "(\\d+ )+f", "(\\d+ )+\\d+",
    ]

    client_ = None
    type_ = None
    
    is_file_map = dict()
    ts_map = dict()
    ts_map_s = dict()
    size_map = dict()
    size_map_s = dict()
    list_map = dict()
    file_lines_map = dict()
    
    def __init__(self, client_=None, type_="local"):
        self.client_ = client_
        self.type_ = type_
        self.init_p()
        self.do_logd_init()
    
    def init_p(self):
        pass
    
    def do_logd_init(self):
        if (not self.type_ == "local"):
            ulog.logd("init     file system: [{0}:{1}]".format(self.type_, self.c().ip))
    
    def is_local(self):
        return self.type_ == "local"

    def is_not_local(self):
        return not self.is_local()
    
    def is_dir(self, p):
        return not self.is_file(p)
    
    def is_file(self, p):  # TODO: handle cc [ip]xxx
        if (p == "/"):
            return False
        if (s.is_windows_path(p)):
            return cons.local_file_system.is_file(p)
        if (self.is_file_map.__contains__(p)):
            return self.is_file_map[p]
        else:
            self.is_file_map[p] = self.do_is_file(p)
            return self.is_file_map[p]
    
    @abstractmethod
    def do_is_file(self, p):
        pass
    
    def get_parent(self, p):
        if (s.is_windows_path(p)):
            return cons.local_file_system.get_parent(p)
        p = s.crt(p, "/")
        if (p == ""):
            p = "/"
        return p
    
    def get_file_name(self, p):
        if (s.is_windows_path(p)):
            return cons.local_file_system.get_file_name(p)
        return s.rt(p, "/")
    
    def iglob(self, search_key=None, recursive=False, dir_=None):  # @UnusedVariable
        if (not dir_ == None and s.is_windows_path(dir_)):
            return cons.local_file_system.iglob(search_key=search_key, recursive=recursive, dir_=dir_)
        if (dir_ == None):
            dir_ = cons.p
        if (recursive):
            k = dir_ + "(a)"
        else:
            k = dir_
        if (self.list_map.__contains__(k)):
            return self.list_map[k]
        self.list_map[k] = self.do_iglob(search_key=search_key, recursive=recursive, dir_=dir_)
        return self.list_map[k]
    
    def do_iglob(self, search_key=None, recursive=False, dir_=None):  # @UnusedVariable
        l = []
        for entry in self.mlsd(recursive=recursive, dir_=dir_):
            n = entry[0]
            size_ = entry[1]["size"]
            type_ = entry[1]["type"]
            modify_ = entry[1]["modify"]
            p = dir_ + s.sep(dir_) + n
            l.append(p)
            self.is_file_map[p] = (type_ == "file")
            self.ts_map[p] = self.format_ts(modify_)
            self.ts_map_s[p] = self.format_ts_s(modify_)
            self.size_map[p] = self.format_size(size_)
            self.size_map_s[p] = self.format_size_s(size_)
        return l
    
    @abstractmethod
    def mlsd(self, recursive=False, dir_=None):
        pass
    
    def format_ts(self, m):
        m = self.format_ts_s(m)
        import time
        ts = time.strptime(m, '%Y-%m-%d %H:%M:%S')
        return time.mktime(ts)
    
    def format_ts_s(self, m):
        return "{0}-{1}-{2} {3}:{4}:{5}".format(m[0:4], m[4:6], m[6:8], m[8:10], m[10:12], m[12:14])
    
    def format_size(self, m):
        return int(m)
    
    def format_size_s(self, m):
        return fileio.format_file_size(int(m))
    
    def get_file_timestamp(self, f):
        if (s.is_windows_path(f)):
            return cons.local_file_system.get_file_timestamp(f)
        if (self.ts_map.__contains__(f)):
            return self.ts_map[f]
        else:
            parent = self.get_parent(f)
            self.iglob(dir_=parent)
            return self.ts_map[f]
    
    def get_file_timestamp_str(self, f):
        if (s.is_windows_path(f)):
            return cons.local_file_system.get_file_timestamp_str(f)
        return self.ts_map_s[f]
    
    def get_file_size(self, f):
        if (s.is_windows_path(f)):
            return cons.local_file_system.get_file_size(f)
        if (self.is_file(f)):
            return self.size_map[f]
        else:
            return 0
    
    def get_file_size_str(self, f):
        if (s.is_windows_path(f)):
            return cons.local_file_system.get_file_size_str(f)
        if (self.is_file(f)):
            return self.size_map_s[f]
        else:
            return ""
    
    def exists(self, f):
        if (s.is_windows_path(f)):
            return cons.local_file_system.exists(f)
        if (f == "/"):
            return True
        parent = self.get_parent(f)
        if (self.list_map.__contains__(parent)):
            files = self.list_map[parent]
            return files.__contains__(f)
        else:
            self.iglob(dir_=parent)
            if (self.list_map.__contains__(parent)):
                files = self.list_map[parent]
                return files.__contains__(f)
        return False
    
    def list_current_dir(self, p):
        if (s.is_windows_path(p)):
            return cons.local_file_system.list_current_dir(p)
        files = self.list_map[p]
        files = s._filter_(files, lambda x: s._r_("filelistfind.match_list_condition", x))
        return files
    
    def cd(self, p):
        if (s.is_windows_path(p)):
            return cons.local_file_system.cd(p)
        pass
    
    def l(self, f, encoding=None):  # @UnusedVariable
        if (s.is_windows_path(f)):
            return cons.local_file_system.l(f, encoding=encoding)
        if (self.file_lines_map.__contains__(f)):
            return self.file_lines_map[f]
        self.file_lines_map[f] = self.do_l(f)
        return self.file_lines_map[f]
    
    @abstractmethod
    def do_l(self, f):
        pass
    
    def is_l(self, f):
        return s.st(f, "/")
    
    def os_listdir(self, p):  # list file names
        if (s.is_windows_path(p)):
            return cons.local_file_system.os_listdir(p)
        files = self.list_current_dir(p)
        files = s.cv_(files, s.cf, p + s.sep(p))
        return files
    
    def rp_check(self, to_dir):
        if (s.is_windows_path(to_dir)):
            return cons.local_file_system.rp_check(to_dir)
        if (to_dir == ""):
            to_dir = "/"
        to_dir = s.cv(to_dir, "//", "/")
        return filelistfind.rp_check__(to_dir)
    
    def vtba_sub(self, m):
        return m
    
    def do_del_file_file(self, f):
        if (s.is_windows_path(f)):
            cons.local_file_system.do_del_file_file(f)
        else:
            self.set_do_del_callback()
            cons.to_delete_files.append(f)
    
    def do_del_file_dir(self, f):
        if (s.is_windows_path(f)):
            cons.local_file_system.do_del_file_dir(f)
        else:
            self.set_do_del_callback()
            cons.to_delete_files.append(f)
    
    def set_do_del_callback(self):
        if (cons.del_callback == None):
            cons.del_callback = self.do_del_callback
    
    def do_del_callback(self, files):  # @UnusedVariable
        self.do_del_files(cons.to_delete_files)
        self.do_clean_list_map(cons.p)
        cons.to_delete_files = []
        cons.del_callback = None
    
    @abstractmethod
    def do_del_files(self, l):
        pass
    
    def do_clean_map(self, p):
        if (self.is_dir(p)):
            self.do_clean_list_map(p)
        else:
            self.do_clean_list_map(self.get_parent(p))
            self.do_clean_file_lines_map(p)
    
    def do_clean_list_map(self, p):
        if (self.list_map.__contains__(p)):
            files = self.list_map.pop(p)
            self.do_clean_ts_map(files)
            self.do_clean_size_map(files)
        if (self.list_map.__contains__(p + "(a)")):
            files = self.list_map.pop(p + "(a)")
            self.do_clean_ts_map(files)
            self.do_clean_size_map(files)

    def do_clean_ts_map(self, files):
        for f in files:
            self.do_clean_ts_map_one(f)

    def do_clean_ts_map_one(self, f):
        if (self.ts_map.__contains__(f)):
            self.ts_map.pop(f)
        if (self.ts_map_s.__contains__(f)):
            self.ts_map_s.pop(f)

    def do_clean_size_map(self, files):
        for f in files:
            self.do_clean_size_map_one(f)

    def do_clean_size_map_one(self, f):
        if (self.size_map.__contains__(f)):
            self.size_map.pop(f)
        if (self.size_map_s.__contains__(f)):
            self.size_map_s.pop(f)

    def do_clean_file_lines_map(self, p):
        if (self.file_lines_map.__contains__(p)):
            self.file_lines_map.pop(p)
    
    def do_copy_file_file(self, from_file, to_file):  # TODO: handle cc: [ip]xxx
        self.set_do_copy_callback()
        if (s.is_windows_path(from_file)):
            self.do_upload__file(from_file, to_file)
        else:
            self.do_copy__file(from_file, to_file)
    
    def set_do_copy_callback(self):
        if (cons.copy_callback == None):
            cons.copy_callback = self.do_copy_callback
    
    def do_copy_callback(self, files):  # @UnusedVariable
        self.do_clean_list_map(cons.p)
        cons.copy_callback = None
    
    @abstractmethod
    def do_copy__file(self, from_file, to_file):
        pass
    
    @abstractmethod
    def do_upload__file(self, from_file, to_file):
        pass
    
    def do_copy_file_dir(self, from_file, to_file):
        self.set_do_copy_callback()
        if (s.is_windows_path(from_file)):
            self.do_upload__dir(from_file, to_file)
        else:
            self.do_copy__dir(from_file, to_file)
    
    def do_copy__dir(self, from_file, to_file):
        # TODO
        pass
    
    def do_upload__dir(self, from_file, to_file):
        self.do_upload__dir_mkdir(to_file)
        files = s._r_("filelistfind.list_dir_", from_file, None, None, True)
        for file in files:
            from_file_ = file
            n = s.cf(from_file_, from_file + s.sep(from_file))
            is_dir = s._r_("fileio.is_dir", from_file_)
            to_file_ = to_file + s.sep(to_file) + s.cv(n, s.sep(from_file_), s.sep(to_file))
            if (is_dir):
                self.do_upload__dir_mkdir(to_file_)
            else:
                self.do_upload__file(from_file_, to_file_)
    
    @abstractmethod
    def do_upload__dir_mkdir(self, dir_):
        pass
    
    def mkdir(self, make_dir):
        if (s.is_windows_path(make_dir)):
            cons.local_file_system.mkdir(make_dir)
        else:
            parent = self.get_parent(make_dir)
            if (not self.exists(parent)):
                self.mkdir(parent)
            if (not self.exists(make_dir)):
                self.do_mkdir__(make_dir)
    
    def do_mkdir__(self, f):
        self.do_mkdir(f)
        cons.mark_go_dir = f
        self.do_clean_map(self.get_parent(f))
    
    @abstractmethod
    def do_mkdir(self, f):
        pass
    
    def set_file_timestamp(self, f, ts):
        # TODO
        pass
    
    def enrich_cc(self, files):
        return s.cv_(files, s.af, s.wrap(self.type_ + ":" + self.c().ip, "[]"))
    
    def c(self):
        return self.client_
    
    def vn(self, m):
        if (m == "vn"):
            self.do_clean_map(cons.p)
            m = "v"
        return m
    
    def ln(self, m):
        if (m == "ln"):
            self.do_clean_map(cons.p)
            m = "l"
        return m
    
    def fn(self, m):
        if (m == "fn"):
            self.do_clean_map(self.get_parent(cons.p))
            m = "f"
        return m

    def clean_up(self):
        clean_latest_open_file()
        self.do_logd_clean_up()
        if (not self.c() == None):
            self.c().close()
            self.client_ = None
    
    def do_logd_clean_up(self):
        if (not self.type_ == "local"):
            ulog.logd("clean up file system: [{0}:{1}]".format(self.type_, self.c().ip))

    def get_input_p(self):
        sub = self.get_input_p_sub()
        if (sub):
            return "[{0}:{1}:{2}]{3}".format(self.c().type, self.c().ip, sub, cons.p)
        else:
            return "[{0}:{1}]{2}".format(self.c().type, self.c().ip, cons.p)
    
    def get_input_p_sub(self):
        return None
    
    def open_file(self, f):
        if (s.is_windows_path(f)):
            cons.local_file_system.open_file(f)
        else:
            from_file = f
            to_file = self.open_file__to_local_file(f)
            self.set_latest_open_file(to_file)
            self.download_file(from_file, to_file)
            fileopen.open_file__(to_file)

    def open_file__to_local_file(self, f):
        to = cons.linux_files + "/" + self.type_ + "/" + self.c().ip
        to += f
        to = s.cv(to, "/", "\\")
        return to
    
    def set_latest_open_file(self, to):
        self.w(cons.latest_open_file, [to])
    
    def w(self, f, lines):
        if (s.is_windows_path(f)):
            cons.local_file_system.w(f, lines)
        else:
            # TODO w in local tmp files, and upload
            pass

    def download_file(self, from_file, to_file, overwrite=False):
        if (self.exists(to_file) and not overwrite):
            from_ts = self.get_file_timestamp(from_file)
            to_ts = self.get_file_timestamp(to_file)
            if (to_ts + 10 >= from_ts):
                ulog.logtr("ignore same file: " + to_file)
                return False
        self.mkdir(self.get_parent(to_file))
        self.do_download_file(from_file, to_file)
        return True

    @abstractmethod
    def do_download_file(self, from_file, to_file):
        pass

    def upload_file(self, from_file, to_file, overwrite=False):
        if (self.exists(to_file) and not overwrite):
            from_ts = self.get_file_timestamp(from_file)
            to_ts = self.get_file_timestamp(to_file)
            if (to_ts + 10 >= from_ts):
                ulog.logtr("ignore same file: " + to_file)
                return False
        self.mkdir(self.get_parent(to_file))
        self.do_upload_file(from_file, to_file)
        self.do_clean_map(to_file)
        return True

    @abstractmethod
    def do_upload_file(self, from_file, to_file):
        pass

    def rp(self, f):
        if (s.is_windows_path(f)):
            f = tar.rp(f)
        f = s.format_sep(f)
        return f

    def translate(self, m):
        m = self.fs_up_file(m)
        m = self.fs_more_translate(m)
        return m

    def fs_up_file(self, m):
        if (m in ["up", "cm"]):
            from_file = self.open_file__to_local_file(cons.p) 
            to_file = cons.p
            uploaded = self.upload_file(from_file, to_file)
            if (uploaded):
                log("commit: " + to_file)
            m = cons.ignore_cmd
        return m
    
    def fs_more_translate(self, m):
        return m
    
    def get_list_max(self):
        return cons.list_max
    
    def is_text_file(self, p):
        return fileopen.is_text_file__(p)

    def max_lines(self):
        return cons.max_lines

    def keep_header(self):
        return False

    def do_backup_del_list(self, files):
        pass


class local_file_system(file_system):

    def init_p(self):
        if (self.exists("/root")):
            cons.p = cons.p_linux
    
    def vn(self, m):
        if (m == "vn"):
            m = "v"
        return m
    
    def ln(self, m):
        if (m == "ln"):
            m = "l"
        return m

    def get_parent(self, f):
        if (s.is_linux_path(f) and not s.is_linux()):
            return super().get_parent(f)
        else:
            return fileio.get_parent__(f)

    def get_file_name(self, p):
        return fileio.get_file_name__(p)

    def l(self, f, encoding=None):
        return fileio.do_l__(f, encoding=encoding)
    
    def get_file_timestamp(self, f):
        if (s.is_linux_path(f) and not s.is_linux()):
            fs_prepare_file_system(f)
            return fs_get_file_timestamp(f)
        else:
            return fileio.get_file_timestamp__(f)
    
    def set_file_timestamp(self, f, ts):
        fileio.set_file_timestamp__(f, ts)

    def get_file_size(self, f):
        return fileio.get_file_size__(f)

    def get_file_timestamp_str(self, f):
        return fileio.get_file_timestamp_str__(f)

    def get_file_size_str(self, f):
        return fileio.get_file_size_str__(f)

    def is_file(self, f):
        if (s.is_linux_path(f) and not s.is_linux()):
            fs_prepare_file_system(f)
            return fs_is_file(f)
        else:
            return fileio.is_file__(f)

    def is_dir(self, f):
        return fileio.is_dir__(f)

    def exists(self, f):
        return fileio.exists__(f)

    def mkdir(self, make_dir):
        parent = self.get_parent(make_dir)
        if (not self.exists(parent)):
            self.mkdir(parent)
        if (not self.exists(make_dir)):
            self.do_mkdir(make_dir)

    def do_mkdir(self, f):
        fileio.do_mkdir__(f)

    def vtba_sub(self, f):
        return filego.vtba_sub__(f)

    def cd(self, f):
        return filelistfind.cd__(f)
    
    def list_current_dir(self, f):
        return filelistfind.list_current_dir__(f)

    def rp_check(self, f):
        return filelistfind.rp_check__(f)

    def os_listdir(self, f):
        return filelistfind.os_listdir__(f)

    def iglob(self, search_key=None, recursive=False, dir_=None):
        return self.do_iglob(search_key=search_key, recursive=recursive, dir_=dir_)
    
    def do_iglob(self, search_key, recursive=False, dir_=None):
        return filelistfind.do_iglob__(search_key, recursive=recursive, dir_=dir_)

    def enrich_cc(self, files):
        return files

    def do_copy_file_file(self, from_file, to_file):
        if (s.is_linux_path(from_file) and not s.is_linux()):
            fs_prepare_file_system(from_file)
            fs_download_file(from_file, to_file)
        else:
            filecopy.do_copy_file_file__(from_file, to_file)

    def do_copy_file_dir(self, from_file, to_file):
        if (s.is_linux_path(from_file) and not s.is_linux()):
            fs_prepare_file_system(from_file)
            fs_download_dir(from_file, to_file)
        else:
            filecopy.do_copy_file_dir__(from_file, to_file)

    def do_del_file_file(self, f):
        filedelete.do_del_file_file__(f)
    
    def do_del_file_dir(self, f):
        filedelete.do_del_file_dir__(f)

    def get_input_p(self):
        return s.get_input_p__()

    def open_file(self, f):
        fileopen.open_file__(f)

    def w(self, f, lines):
        filebackup_.backup(f)
        if (cons.keep_timestamp):
            ts = self.get_file_timestamp(f)
        fileio.w__(f, lines)
        if (cons.keep_timestamp):
            self.set_file_timestamp(f, ts)

    def translate(self, m):
        return m

    def do_backup_del_list(self, files):
        filebackup_.backup_files(files)

