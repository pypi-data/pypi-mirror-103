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
import utime           as utime

hdfs_sites = {
    "local": {
        "ip"    : "localhost",
        "port"  : 50070,
        "port_" : 8020,
        "user"  : "gzhou",
        "pwd"   : "",
        "dir"   : "/user/gzhou",
    },
    "zhihui_test": {
        "ip"    : "10.101.7.163",
        "port"  : 50070,
        "port_" : 8020,
        "user"  : "gzhou",
        "pwd"   : "",
        "dir"   : "/user/gzhou",
    },
    "282": {
        "ip"    : "10.0.2.82",
        "port"  : 50070,
        "port_" : 8020,
        "user"  : "root",
        "pwd"   : "",
        "dir"   : "/user/gzhou",
    },
}

hdfs_sites_shortcuts = {
    "c" : "zhihui_test",
}

hdfs_default = "282"

hdfs_cmds_background_is = [
]

hdfs_cmds_background_st = [
]

hdfs_quick_cmds = {
}
hdfs_quick_cmds_st = {
}


def translate(m):
    m00 = m
    m = quick_cmds(m)
    m = fs().vn(m)
    m = fs().ln(m)
    m = fs().fn(m)
    m = select_ip(m)
    m = tr_hdfs(m)
    ulog.log_trans(m00, m)
    return m


def quick_cmds(m):
    if (hdfs_quick_cmds.__contains__(m)):
        m = hdfs_quick_cmds[m]
    else:
        for k in hdfs_quick_cmds_st.keys():
            if (s.st(m, k)):
                args = s.cf(m, k)
                m = hdfs_quick_cmds_st[k]
                m = s.cv(m, "xxx", args)
    return m


def fs():
    return cons.file_system


def c():
    return fs().c()


def select_ip(m):
    if (m == "hdfs"):
        m = "hdfs " + hdfs_default
    elif (s.st(m, "hdfs")):
        k = s.cf(m, "hdfs")
        if (hdfs_sites_shortcuts.__contains__(k)):
            m = "hdfs " + hdfs_sites_shortcuts[k]
    return m


def tr_hdfs(m):
    if (s.st(m, "hdfs ")):
        m = s.cf(m, "hdfs ")
        m = do_hdfs(m)
    if (is_hdfs() and not m == cons.ignore_cmd):
        if (m in fs().not_cmds_is):
            if (m in ["ca", "env ca"]):
                filesystem.fs_clean_up()
            pass
        elif (s.st(m, *fs().not_cmds_st)):
            pass
        elif (s.match(m, *fs().not_cmds_match)):
            pass
        else:
            m = do_hdfs_in_r(m)
    return m


def do_hdfs_in_r(m):
    if (m == "isdir"):
        log(fs().is_dir(cons.p))
        m = cons.ignore_cmd
    else:
        r = do_ex(m)
        if (r):
            ulog.log_format(s.sp(r))
        m = cons.ignore_cmd
    return m


def do_hdfs(m):
    cons.file_system = hdfs_file_system(hdfs_client(hdfs_sites[m]), "hdfs")
    return "l"


def do_ex(m, dir_=None, file_system_=None):
    start = s.nowts()
    if (dir_ == None):
        dir_ = cons.p
    ulog.logd("hdfs run: " + m)
    if (file_system_ == None):
        client = c()
    else:
        client = file_system_.c()
    res = None
    if (m == "ls -l"):
        res = client.hdfs_.list(dir_, status=True)
    elif (m == "ls -lR"):
        res = client.hdfs_.walk(dir_, status=True)
    elif (s.st(m, "ls -l ")):
        n = s.cf(m, "ls -l ")
        res = client.hdfs_.list(dir_, status=True)
        res = s._filter_(res, lambda x: s.isf(x[0], n))
    elif (s.st(m, "rm -fr ")):
        m = s.cf(m, "rm -fr ")
        files = s.sp(m, " ")
        for file in files:
            client.hdfs_.delete(s.unwrap(file), recursive=True)
    elif (s.st(m, "cat ")):
        m = s.cf(m, "cat ")
        file = dir_ + "/" + m
        with client.hdfs_.read(file) as reader:
            res = reader.read().decode("utf-8")
    ulog.logp("do_ex", start, suffix=" " + m)
    return res


def is_background(m):
    for k in hdfs_cmds_background_is:
        if (m == k):
            return True
    for k in hdfs_cmds_background_st:
        if (s.st(m, k)):
            return True
    return False


def rm_background(m):
    m = s.cf(m, "ex  ")
    return m


def is_hdfs(f=None):
    b = (not fs() == None and fs().type_ == "hdfs")
    if (not f == None):
        return b and s.st(f, "/")
    else:
        return b


def do_cd(p):
    do_ex("cd " + p)


def hdfs_download_file(server_path, local_path, file_system_=None):
    if (file_system_ == None):
        client = c()
    else:
        client = file_system_.c()
    start = s.nowts()
    if (cons.local_file_system.exists(local_path)):
        cons.local_file_system.do_del_file_file(local_path)
    client.hdfs_.download(server_path, local_path)
    ulog.logp("hdfs download", start, " " + server_path)


def hdfs_upload_file(local_path, server_path, file_system_=None):
    if (file_system_ == None):
        client = c()
    else:
        client = file_system_.c()
    start = s.nowts()
    client.hdfs_.upload(server_path, local_path)
    ulog.logp("hdfs upload", start, " " + server_path)


def hdfs_mkdir(server_path):
    c().hdfs_.makedirs(server_path)


def do_download_file__(from_file, to_file):
    k = filesystem.fs_host_as_key(from_file)
    hdfs_download_file(s.cf(from_file, k), to_file, file_system_=cons.file_systems[k])


def do_download_dir__(from_file, to_file):
    k = filesystem.fs_host_as_key(from_file)
    hdfs_download_file(s.cf(from_file, k), to_file, file_system_=cons.file_systems[k])


def prepare_file_system(ip):
    return hdfs_file_system(hdfs_client(find_hdfs_sites_by_ip(ip)), "hdfs")


def find_hdfs_sites_by_ip(ip):
    for k in hdfs_sites.keys():
        if (hdfs_sites[k]["ip"] == ip):
            return hdfs_sites[k]
    raise ValueError("unsupported hdfs ip: " + ip)


def handle(m):
    if (s.st(m, "down_aws ")):
        m = s.cf(m, "down_aws ")
        down_aws(m)


def down_aws(m):
    down_aws_dir("/do_dev/viaops/hdfs_target", m)


def down_aws_dir(hdir, n):
    s = "/home/vitria/hadoop-2.7.6/bin/hadoop distcp hdfs://master:8020{0}/{1} file:///home/vitria/gzhou/incident_notification/{1}"
    print(s.format(hdir, n))


class hdfs_client(client):
    
    port_ = 8020
    hdfs_ = None
    
    def init(self):
        start = s.nowts()
        super().init()
        self.port_ = self.site["port_"]
        self.type = "hdfs"
        from hdfs.client import InsecureClient
        self.hdfs_ = InsecureClient("http://" + self.ip + ":" + str(self.port), user=self.user)
        ulog.logp("init  hdfs client", start, " [hdfs:{0}]".format(self.ip))
    
    def close(self):
        start = s.nowts()
        ulog.logp("close hdfs client", start, " [hdfs:{0}]".format(self.ip))
        super().close()


class hdfs_file_system(file_system):
    
    def do_is_file(self, p):
        n = self.get_file_name(p)
        parent = self.get_parent(p)
        r = do_ex("ls -l " + n, dir_=parent, file_system_=self)
        if (len(r) == 1):
            r = r[0]
            return r[1]["type"] == "FILE"
        return False
    
    def mlsd(self, recursive=False, dir_=None):
        if (recursive):
            r = do_ex("ls -lR", dir_=dir_, file_system_=self)
        else:
            r = do_ex("ls -l", dir_=dir_, file_system_=self)
        l = []
        dir_ = ""
        for line in r:
            if (not line == ""):
                if (recursive):
                    if (not line[0][0] == cons.p):
                        l.append(self.mlsd_to_line(line[0], ""))
                    for file in line[2]:
                        l.append(self.mlsd_to_line(file, line[0][0]))
                else:
                    l.append(self.mlsd_to_line(line, dir_))
        l = s.cv_(l, lambda x: (s.cf(x[0], cons.p + "/"), x[1]))
        l = s.sort(l, sort_key_func=lambda x:x[0])
        return l
    
    def mlsd_to_line(self, line, dir_):
        is_file = line[1]["type"] == "FILE"
        if (is_file):
            type_ = "file"
        else:
            type_ = "dir"
        size_s = line[1]["length"]
        time_s = line[1]["modificationTime"]
        time_s = utime.do_ms_to_time(str(time_s), format_="%Y%m%d%H%M%S")
        if (dir_ == ""):
            n = line[0]
        else:
            n = dir_ + "/" + line[0]
        o = {
            "size": size_s,
            "type": type_,
            "modify": time_s
        }
        return (n, o)
    
    def do_l(self, f):
        n = self.get_file_name(f)
        parent = self.get_parent(f)
        r = do_ex("cat " + n, dir_=parent, file_system_=self)
        r = s.sp(r)
        return r
    
    def do_del_files(self, l):
        l = s.cv_(l, s.wrap)
        m = s.conn(l, " ")
        m = "rm -fr " + m
        do_ex(m, file_system_=self)
    
    def do_copy__file(self, from_file, to_file):
        # TODO
        pass
    
    def do_upload__file(self, from_file, to_file):
        hdfs_upload_file(from_file, to_file, file_system_=self)
    
    def do_upload__dir(self, from_file, to_file):
        hdfs_upload_file(from_file, to_file, file_system_=self)
    
    def do_upload__dir_mkdir(self, dir_):
        hdfs_mkdir(dir_)

    def do_mkdir(self, f):
        hdfs_mkdir(f)

    def do_download_file(self, from_file, to_file):
        hdfs_download_file(from_file, to_file, file_system_=self)

    def do_upload_file(self, from_file, to_file):
        if (self.exists(to_file)):
            self.do_del_files([to_file])
        hdfs_upload_file(from_file, to_file, file_system_=self)
    
    def fs_more_translate(self, m):
        m = self.fs_web(m)
        m = self.ci_url(m)
        return m
    
    def fs_web(self, m):
        if (m == "w"):
            p = cons.p
            if (self.is_file(p)):
                p = self.get_parent(p)
            m = "s cr http://{0}:{1}/explorer.html#{2}".format(self.client_.ip, self.client_.port, p)
        return m
    
    def ci_url(self, m):
        if (m == "ciurl"):
            m = "ci hdfs://{0}:{1}{2}".format(self.client_.ip, self.client_.port_, cons.p)
        elif (m == "ciurl "):
            m = "ci hdfs://{0}:{1}".format(self.client_.ip, self.client_.port_)
        elif (m == "ciw"):
            m = "ci http://{0}:{1}/explorer.html#{2}".format(self.client_.ip, self.client_.port, cons.p)
        return m

