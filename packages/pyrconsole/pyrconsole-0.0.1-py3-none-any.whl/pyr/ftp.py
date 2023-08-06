import ustring         as s
from   ulog            import log
from   filesystem      import file_system
from   filesystem      import client

import os

import cmds            as cmds
import cons            as cons
import env             as env
import fileio          as fileio
import filesystem      as filesystem
import tar             as tar
import ulist           as ulist
import ulog            as ulog

ftp_sites = {
    "359": {
        "ip"   : "10.101.3.59",
        "port" : 21,
        "user" : "lan-download",
        "pwd"  : "lan-download",
        "dir"  : "/cruisecontrol",
        "mlsd" : "false",
    },
    "local": {
        "ip"   : "localhost",
        "port" : 21,
        "user" : "root",
        "pwd"  : "qilinsoft",
        "dir"  : "/soft/download",
    },
    "vitria": {
        "ip"   : "vtnewftp.vitria.com",
        "port" : 21,
        "user" : "zliu",
        "pwd"  : "12977-ZL7",
        "dir"  : "/tmp/mdr",
        "mlsd" : "false",
    }
}

ftp_sites_shortcuts = {
    "b" : "359",
}

ftp_default = "local"

ftp_cmds_background_is = [
]

ftp_cmds_background_st = [
]


def translate(m):
    m00 = m
    m = go_ftp_url(m)
    m = ftp_server(m)
    m = fs().vn(m)
    m = fs().ln(m)
    m = fs().fn(m)
    m = select_ip(m)
    m = ftp(m)
    ulog.log_trans(m00, m)
    return m


def go_ftp_url(m):
    if (is_ftp() and s.st(m, "ftp://")):
        m = s.cf(m, "ftp://")
        m = s.clfw(m, "/")
        m = "g " + m
    return m


def ftp_server(m):
    if (m == "ftps"):
        do_ftp_server()
        m = cons.ignore_cmd
    return m


def do_ftp_server():
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import FTPServer
    authorizer = DummyAuthorizer()
    authorizer.add_user("root", "qilinsoft", "D:/", perm="elradfmwMT")
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(("127.0.0.1", 21), handler)
    server.serve_forever()


def fs():
    return cons.file_system


def c():
    return fs().c()


def select_ip(m):
    if (m == "ftp"):
        m = "ftp " + ftp_default
    elif (s.st(m, "ftp")):
        k = s.cf(m, "ftp")
        if (ftp_sites_shortcuts.__contains__(k)):
            m = "ftp " + ftp_sites_shortcuts[k]
    return m


def ftp(m):
    if (s.st(m, "ftp ")):
        m = s.cf(m, "ftp ")
        m = do_ftp(m)
    if (is_ftp() and not m == cons.ignore_cmd):
        if (m in fs().not_cmds_is):
            if (m in ["ca", "env ca"]):
                filesystem.fs_clean_up()
            pass
        elif (s.st(m, *fs().not_cmds_st)):
            pass
        elif (s.match(m, *fs().not_cmds_match)):
            pass
        else:
            m = do_ftp_in_r(m)
    return m


def do_ftp_in_r(m):
    if (m == "isdir"):
        log(fs().is_dir(cons.p))
        m = cons.ignore_cmd
    else:
        r = do_ex(m)
        if (r):
            log(r)
        m = cons.ignore_cmd
    return m


def do_ftp(m):
    cons.file_system = ftp_file_system(ftp_client(ftp_sites[m]), "ftp")
    return "l"


def do_ex(m, dir_=None):  # @UnusedVariable
    r = []
    c().ftp_.retrlines(m, r.append)
    return r


def is_ftp(f=None):
    b = (not fs() == None and fs().type_ == "ftp")
    if (not f == None):
        return b and s.st(f, "/")
    else:
        return b


def do_cd(p):
    do_ex("cd " + p)


def ftp_download_file(server_path, local_path, file_system_=None):
    if (file_system_ == None):
        client = c()
    else:
        client = file_system_.c()
    start = s.nowts()
    out = open(local_path, 'wb')
    try:
        client.ftp_.retrbinary("retr " + server_path, out.write)
    finally:
        out.close()
    ulog.logp("ftp download", start, " " + server_path)


def ftp_upload_file(local_path, server_path, file_system_=None):
    if (file_system_ == None):
        client = c()
    else:
        client = file_system_.c()
    start = s.nowts()
    out = open(local_path, 'rb')
    try:
        client.ftp_.storbinary('stor ' + server_path, out)
    finally:
        out.close()
    ulog.logp("ftp upload", start, " " + server_path)


def ftp_mkdir(server_path):
    c().ftp_.mkd(server_path)


def do_download_file__(from_file, to_file):
    k = filesystem.fs_host_as_key(from_file)
    ftp_download_file(s.cf(from_file, k), to_file, file_system_=cons.file_systems[k])


def do_download_dir__(from_file, to_file):
    k = filesystem.fs_host_as_key(from_file)
    ftp_download_file(s.cf(from_file, k), to_file, file_system_=cons.file_systems[k])


def prepare_file_system(ip):
    return ftp_file_system(ftp_client(find_ftp_sites_by_ip(ip)), "ftp")


def find_ftp_sites_by_ip(ip):
    for k in ftp_sites.keys():
        if (ftp_sites[k]["ip"] == ip):
            return ftp_sites[k]
    raise ValueError("unsupported ftp ip: " + ip)


class ftp_client(client):
    
    ftp_ = None
    mlsd_ = "true"
    
    def init(self):
        start = s.nowts()
        super().init()
        if (self.site.__contains__("mlsd")):
            self.mlsd_ = self.site["mlsd"]
        self.type = "ftp"
        import ftplib
        self.ftp_ = ftplib.FTP()
        self.ftp_.connect(host=self.ip, port=self.port)
        self.ftp_.login(user=self.user, passwd=self.pwd)
        self.ftp_.cwd(cons.p)
        ulog.logp("init  ftp client", start, " [ftp:{0}]".format(self.ip))
        
    def close(self):
        start = s.nowts()
        self.ftp_.close()
        ulog.logp("close ftp client", start, " [ftp:{0}]".format(self.ip))
        super().close()


class ftp_file_system(file_system):
    
    def do_is_file(self, p):
        n = self.get_file_name(p)
        parent = self.get_parent(p)
        self.c().ftp_.cwd(parent)
        r = []
        self.c().ftp_.dir(r.append)
        r = s._filter_(r, s.end, " " + n)
        if (len(r) >= 1):
            r = r[0]
            return s.st(r, "-")
        return False
    
    def mlsd(self, recursive=False, dir_=None):
        if (recursive):
            return self.do_ftp_mlsd__(dir_)
        else:
            return self.do_ftp_mlsd(dir_)

    def do_ftp_mlsd__(self, dir_, parent_=""):  # all
        r = []
        for entry in self.do_ftp_mlsd(dir_):
            n = entry[0]
            if (parent_ != ""):
                n__ = parent_ + "/" + n
            else:
                n__ = n
            type_ = entry[1]["type"]
            if (type_ == "file"):
                r += [(n__, entry[1])]
            else:
                r += [(n__, entry[1])]
                r += self.do_ftp_mlsd__(dir_ + "/" + n, parent_=n__)
        return r
    
    def do_ftp_mlsd(self, dir_):
        if (self.c().mlsd_ == "false"):
            return self.do_ftp_mlsd__with_dir(dir_)
        else:
            return self.c().ftp_.mlsd(dir_, facts=["type", "size", "modify"])
    
    def do_ftp_mlsd__with_dir(self, dir_):
        lines = []
        self.c().ftp_.dir(dir_, lines.append)
        r = []
        for line in lines:
            n = s.rt(line, " ")
            if (s.st(line, "d")):
                type_ = "dir"
            else:
                type_ = "file"
            size_ = s.sp(line, " ", no_el=True)[4]
            modify_ = self.do_ftp_mlsd__get_modify(line)
            r.append((n, {"size": size_, "type": type_, "modify":modify_}))
        return r
    
    def do_ftp_mlsd__get_modify(self, line):
        l = s.sp(line, " ", no_el=True)
        month = l[5]
        day = l[6]
        year_or_time = l[7]
        months_map = {
            "Jan" : "01",
            "Feb" : "02",
            "Mar" : "03",
            "Apr" : "04",
            "May" : "05",
            "Jun" : "06",
            "Jul" : "07",
            "Aug" : "08",
            "Sep" : "09",
            "Oct" : "10",
            "Nov" : "11",
            "Dec" : "12",
        }
        month = months_map[month]
        if (s.ct(year_or_time, ":")):
            year = s.this_year()
            hour = s.lf(year_or_time, ":")
            minute = s.clf(year_or_time, ":")
            second = "00"
            return "{0}{1}{2}{3}{4}{5}".format(year, month, day, hour, minute, second)
        else:
            year = year_or_time
            hour = "00"
            minute = "00"
            second = "00"
            return "{0}{1}{2}{3}{4}{5}".format(year, month, day, hour, minute, second)
    
    def do_l(self, f):
        r = []
        self.c().ftp_.retrlines("RETR " + f, r.append)
        return r
    
    def do_del_files(self, l):
        for f in l:
            if (self.is_file(f)):
                self.do_ftp_delete_file(f)
            else:
                self.do_ftp_delete_dir(f)
    
    def do_ftp_delete_file(self, f):
        self.c().ftp_.delete(f)
        
    def do_ftp_delete_dir(self, dir_):
        for entry in self.do_ftp_mlsd(dir_):
            n = entry[0]
            type_ = entry[1]["type"]
            if (type_ == "file"):
                self.do_ftp_delete_file(dir_ + "/" + n)
            else:
                self.do_ftp_delete_dir(dir_ + "/" + n)
        self.c().ftp_.rmd(dir_)
    
    def do_copy__file(self, from_file, to_file):
        # TODO
        pass
    
    def do_upload__file(self, from_file, to_file):
        ftp_upload_file(from_file, to_file, file_system_=self)
    
    def do_upload__dir_mkdir(self, dir_):
        ftp_mkdir(dir_)
    
    def do_mkdir(self, f):
        ftp_mkdir(f)
    
    def do_download_file(self, from_file, to_file):
        ftp_download_file(from_file, to_file, file_system_=self)
    
    def do_upload_file(self, from_file, to_file):
        ftp_upload_file(from_file, to_file, file_system_=self)

