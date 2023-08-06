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
import rvar            as rvar
import tar             as tar
import ulist           as ulist
import ulog            as ulog

mysql_sites = {
    "local": {
        "ip"       : "localhost",
        "port"     : 3306,
        "user"     : "root",
        "pwd"      : "Qilin@1234",
        "dir"      : "/",
        "database" : "test",
    },
    "local_viaops_config_db": {
        "ip"       : "localhost",
        "port"     : 3306,
        "user"     : "root",
        "pwd"      : "Qilin@1234",
        "dir"      : "/",
        "database" : "viaops_config_db",
    },
}

mysql_sites_shortcuts = {
    "lc" : "local_viaops_config_db",
}

mysql_default = "local_viaops_config_db"

mysql_cmds_background_is = [
]

mysql_cmds_background_st = [
]

mysql_quick_cmds = {
    "desc" : "desc %n%;"
}

mysql_quick_cmds_st = {
}

mysql_column_types = {
    "string"   : "varchar(255)",
    "int"      : "integer",
    "datetime" : "datetime",
}


def translate(m):
    m00 = m
    m = quick_cmds(m)
    m = fs().vn(m)
    m = fs().ln(m)
    m = fs().fn(m)
    m = select_ip(m)
    m = rvar_(m)
    m = mysql(m)
    ulog.log_trans(m00, m)
    return m


def quick_cmds(m):
    if (mysql_quick_cmds.__contains__(m)):
        m = mysql_quick_cmds[m]
    else:
        for k in mysql_quick_cmds_st.keys():
            if (s.st(m, k)):
                args = s.cf(m, k)
                m = mysql_quick_cmds_st[k]
                m = s.cv(m, "xxx", args)
    return m


def fs():
    return cons.file_system


def c():
    return fs().c()


def select_ip(m):
    if (m == "mysql"):
        m = "mysql " + mysql_default
    elif (s.st(m, "mysql")):
        k = s.cf(m, "mysql")
        if (mysql_sites_shortcuts.__contains__(k)):
            m = "mysql " + mysql_sites_shortcuts[k]
    return m


def rvar_(m):
    m = rvar.rvar(m)
    return m


def mysql(m):
    if (s.st(m, "mysql ")):
        m = s.cf(m, "mysql ")
        m = do_mysql(m)
    if (is_mysql() and not m == cons.ignore_cmd):
        if (m in ["-"]):
            m = do_mysql_in_r(m)
        if (m in fs().not_cmds_is):
            if (m in ["ca", "env ca"]):
                filesystem.fs_clean_up()
            pass
        elif (s.st(m, *fs().not_cmds_st)):
            pass
        elif (s.match(m, *fs().not_cmds_match)):
            pass
        else:
            m = do_mysql_in_r(m)
    return m


def do_mysql_in_r(m):
    if (is_use(m)):
        m = do_use(m)
    elif (is_create(m)):
        m = do_create(m)
    elif (is_insert(m)):
        m = do_insert(m)
    elif (is_delete(m)):
        m = do_delete(m)
    else:
        r = do_ex(m)
        if (r):
            r = add_header(r, m)
            ulog.logl("", results_to_lines(r))
        m = cons.ignore_cmd
    return m


def is_use(m):
    return s.st(m, "use ")


def do_use(m):
    m = s.cf(m, "use ")
    m = s.cl(m, ";")
    fs().use_database(m)
    m = "l"
    return m


def is_create(m):
    return m in ["cr", "create"]


def do_create(m):  # @UnusedVariable
    n = input("    table name: ")
    columns = ""
    while (True):
        cn = input("    column name: ")
        if (cn == ""):
            break
        ct = input("    column type: ")
        if (ct == ""):
            ct = "string"
        ct = mysql_column_types[ct]
        columns += "{0} {1}, ".format(cn, ct)
    pk = input("    primary key: ")
    if (pk == ""):
        columns = s.cl(columns, ", ")
    else:
        columns += "primary key ({0})".format(pk)
    sql = "create table {0} ({1})".format(n, columns)
    do_ex(sql)
    fs().do_clean_map("/")
    log()
    return "l"


def is_insert(m):
    return s.st(m, "ins ", "+")


def do_insert(m):
    m = s.trim(s.cf(m, "ins ", "+"))
    m = s.resolve_repeat_ids(m)
    m = s.cv_(m, s.get_parts)
    tn = fileio.get_file_name(cons.p)

    def wrap__(x):
        if (s.is_number(x)):
            return x
        else:
            return s.wrap(x, "''")

    for m_one in m:
        m_one = s.cv_(m_one, wrap__)
        m_one = s.conn(m_one, ", ")
        sql = "insert into {0} values ({1})".format(tn, m_one)
        do_ex(sql)
    do_ex("commit")
    fs().do_clean_map(cons.p)
    return "v"


def is_delete(m):
    return m == "-"


def do_delete(m):  # @UnusedVariable
    tn = fileio.get_file_name(cons.p)
    if (env.has_find_condition()):
        found_lines = cons.found_lines[cons.p]
        header = found_lines[0][1]
        header = s.cf(header, "| ")
        header = s.cl(header, " |")
        header = s.sp(header, " | ")
        for i in range(len(found_lines) - 1):
            line = found_lines[i + 1][1]
            line = s.cf(line, "| ")
            line = s.cl(line, " |")
            line = s.sp(line, " | ")
            con = ""
            for j in range(len(header)):
                cn = header[j]
                cv = line[j]
                if (s.is_number(cv)):
                    con += "{0} = {1} and ".format(cn, cv)
                else:
                    con += "{0} = '{1}' and ".format(cn, cv)
            con = s.cl(con, " and ")
            sql = "delete from {0} where {1}".format(tn, con)
            do_ex(sql)
        do_ex("commit")
        fs().do_clean_map(cons.p)
        env.reset_find()
    else:
        sql = "delete from {0}".format(tn)
        do_ex(sql)
        do_ex("commit")
        fs().do_clean_map(cons.p)
    return "v"


def add_header(res, m):
    if (s.stic(m, "select")):
        m = s.lower(m)
        m = s.lf(m, " from ")
        m = s.cf(m, "select ")
        m = s.sp(m, ",")
        m = s.trim(m)
        m = tuple(m)
        r = []
        r += [m]
        r += res
        res = r
    return res


def do_mysql(m):
    cons.file_system = mysql_file_system(mysql_client(mysql_sites[m]), "mysql")
    return "l"


def do_ex(m, dir_=None, file_system_=None):
    start = s.nowts()
    if (dir_ == None):
        dir_ = cons.p
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
            file = s.unwrap(file)
            file_name = fileio.get_file_name(file)
            sql = "drop table {0}".format(file_name)
            do_ex_sql(client, sql)
    elif (s.st(m, "cat ")):
        m = s.cf(m, "cat ")
        file = dir_ + "/" + m
        with client.hdfs_.read(file) as reader:
            res = reader.read().decode("utf-8")
    else:
        res = do_ex_sql(client, m)
    ulog.logp("do_ex", start, suffix=" " + m)
    return res


def do_ex_sql(client, m):
    cursor = client.mysql_.cursor()
    ulog.logd()
    ulog.logd("mysql run: " + m)
    cursor.execute(m)
    res = cursor.fetchall()
    return res


def is_background(m):
    for k in mysql_cmds_background_is:
        if (m == k):
            return True
    for k in mysql_cmds_background_st:
        if (s.st(m, k)):
            return True
    return False


def rm_background(m):
    m = s.cf(m, "ex  ")
    return m


def is_mysql(f=None):
    b = (not fs() == None and fs().type_ == "mysql")
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
    ulog.logp("mysql download", start, " " + server_path)


def sftp_upload_file(local_path, server_path, file_system_=None):
    if (file_system_ == None):
        client = c()
    else:
        client = file_system_.c()
    start = s.nowts()
    client.sftp_.put(local_path, server_path)
    ulog.logp("mysql upload", start, " " + server_path)


def sftp_mkdir(server_path):
    c().sftp_.mkdir(server_path)


def do_download_file__(from_file, to_file):
    k = filesystem.fs_host_as_key(from_file)
    sftp_download_file(s.cf(from_file, k), to_file, file_system_=cons.file_systems[k])


def prepare_file_system(ip):
    return mysql_file_system(mysql_client(find_mysql_sites_by_ip(ip)), "mysql")


def find_mysql_sites_by_ip(ip):
    for k in mysql_sites.keys():
        if (mysql_sites[k]["ip"] == ip):
            return mysql_sites[k]
    raise ValueError("unsupported mysql ip: " + ip)


def results_to_lines(res):
    r = []
    size_map = to_size_map(res)
    for line in res:
        r.append(to_record_line(line, size_map))
    return r


def to_size_map(res):
    r = dict()
    line0 = res[0]
    for i in range(len(line0)):
        r[i] = 0
    for line in res:
        for i in range(len(line)):
            r[i] = max(r[i], len(str(line[i])))
    return r


def to_record_line(line, size_map):
    r = "| "
    for i in range(len(line)):
        r += str(line[i]) + s.get_indent_string(size_map[i] - len(str(line[i]))) + " | "
    r = s.cl(r, " ")
    return r


class mysql_client(client):
    
    database = ""
    mysql_ = None
    
    def init(self):
        start = s.nowts()
        super().init()
        self.database = self.site["database"]
        self.type = "mysql"
        import pymysql
        self.mysql_ = pymysql.connect(
            host=self.ip,
            port=self.port,
            user=self.user,
            password=self.pwd,
            database=self.database,
            charset="utf8"
        )
        ulog.logp("init  mysql client", start, " [mysql:{0}]".format(self.ip))
    
    def close(self):
        start = s.nowts()
        self.mysql_.close()
        ulog.logp("close mysql client", start, " [mysql:{0}]".format(self.ip))
        super().close()


class mysql_file_system(file_system):
    
    def do_is_file(self, p):
        return not p == "/"
    
    def mlsd(self, recursive=False, dir_=None):  # @UnusedVariable
        r = do_ex("select table_name,table_rows from information_schema.tables where table_schema='{0}' and table_type='BASE TABLE';".format(self.c().database), file_system_=self)
        l = []
        for line in r:
            type_ = "file"
            n = line[0]
            o = {
                "size": line[1],
                "type": type_,
                "modify": ""
            }
            l.append((n, o))
        l = s.sort(l, sort_key_func=lambda x:x[0])
        return l
    
    def format_ts(self, m):
        return m
    
    def format_ts_s(self, m):
        return m
    
    def format_size(self, m):
        return m
    
    def format_size_s(self, m):
        return m

    def header(self, n):
        res = do_ex("desc " + n, file_system_=self)
        r = []
        for line in res:
            r.append(line[0])
        return tuple(r)
    
    def do_l(self, f):
        n = self.get_file_name(f)
        r = []
        res = do_ex("select * from " + n, file_system_=self)
        r += [self.header(n)]
        r += res
        return results_to_lines(r)
    
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

    def get_list_max(self):
        if (cons.list_max == cons.list_max_default):
            return 20
        else:
            return cons.list_max

    def is_text_file(self, p):  # @UnusedVariable
        return True

    def max_lines(self):
        return 20

    def keep_header(self):
        return True

    def get_input_p_sub(self):
        return self.c().database
    
    def use_database(self, another_database):
        c().mysql_.close()
        c().site["database"] = another_database
        c().init()
        cons.p = "/"
        self.do_clean_map(cons.p)

