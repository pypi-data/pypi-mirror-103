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

ssh_sites = {
    "5106": {
        "ip"   : "10.111.5.106",
        "port" : 22,
        "user" : "root",
        "pwd"  : "qilinsoft",
        "dir"  : "/home/gzhou",
    },
    "7121": {
        "ip"   : "10.111.7.121",
        "port" : 22,
        "user" : "root",
        "pwd"  : "qilinsoft",
        "dir"  : "/home/gzhou",
    },
    "3133": {
        "ip"   : "10.111.3.133",
        "port" : 22,
        "user" : "root",
        "pwd"  : "qilinsoft",
        "dir"  : "/home/gzhou",
    },
    "3127": {
        "ip"   : "10.111.3.127",
        "port" : 22,
        "user" : "root",
        "pwd"  : "qilinsoft",
        "dir"  : "/home/gzhou",
    },
    "5128": {
        "ip"   : "10.111.5.128",
        "port" : 22,
        "user" : "root",
        "pwd"  : "qilinsoft",
        "dir"  : "/home/gzhou",
    },
    "2144": {
        "ip"   : "10.0.2.144",
        "port" : 22,
        "user" : "centos",
        "pwd"  : "ppk_cisco",
        "dir"  : "/home/centos",
    },
    "2150": {
        "ip"   : "10.0.2.150",
        "port" : 22,
        "user" : "centos",
        "pwd"  : "ppk_cisco",
        "dir"  : "/home/centos",
    },
    "282": {
        "ip"   : "10.0.2.82",
        "port" : 22,
        "user" : "centos",
        "pwd"  : "ppk_cisco",
        "dir"  : "/home/centos",
    },
    "283": {
        "ip"   : "10.0.2.83",
        "port" : 22,
        "user" : "centos",
        "pwd"  : "ppk_cisco",
        "dir"  : "/home/centos",
    },
    "199": {
        "ip"   : "10.50.1.99",
        "port" : 22,
        "user" : "vitria",
        "pwd"  : "ppk_aws",
        "dir"  : "/home/vitria",
    },
    "199_pub": {
        "ip"   : "54.84.45.75",
        "port" : 22,
        "user" : "vitria",
        "pwd"  : "ppk_aws",
        "dir"  : "/home/vitria/gzhou",
    },
    "1110": {
        "ip"   : "10.50.1.110",
        "port" : 22,
        "user" : "vitria",
        "pwd"  : "ppk_aws",
        "dir"  : "/home/vitria",
    },
    "111": {
        "ip"   : "10.50.1.11",
        "port" : 22,
        "user" : "vitria",
        "pwd"  : "ppk_aws",
        "dir"  : "/home/vitria",
    },
    "178": {
        "ip"   : "10.50.1.78",
        "port" : 22,
        "user" : "vitria",
        "pwd"  : "ppk_aws",
        "dir"  : "/home/vitria",
    },
    "167": {
        "ip"   : "10.50.1.67",
        "port" : 22,
        "user" : "vitria",
        "pwd"  : "ppk_aws",
        "dir"  : "/home/vitria",
    },
    "1251": {
        "ip"   : "10.50.1.251",
        "port" : 22,
        "user" : "vitria",
        "pwd"  : "ppk_aws",
        "dir"  : "/home/vitria",
    },
    "7163": {
        "ip"   : "10.101.7.163",
        "port" : 22,
        "user" : "root",
        "pwd"  : "zhihui1234",
        "dir"  : "/home/gzhou",
    },
    "3185": {
        "ip"   : "10.101.3.185",
        "port" : 22,
        "user" : "root",
        "pwd"  : "qilinsoft",
        "dir"  : "/home/gzhou",
    },
    "3186": {
        "ip"   : "10.101.3.186",
        "port" : 22,
        "user" : "root",
        "pwd"  : "qilinsoft",
        "dir"  : "/home/gzhou",
    },
    "3127_bj": {
        "ip"   : "10.101.3.127",
        "port" : 22,
        "user" : "root",
        "pwd"  : "111111",
        "dir"  : "/home/gzhou",
    },
    "3129": {
        "ip"   : "10.101.3.129",
        "port" : 22,
        "user" : "root",
        "pwd"  : "111111",
        "dir"  : "/home/gzhou",
    },
    "759": {
        "ip"   : "10.101.7.59",
        "port" : 22,
        "user" : "root",
        "pwd"  : "qilinsoft",
        "dir"  : "/home/gzhou",
    },
    "760": {
        "ip"   : "10.101.7.60",
        "port" : 22,
        "user" : "root",
        "pwd"  : "qilinsoft",
        "dir"  : "/home/gzhou",
    },
    "761": {
        "ip"   : "10.101.7.61",
        "port" : 22,
        "user" : "root",
        "pwd"  : "qilinsoft",
        "dir"  : "/home/gzhou",
    },
}

ssh_sites_shortcuts = {
    "1"    : "5106",
    "2"    : "7121",
    "3"    : "3133",
    "4"    : "3127",
    "5"    : "5128",
    "db1"  : "5106",
    "db2"  : "7121",
    "db3"  : "3133",
    "v1"   : "3127",
    "v2"   : "5128",
    "av1"  : "199",
    "av2"  : "1110",
    "adb"  : "178",
    "a67"  : "167",
    "a251" : "1251",
}

ssh_ppks = {
    "ppk_cisco" : "rnp/Support/1209 More help on Stream Builder customer mapping/ppk/centos.pem",
    "ppk_aws"   : "rnp/Investigation/1025 SNMP Trap Split/vpn/charter_dev_env_vitria.pem",
}

ssh_default = "2144"

ssh_cmds_background_is = [
]

ssh_cmds_background_st = [
    "ex  ",
    "ping "
]

ssh_quick_cmds = {
    "ps" : "ps aux",
    "ns" : "netstat -nao",
}
ssh_quick_cmds_st = {
    "ps " : "ps aux | grep xxx",
    "ns " : "netstat -nao | grep xxx",
}


def translate(m):
    m00 = m
    m = quick_cmds(m)
    m = vtba(m)
    m = fs().vn(m)
    m = fs().ln(m)
    m = fs().fn(m)
    m = select_ip(m)
    m = ssh(m)
    ulog.log_trans(m00, m)
    return m


def quick_cmds(m):
    if (is_ssh()):
        if (ssh_quick_cmds.__contains__(m)):
            m = ssh_quick_cmds[m]
        else:
            for k in ssh_quick_cmds_st.keys():
                if (s.st(m, k)):
                    args = s.cf(m, k)
                    m = ssh_quick_cmds_st[k]
                    m = s.cv(m, "xxx", args)
    return m


def vtba(m):
    if (is_ssh()):
        if (m in ["gh", "ghome", "gvtba"]):
            m = "g " + get_vtba_home()
        if (m in ["gsp", "gspark"]):
            m = "g " + get_spark_home()
        if (m in ["ghd", "ghdfs", "ghadoop"]):
            m = "g " + get_hadoop_home()
        if (s.st(m, "g ")):
            dir_ = s.cf(m, "g ")
            dir_ = ssh_rp(dir_)
            dir_ = tar.rp(dir_)
            if (s.st(dir_, tar.rp("home"))):
                dir_ = s.cv(dir_, tar.rp("home"), get_vtba_home())
                dir_ = s.to_linux_path(dir_)
            m = "g " + dir_
    return m


def ssh_rp(p):
    p = s.cv(p, "$VTBA_HOME", get_vtba_home())
    p = s.cv(p, "$SPARK_HOME", get_spark_home())
    p = s.cv(p, "$HADOOP_HOME", get_hadoop_home())
    return p


def get_vtba_home():
    ip = fs().c().ip
    for k in ssh_sites:
        if (ssh_sites[k]["ip"] == ip):
            if (ssh_sites[k].__contains__("vtba")):
                return ssh_sites[k]["vtba"]
            else:
                vtba = get_vtba_home_by_echo()
                ssh_sites[k]["vtba"] = vtba
                return vtba
    return None


def get_spark_home():
    ip = fs().c().ip
    for k in ssh_sites:
        if (ssh_sites[k]["ip"] == ip):
            if (ssh_sites[k].__contains__("spark")):
                return ssh_sites[k]["spark"]
            else:
                spark = get_spark_home_by_echo()
                ssh_sites[k]["spark"] = spark
                return spark
    return None


def get_hadoop_home():
    ip = fs().c().ip
    for k in ssh_sites:
        if (ssh_sites[k]["ip"] == ip):
            if (ssh_sites[k].__contains__("hadoop")):
                return ssh_sites[k]["hadoop"]
            else:
                hadoop = get_hadoop_home_by_echo()
                ssh_sites[k]["hadoop"] = hadoop
                return hadoop
    return None


def get_vtba_home_by_echo():
    return s.sp(do_ex("echo $VTBA_HOME"), no_el=True)[0]


def get_spark_home_by_echo():
    return s.sp(do_ex("echo $SPARK_HOME"), no_el=True)[0]


def get_hadoop_home_by_echo():
    return s.sp(do_ex("echo $HADOOP_HOME"), no_el=True)[0]


def fs():
    return cons.file_system


def c():
    return fs().c()


def select_ip(m):
    if (m == "ssh"):
        m = "ssh " + ssh_default
    elif (s.st(m, "ssh")):
        k = s.cf(m, "ssh")
        if (ssh_sites_shortcuts.__contains__(k)):
            m = "ssh " + ssh_sites_shortcuts[k]
    return m


def ssh(m):
    if (s.st(m, "ssh ")):
        m = s.cf(m, "ssh ")
        m = do_ssh(m)
    if (is_ssh() and not m == cons.ignore_cmd):
        if (m in fs().not_cmds_is):
            if (m in ["ca", "env ca"]):
                filesystem.fs_clean_up()
            pass
        elif (s.st(m, *fs().not_cmds_st)):
            pass
        elif (s.match(m, *fs().not_cmds_match)):
            pass
        elif (s.st(m, "g") and not s.st(m, "g ") and not s.ct(m, " ")):
            pass
        else:
            m = do_ssh_in_r(m)
    return m


def do_ssh_in_r(m):
    if (m == "isdir"):
        log(fs().is_dir(cons.p))
        m = cons.ignore_cmd
    else:
        r = do_ex(m)
        if (r):
            ulog.log_format(s.sp(r))
        m = cons.ignore_cmd
    return m


def do_ssh(m):
    cons.file_system = ssh_file_system(ssh_client(ssh_sites[m]), "ssh")
    return "l"


def do_ex(m, dir_=None, file_system_=None):
    is_background_ = is_background(m)
    if (is_background_):
        m = rm_background(m)
    m = s.cf(m, "ex ")
    start = s.nowts()
    if (dir_ == None):
        dir_ = cons.p
    fs__ = [fs(), file_system_][not file_system_ == None]
    if (fs__.is_file(dir_)):
        dir_ = fs__.get_parent(dir_)
    m = "cd \"{0}\";{1}".format(dir_, m)
    ulog.logd("ssh run: " + m)
    if (file_system_ == None):
        client = c()
    else:
        client = file_system_.c()
    stdin, stdout, stderr = client.ssh_.exec_command(m)  # @UnusedVariable
    if (is_background_):
        while (True):
            try:
                line = s.clean_line_sep(stdout.readline())
            except:
                break
            if (line):
                ulog.log_format(line)
        return None
    else:
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        res = result.decode()
        # res = result.decode("utf-8")
        # res = result.decode(encoding="utf-8")
        ulog.logp("do_ex", start, suffix=" " + m)
        return res


def is_background(m):
    for k in ssh_cmds_background_is:
        if (m == k):
            return True
    for k in ssh_cmds_background_st:
        if (s.st(m, k)):
            return True
    return False


def rm_background(m):
    m = s.cf(m, "ex  ")
    return m


def is_ssh(f=None):
    b = (not fs() == None and fs().type_ == "ssh")
    if (not f == None):
        return b and s.st(f, "/")
    else:
        return b


def do_cd(p):
    do_ex("cd " + p)


def sftp_download_file(server_path, local_path, file_system_=None):
    if (file_system_ == None):
        client = c()
    else:
        client = file_system_.c()
    start = s.nowts()
    client.sftp_.get(server_path, local_path)
    ulog.logp("ssh download", start, " " + server_path)


def sftp_upload_file(local_path, server_path, file_system_=None):
    if (file_system_ == None):
        client = c()
    else:
        client = file_system_.c()
    start = s.nowts()
    client.sftp_.put(local_path, server_path)
    ulog.logp("ssh upload", start, " " + server_path)


def sftp_mkdir(server_path):
    c().sftp_.mkdir(server_path)


def do_download_file__(from_file, to_file):
    k = filesystem.fs_host_as_key(from_file)
    sftp_download_file(s.cf(from_file, k), to_file, file_system_=cons.file_systems[k])


def do_download_dir__(from_file, to_file):
    k = filesystem.fs_host_as_key(from_file)
    sftp_download_file(s.cf(from_file, k), to_file, file_system_=cons.file_systems[k])


def prepare_file_system(ip):
    return ssh_file_system(ssh_client(find_ssh_sites_by_ip(ip)), "ssh")


def find_ssh_sites_by_ip(ip):
    for k in ssh_sites.keys():
        if (ssh_sites[k]["ip"] == ip):
            return ssh_sites[k]
    raise ValueError("unsupported ssh ip: " + ip)


class ssh_client(client):
    
    ssh_ = None
    transport_ = None
    sftp_ = None
    
    def init(self):
        start = s.nowts()
        super().init()
        self.type = "ssh"
        import paramiko
        self.ssh_ = paramiko.SSHClient()
        self.ssh_.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect_ssh()
        self.transport_ = paramiko.Transport((self.ip, self.port))
        self.connect_transport()
        self.sftp_ = paramiko.SFTPClient.from_transport(self.transport_)
        ulog.logp("init  ssh client", start, " [ssh:{0}]".format(self.ip))
    
    def connect_ssh(self):
        if (self.is_using_ppk()):
            self.ssh_.connect(hostname=self.ip, port=self.port, username=self.user, pkey=self.private_key())
        else:
            self.ssh_.connect(hostname=self.ip, port=self.port, username=self.user, password=self.pwd)
    
    def connect_transport(self):
        if (self.is_using_ppk()):
            self.transport_.connect(username=self.user, pkey=self.private_key())
        else:
            self.transport_.connect(username=self.user, password=self.pwd)
    
    def is_using_ppk(self):
        return s.st(self.pwd, "ppk_")
    
    def private_key(self):
        import paramiko
        return paramiko.RSAKey.from_private_key_file(tar.rp(ssh_ppks[self.pwd]))
    
    def close(self):
        start = s.nowts()
        self.sftp_.close()
        self.ssh_.close()
        ulog.logp("close ssh client", start, " [ssh:{0}]".format(self.ip))
        super().close()


class ssh_file_system(file_system):
    
    def do_is_file(self, p):
        n = self.get_file_name(p)
        parent = self.get_parent(p)
        r = do_ex("ls -l " + n, dir_=parent, file_system_=self)
        r = s.sp(r, "\n")
        r = s._filter_(r, s.end, " " + n)
        if (len(r) == 1):
            r = r[0]
            return s.st(r, "-")
        return False
    
    def mlsd(self, recursive=False, dir_=None):
        if (recursive):
            r = do_ex("ls -lR --time-style '+%Y%m%d%H%M%S'", dir_=dir_, file_system_=self)
        else:
            r = do_ex("ls -l --time-style '+%Y%m%d%H%M%S'", dir_=dir_, file_system_=self)
        r = s.sp(r, "\n")
        r = s._filter_(r, s.nst, "total")
        l = []
        dir_ = ""
        for line in r:
            if (not line == ""):
                if (recursive):
                    if (s.end(line, ":")):
                        dir_ = s.cl(line, ":")
                        if (dir_ == "."):
                            dir_ = ""
                        else:
                            dir_ = s.cf(dir_, "./")
                        continue
                is_file = s.st(line, "-")
                if (is_file):
                    type_ = "file"
                else:
                    type_ = "dir"
                line = s.clf_(line, " ", 4)
                size_s = s.lf(line, " ")
                line = s.clf(line, " ")
                time_s = s.lf(line, " ")
                line = s.clf(line, " ")
                if (dir_ == ""):
                    n = line
                else:
                    n = dir_ + "/" + line
                o = {
                    "size": size_s,
                    "type": type_,
                    "modify": time_s
                }
                l.append((n, o))
        l = s.sort(l, sort_key_func=lambda x:x[0])
        return l
    
    def do_l(self, f):
        n = self.get_file_name(f)
        parent = self.get_parent(f)
        r = do_ex("cat " + n, dir_=parent, file_system_=self)
        r = s.sp(r, "\n")
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
        sftp_upload_file(from_file, to_file, file_system_=self)
    
    def do_upload__dir_mkdir(self, dir_):
        sftp_mkdir(dir_)

    def do_mkdir(self, f):
        do_ex("mkdir " + s.wrap(f), file_system_=self)

    def do_download_file(self, from_file, to_file):
        sftp_download_file(from_file, to_file, file_system_=self)

    def do_upload_file(self, from_file, to_file):
        sftp_upload_file(from_file, to_file, file_system_=self)
