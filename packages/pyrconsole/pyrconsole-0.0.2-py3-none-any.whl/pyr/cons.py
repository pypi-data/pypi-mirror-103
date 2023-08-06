import os

KB = 1024
MB = 1024 * KB
GB = 1024 * MB
TB = 1024 * GB
size_rate = 0.95

sep = os.path.sep
line_sep = "\n"

ignore_cmd = "ignore_cmd"
title_line = "------------------------------------------------------------------------------------------------"

# rconsole
r = None
post_handle = dict()

# constants
cwd_dir   = None
rn_dir    = "C:\\Users\\gzhou\\Desktop\\rename"
diary     = "C:\\Users\\gzhou\\Desktop\\diary.txt"
rnt       = rn_dir + "\\rename.txt"
tmp       = rn_dir + "\\Project\\TMP"
bat_dir   = "C:\\workspace\\buildtemp\\files\\bat"
yoda      = "D:\\jedi\\yoda"
vtba      = "D:\\jedi\\yoda\\export\\home"
tar       = "D:\\soft\\typeandrun\\Config.ini"
fast_copy = "D:\\soft\\fastcopy\\FastCopy.exe"
pyr_dir   = "C:\\workspace\\pyr\\pyr"

# alogs
alogs_dir           = "D:\\alogs"
lastop_dir          = alogs_dir + "\\lastop"
chf                 = lastop_dir + "\\ci_history.txt"
fhf                 = lastop_dir + "\\p_history.txt"
cc_dirs             = alogs_dir + "\\ccReplace\\ccCtrlCCtrlVDirs.txt"
default_output_file = alogs_dir + "\\output.log"
linux_files         = alogs_dir + "\\linux_files"
latest_open_file    = alogs_dir + "\\linux_files\\latest_open_file.txt"
r_variables         = dict()

# env
p                 = "C:\\Users\\gzhou\\Desktop\\rename"
p_linux           = "/home/gzhou"
last_p            = None
debug             = False
trace             = False
debug_performance = False
not_reset         = False

# log
silent                 = 0
tmp_silent             = 0
alog                   = 0
nawlog                 = 0
always_format_log_line = False
log_cache              = []
has_log_cache          = False
log_tab                = ""
debug_log_tab          = ""
rl                     = None
rl_file                = None
rl_start               = False
rl_clean_up            = False
logd_el                = False

# list and find
view_all                      = False
list_max_default              = 100
list_max                      = list_max_default
find_condition                = None
find_condition_key            = None
find_condition_multiple_lines = None
find_condition_picked         = []
list_condition                = None
list_filter                   = None
list_level                    = None
listed_files                  = None
found_files                   = None
found_file_index              = 0
found_file_root               = None
found_lines                   = None
output_file                   = None
max_lines                     = 50

find_shortcuts = {
    "bc"    : "BUILD c",
    "ec"    : "ERROR c",
    "wc"    : "WARN c",
    "lds"   : "com.vitria.domainservice",
    "lvs"   : "com.vitria.virtualserver",
    "lfs"   : "com.vitria.feedserver",
    "lcomp" : "com.vitria.component",
    "lsp"   : "com.vitria.spark",
    "vtcm"  : "vtcommon.jar",
    "vtfc"  : "vtfc.jar",
    "vtdm"  : "vtdms.jar",
    "vtum"  : "vtum.jar",
    "vtcl"  : "vtclient.jar",
    "vtco"  : "vtcore.jar",
    "vten"  : "vtengine.jar",
    "vtfs"  : "vtfeedserver.jar",
    "vtvs"  : "vtvirtualserver.jar",
    "vtds"  : "vtdomainservice.jar",
    "vtas"  : "vtm3oautostart.war",
    "clpi"  : "com.vitria.domainservice.ProjectInfo",
}

# copy files
cc_root = None

# go files
goto = False

# line ops in file edit
replace_ops             = None
replace_condition_from  = None
replace_condition_to    = None
replace_condition_camel = False
keep_timestamp          = False
delete_condition        = None

# filerename
rename_with_ext = False

mark_go_dir = None

cal_result = None

# cache
eis_map = None
co_map  = None
est_map = None
rf_map  = None
tar_map = None

# last op
last_command  = None
space_command = None

# ops
ops_cf = [
    "af", "al", "cf", "cl", "lf", "lfw", "clf", "clfw", "rt", "rtw", "crt", "crtw",
]
ops_ct = [
    "ct", "nct", "st", "nst", "end", "nend", "ctic", "nctic", "stic", "nstic", "endic", "nendic",
]
ops = [
    "af",       "al",        "cf",    "cl",     "lf",          "lfw",        "clf",                "clfw",   "rt",   "rtw",         "crt",   "crtw",
    "c",        "cv",        "cvic",  "trim",   "trimleft",    "trimright",  "wrap",               "unwrap", "nl",   "api",
    "ct",       "nct",       "st",    "nst",    "end",         "nend",       "ctic",               "nctic",  "stic", "nstic",       "endic", "nendic",
    "dt",       "len",       "isf",   "count",  "countn",      "gndoc",
    "shrinkel", "noel",      "nomel", "rmdup",  "tol",         "conns",      "conn",               "use",    "sort", "sortreverse", "dup",
    "sp",       "rnlog",     "swc",   "lower",  "upper",       "camel",
    "no_dup",   "no_spaces", "duiqi", "duiqi2", "format_json", "format_xml", "format_json_or_xml",
]
ops_as_one_line = [
    "shrinkel", "noel", "nomel", "rmdup",  "tol", "conns", "conn", "use", "sort", "sortreverse", "dup",
    "countn",   "swc",  "duiqi", "duiqi2",
]
ops_one_to_n = [
    "sp",
]

# go
file_go_map = {
    "shizhi" : "dd/shizhi.xlsx",
    "kui"    : "dd/Kui.xls",
    "sui.cc" : "dd/School/CreditCards.xlsx",
    "tp"     : "dd/TestProject.zip",
    "fmond"  : "alogs/monday.txt",
}

# open
file_open_map = {
    " sz" : "dd/shizhi.xlsx",
    "ok"  : "dd/Kui.xlsx",
}

# stock
stock_codes = None

# svn
branches = {
    "main"    : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda/",
    "sjb"     : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_branches/jboss_upgrade/",
    "sjb20"   : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_branches/wildfly20_upgrade/",
    "3.3"     : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_release_branches/apps/major-minor/ADF_3.3/",
    "3.6"     : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_release_branches/apps/major-minor/Apps_3.6Beta/",
    "600x"    : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_release_branches/m3o/patches/6.0.0.x/",
    "60bak"   : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_branches/yoda_main_6.0bak/",
    "61ga"    : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_release_branches/m3o/major-minor/6.1_Apps3.5/",
    "610x"    : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_release_branches/m3o/patches/6.1.0.x/",
    "vera"    : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_branches/VIA6103Comcast/",
    "3.7"     : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_release_branches/apps/major-minor/Apps_3.7/",
    "3.7.1"   : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_release_branches/apps/maintenance/Apps_3.7.1/",
    "3.8"     : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_release_branches/apps/major-minor/Apps_3.8/",
    "3.8.1"   : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_release_branches/apps/maintenance/Apps_3.8.1/",
    "3.8.2.x" : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_release_branches/apps/patches/Apps_3.8.2.x/",
    "3.8.3.x" : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_release_branches/apps/patches/Apps_3.8.3.x/",
    "w20"     : "http://vt-sjc-srcsvn.vitria.com/svn/jedi/yoda_branches/wildfly20_upgrade/",
}
branches_sw = {
    "swb"  : "main",
    "sw60" : "600x",
    "sw61" : "610x",
    "sw20" : "w20",
}
svn_keys = None

# web
maxthon_dir  = "C:\\Program Files (x86)\\Maxthon5\\Bin"
maxthon      = "Maxthon.exe"
chrome_dir   = "C:\\Program Files (x86)\\Google\\Chrome\\Application"
chrome       = "chrome.exe"
iexplore_dir = "C:\\Program Files (x86)\\Internet Explorer"
iexplore     = "iexplore.exe"
firefox_dir  = "C:\\Program Files\\Mozilla Firefox"
firefox      = "firefox.exe"
mx           = "\"{0}{1}{2}\"".format(maxthon_dir, sep, maxthon)
cr           = "\"{0}{1}{2}\"".format(chrome_dir, sep, chrome)
ie           = "\"{0}{1}{2}\"".format(iexplore_dir, sep, iexplore)
ff           = "\"{0}{1}{2}\"".format(firefox_dir, sep, firefox)

# callback
run_callback  = None
del_callback  = None
copy_callback = None

# tasklist
tasklist_filter = None
tasklist_tasks  = None

# jps
jps_processes = None

# ci
lasoff = False
ci_ops = {
    "/"     : "w;xxx",
    "\\"    : "wo;xxx",
    "ag"    : "s gp xxx",
    "ah"    : "ahxxx",
    "b  "   : "b  xxx",
    "b+"    : "b  xxx",
    "b-"    : "brm  xxx",
    "b:"    : "b:xxx",
    "b="    : "bn  xxx",
    "bci"   : "bci xxx",
    "bdown" : "bdown xxx",
    "bn"    : "bn xxx",
    "brm  " : "brm  xxx",
    "brm"   : "brm xxx",
    "btop"  : "btop xxx",
    "bup"   : "bup xxx",
    "bv  "  : "bv  xxx",
    "f "    : "f xxx",
    "f."    : "f.xxx",
    "fs."   : "fs xxx",
    "g."    : "g xxx",
    "ksel"  : ".. fs xxx;\def;\dict();r xxx self.xxx[];r self.self. self.[]",
    "l."    : "l xxx",
    "m"     : "ci xxx",
    "mq."   : "mq xxx",
    "q."    : "q xxx",
    "qk."   : "qk xxx",
    "rm"    : "rm xxx",
    "s gg"  : "s gg xxx",
    "s mg"  : "s gg xxx",
    "s."    : "s xxx",
    "w."    : "w xxx",
    "w;"    : "w;xxx",
    "wo;"   : "wo;xxx",
}
ci_mysql = False
ci_mysql_map = {
    "m"   : "SELECT * FROM performance_schema.replication_group_members;",
    "rs"  : "RESET SLAVE;",
    "rm"  : "RESET MASTER;",
    "s"   : "START GROUP_REPLICATION;",
    "t"   : "STOP GROUP_REPLICATION;",
    "pm"  : "SHOW STATUS LIKE 'group_replication_primary_member';",
    "on"  : "SET GLOBAL group_replication_bootstrap_group=ON;",
    "off" : "SET GLOBAL group_replication_bootstrap_group=OFF;",
    "d"   : "D:\\jedi\\yoda\\build\\lib\\driver\\mysql\\mysql-connector-java-5.1.38-bin.jar",
    "h"   : "LAPTOP-GZHOU",
}
m_list = []

# gxxx
gxxx = None

# fileio
encodings = dict()
lines_cache = dict()
is_run_all_ts = None
input_result__ = None

# filego
do_a_up_line_count      = 0
do_a_up_line_file_count = 0
m_dirs                  = None

# filecopy
copy_files = []

# filedelete
to_delete_files = []

# run
run_cmds = {
    "b ."  : "ant",
    "badf" : "badf",
    " up"  : "up",
    "mvnp" : "mvnp",
}

# cmds
quick_cmds = {
    " fm"     : " format_json_or_xml",
    " w"      : "gw20",
    "b "      : ".. [[run ant clean]];run ant[]",
    "c.ppk "  : "c.end(.ppk) ",
    "c.ppk"   : "c.end(.ppk)",
    "c.rt"    : "c.st(RT ) or(st(VIAOps )) ",
    "c10"     : "c.st(10.0.2.) ",
    "cdel"    : "c.st(delete from ) ",
    "chttp"   : "c.st(http://) or(st(https://)) ",
    "comp "   : "comp df/bak/workspace",
    "cplan"   : "c.st(https://vitria.atlassian.net) plan ",
    "cps"     : "c.st(ps ) ",
    "csel"    : "c.st(select ) ",
    "cseln"   : "c.st(select count(*) ) ",
    "cshow"   : "c.st(show ) ",
    "csudo"   : "c.st(sudo ) ",
    "csys"    : "c.st(systemctl ) ",
    "ctar"    : "c.st(tar ) ",
    "cudp"    : "c.st(<) not(end(>)) ",
    "cupd"    : "c.st(update ) ",
    "czoom"   : "c.st(https://zoom) ",
    "fm"      : "r format_json_or_xml keep_ts",
    "ftp "    : " ftph",
    "hdfs "   : " hdfsh",
    "kt"      : ".. [log a;{{log a;{log a};log a};log a};log a]",
    "mysql "  : " mysqlh",
    "og"      : ".. gbtl;glog[];b2",
    "r ; \\n" : "r ;(;;)\\n",
    "rg"      : ".. gtbak;glog[];b2",
    "s "      : " sh",
    "sch"     : "f.mpp",
    "ssh "    : " sshh",
}
quick_cmds_st = {
    "b+" : "b  xxx",
    "b-" : "brm  xxx",
    "b=" : "bn  xxx",
}
cmds          = dict()
next_prev_cmd = None

# daiban
daiban           = None
daiban_option    = None
daiban_workspace = alogs_dir + sep + "DaiBan.log"
roman_numbers    = [
    "i",     "ii",     "iii",     "iv",     "v",     "vi",     "vii",     "viii",     "ix",     "x",
    "xi",    "xii",    "xiii",    "xiv",    "xv",    "xvi",    "xvii",    "xviii",    "xix",    "xx",
    "xxi",   "xxii",   "xxiii",   "xxiv",   "xxv",   "xxvi",   "xxvii",   "xxviii",   "xxix",   "xxx",
    "xxxi",  "xxxii",  "xxxiii",  "xxxiv",  "xxxv",  "xxxvi",  "xxxvii",  "xxxviii",  "xxxix",  "xl",
    "xli",   "xlii",   "xliii",   "xliv",   "xlv",   "xlvi",   "xlvii",   "xlviii",   "xlix",   "l",
    "li",    "lii",    "liii",    "liv",    "lv",    "lvi",    "lvii",    "lviii",    "lix",    "lx",
    "lxi",   "lxii",   "lxiii",   "lxiv",   "lxv",   "lxvi",   "lxvii",   "lxviii",   "lxix",   "lxx",
    "lxxi",  "lxxii",  "lxxiii",  "lxxiv",  "lxxv",  "lxxvi",  "lxxvii",  "lxxviii",  "lxxix",  "lxxx",
    "lxxxi", "lxxxii", "lxxxiii", "lxxxiv", "lxxxv", "lxxxvi", "lxxxvii", "lxxxviii", "lxxxix", "xc",
    "xci",   "xcii",   "xciii",   "xciv",   "xcv",   "xcvi",   "xcvii",   "xcviii",   "xcix",   "c",
]

# file system
local_file_system = None
file_system = None
file_systems = dict()

# open web
web_alias = {
    "pa"  : "http://finance.sina.com.cn/realstock/company/sh601318/nc.shtml",
    "zpm" : "https://zoom.com.cn/j/91934046531?pwd=SFNmQUIvT0tRaHlDaVYrN3l5bzJVQT09",
}

