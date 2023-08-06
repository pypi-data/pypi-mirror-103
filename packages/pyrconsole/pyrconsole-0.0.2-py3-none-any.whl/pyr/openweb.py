import ustring         as s
from   ulog            import log

import os

import ci              as ci
import cons            as cons
import tar             as tar
import ulist           as ulist
import ulog            as ulog


def translate0(m):
    m00 = m
    m = ji(m)
    m = map_ci(m)
    m = web_s(m)
    m = translate_(m)
    m = web_alias(m)
    m = tr_notification_models(m)
    ulog.log_trans(m00, m)
    return m


def ji(m):
    if (m == "ji"):
        m = ci.get_text()
        if (s.ct(m, " DO-")):
            m = s.clfw(m, "DO-")
        m = s.lf(m, " ")
        if (s.is_number(m)):
            m = "DO-" + m
        return "s ji " + m
    return m


def map_ci(m):
    if (m in ["gd", "map"]):
        m = "m" + ci.get_text()
    return m


def translate(m):
    m00 = m
    m = gd(m)
    m = bk(m)
    m = web_tar(m)
    ulog.log_trans(m00, m)
    return m


def web_s(m):
    if (m == "s"):
        return ".. s b;s f;ulog open: baidu, finance.sina[]"
    return m


def translate_(m):
    if (s.st(m, "t ")):
        m = s.cf(m, "t ")
        m = s.trim(m)
        cons.space_command = "s yd " + m
        do_translate(m)
        m = cons.ignore_cmd
    if (m == "t"):
        m = "t " + ci.get_text()
    return m


def web_alias(m):
    if (cons.web_alias.__contains__(m)):
        m = "s " + cons.web_alias[m]
    return m


def tr_notification_models(m):
    if (m in ["h nm", "nm?"]):
        notification_models_help = {
            "start" : "input \"nm\" in Python R to start",
        }
        ulog.logh("notification_models", notification_models_help)
        m = cons.ignore_cmd
    if (m == "nm"):
        do_notification_models()
        m = cons.ignore_cmd
    return m


def do_translate(m):
    app_key = "6bd83f74fe77c777"
    query = m
    salt = str(s.nowts())
    from_ = "EN"
    to_ = "zh-CHS"
    sign = s.md5(app_key + query + salt + "NV9MeQPzAt8Vf9nqxtaOIWNWshB86myV")
    params = dict()
    params["q"] = query
    params["from"] = from_
    params["to"] = to_
    params["sign"] = sign
    params["salt"] = salt
    params["appKey"] = app_key
    url = "https://openapi.youdao.com/api"
    import requests
    r = requests.post(url, params=params).text
    r = s.c(r, "explains", "us-speech")
    if (s.ct(r, "{")):
        r = s.c(r, "\"translation\":[\"", "\"],")
        r = [r]
    else:
        r = s.clf(r, "[")
        r = s.crt(r, "]")
        r = s.sp(r, ",")
        r = s.cv_(r, s.unwrap)
    log()
    log(m)
    ulog.logt(4, r)


def gd(m):
    if (s.st(m, "m")):
        m1 = s.cf(m, "m")
        if (s.is_first_chinese(m1)):
            return "s gd " + m1
    return m


def bk(m):
    if (s.is_first_chinese(m)):
        return "s bk " + m
    return m


def web_tar_0(m):
    if (not m in ["tr"]):
        w = tar.rp_web(m)
        if (not w == None):
            m = "s " + w
    return m


def web_tar(m):
    w = tar.rp_web(m)
    if (not w == None):
        m = "s " + w
    return m


def open_maxthon(f):
    os.chdir(cons.maxthon_dir)
    cmd = "call {0} \"{1}\"".format(cons.maxthon, f)
    os.system(cmd)
    log("open: " + f)


def open_chrome(f):
    os.chdir(cons.chrome_dir)
    cmd = "call {0} \"{1}\"".format(cons.chrome, f)
    os.system(cmd)
    log("open: " + f)


def open_iexplore(f):
    os.chdir(cons.iexplore_dir)
    cmd = "call {0} \"{1}\"".format(cons.iexplore, f)
    os.system(cmd)
    log("open: " + f)


def open_firefox(f):
    os.chdir(cons.firefox_dir)
    cmd = "call {0} \"{1}\"".format(cons.firefox, f)
    os.system(cmd)
    log("open: " + f)


def handle(m):
    mx = False
    cr = False
    ie = False
    ff = False

    if (tar.is_web_key(m)):
        m = tar.rp(m)

    url = m

    if (s.st(m, "http://", "https://")):
        url = m
    elif (s.has_p(m, "mx")):
        mx = True
        url = s.rm_p(m, "mx")
    elif (s.has_p(m, "cr")):
        cr = True
        url = s.rm_p(m, "cr")
    elif (s.has_p(m, "ie")):
        ie = True
        url = s.rm_p(m, "ie")
    elif (s.has_p(m, "ff")):
        ff = True
        url = s.rm_p(m, "ff")
    elif (s.has_p(m, "bk")):
        m = s.rm_p(m, "bk")
        url = "https://baike.baidu.com/item/" + s.cv(m, " ", "%20")
    elif (s.has_p(m, "gd")):
        m = s.rm_p(m, "gd")
        url = "https://www.amap.com/search?query=" + s.cv(m, " ", "+")
    elif (s.has_p(m, "zol")):
        m = s.rm_p(m, "zol")
        url = "http://detail.zol.com.cn/index.php?c=SearchList^&kword=" + s.str_to_hex_str(m)
    elif (s.has_p(m, "tyc")):
        m = s.rm_p(m, "tyc")
        url = "https://www.tianyancha.com/search?key=" + s.cv(m, " ", "%20")
    elif (s.has_p(m, "yd")):
        m = s.rm_p(m, "yd")
        url = "http://dict.youdao.com/w/" + s.cv(m, " ", "_")
    elif (s.has_p(m, "wb")):
        m = s.rm_p(m, "wb")
        url = "https://s.weibo.com/weibo?q=" + s.cv(m, " ", "%20")
    elif (s.has_p(m, "lj")):
        m = s.rm_p(m, "lj")
        url = "https://bj.lianjia.com/xiaoqu/rs" + m + "/"
    elif (s.has_p(m, "ah")):
        m = s.rm_p(m, "ah")
        url = "https://sou.autohome.com.cn/zonghe?q=" + s.str_to_hex_str(m)
    elif (s.has_p(m, "lj")):
        m = s.rm_p(m, "lj")
        url = "https://sou.autohome.com.cn/luntan?q=" + s.str_to_hex_str(m)
    elif (s.has_p(m, "jd")):
        m = s.rm_p(m, "jd")
        url = "https://search.jd.com/Search?mword=" + s.cv(m, " ", "%20") + "^&enc=utf-8"
    elif (s.has_p(m, "jdl")):
        m = s.rm_p(m, "jdl")
        url = "https://order.jd.com/center/search.action?mword=" + s.str_to_hex_str(m)
    elif (s.has_p(m, "tb")):
        m = s.rm_p(m, "tb")
        url = "https://s.taobao.com/search?q=" + s.cv(m, " ", "+")
    elif (s.has_p(m, "xm")):
        m = s.rm_p(m, "xm")
        url = "https://search.mi.com/search_" + s.cv(m, " ", "%20")
    elif (s.has_p(m, "xml")):
        m = s.rm_p(m, "xml")
        url = "https://static.mi.com/order/#type=12&mwords=" + m
    elif (s.has_p(m, "gp")):
        m = s.rm_p(m, "gp")
        url = "http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=" + s.cv(m, " ", "+") + "&country=stock"
    elif (s.has_p(m, "gg")):
        m = s.rm_p(m, "gg")
        url = "http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=" + s.cv(m, " ", "+") + "&country="
    elif (s.has_p(m, "mg")):
        m = s.rm_p(m, "mg")
        url = "http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=" + s.cv(m, " ", "+") + "&country="
    elif (s.has_p(m, "ji")):
        m = s.rm_p(m, "ji")
        url = "https://vitria.atlassian.net/browse/" + m
    else:
        url = "https://www.baidu.com/s?wd=" + s.cv(m, " ", "%20")

    if (mx):
        open_maxthon(url)
    elif (cr):
        open_chrome(url)
    elif (ie):
        open_iexplore(url)
    elif (ff):
        open_firefox(url)
    else:
        open_maxthon(url)


def do_notification_models():
        from subconsole import sub_console

        class notification_models_sub_console(sub_console):
            
            models__ = {
                "VIAOps Incident Notification": [
                    "RT VIAOps Incident Notification",
                    "RT VIAOps Incident Notification Email Target",
                    "RT VIAOps Incident Notification HDFS Target",
                    "RT VIAOps Incident Notification Kafka Target",
                    "RT VIAOps Incident Notification SNMP Target",
                    "RT VIAOps Incident Notification Summary",
                    "RT VIAOps Incident Rescoring and Prescription",
                    "VIAOps Incident Notification Subflow - Common",
                    "VIAOps Incident Notification Subflow - Notification Targets",
                    "VIAOps Incident Notification Subflow - Pull Action Ref Data",
                ],
                "VIAOps Single Incident Notification": [
                    "RT Incident Notification Single Metric",
                    "RT Subflow - Pull Action Ref Data Single Metric",
                ],
                "VIAOps Ingestion": [
                    "VIAOps - Aggregate Output MetricReferenceData Template",
                    "VIAOps - Dropped Events Template",
                    "VIAOps - File Source Template",
                    "VIAOps - Internal Audit Log Template",
                    "VIAOps - Schema Shared",
                    "VIAOps - Tool Repair Table",
                ],
                "VIAOps Incident": [
                    "RT VIAOps Declared Incident",
                    "RT VIAOps Incident Grouping",
                    "RT VIAOps Scored Incident",
                    "RT VIAOps Simple Deviation Incident",
                    "RT VIAOps Simple Threshold Incident",
                    "RT VIAOps Store Incident DA",
                    "SF VIAOps Adhoc Incident",
                    "SF VIAOps Contextual Metric Enrichment",
                    "SF VIAOps Incident Group",
                    "SF VIAOps Incident Service",
                    "SF VIAOps Scored Incident Evaluation",
                    "SF VIAOps Simple Deviation Incident Evaluation",
                    "SF VIAOps Simple Threshold Incident Evaluation",
                    "VIAOps Incident Group Service",
                    "VIAOps Incident Service",
                    "VIAOps Incident Subflow",
                ],
                "VIAOps DO Monitoring": [
                    "Adhoc Parse Query Performance Monitoring",
                    "DO Action Performance Metric Table",
                    "DO Incident Group Performance Metric Table",
                    "DO Incident Performance Metric Table",
                    "DO Monitoring Metric Table",
                    "RT Parse DataSource Performance Monitoring",
                    "RT Parse Incident Performance Metric",
                    "RT Parse Query Performance Monitoring",
                ],
            }
            
            ip = "localhost"
            port = "8080"
            space = "VIAOps Incident Notification"
            
            def n(self):
                return self.space
            
            def callback(self, m):
                m = self.translate(m)
                if (m):
                    self.try_(self.main__, m)
            
            def translate(self, m):
                m00 = m
                m = self.v_(m)
                if (m == None):
                    return m
                m = self.vm_(m)
                if (m == None):
                    return m
                m = self.sw_(m)
                if (m == None):
                    return m
                m = self.ci_(m)
                if (m == None):
                    return m
                ulog.log_trans(m00, m)
                return m

            def v_(self, m):
                if (m == "v"):
                    log()
                    log("ip    = " + self.ip)
                    log("port  = " + self.port)
                    log("space = " + self.space)
                    log()
                    return None
                return m

            def vm_(self, m):
                if (m == "vm"):
                    log()
                    ulog.logl(self.n(), self.models__[self.space])
                    log()
                    return None
                return m

            def sw_(self, m):
                if (m == "aws"):
                    self.ip = "54.84.45.75"
                    self.port = "18080"
                    self.v_("v")
                    return None
                if (m == "sp"):
                    spaces = list(self.models__.keys())
                    self.space = ulist.select("spaces", spaces)
                    self.vm_("vm")
                    return None
                return m

            def ci_(self, m):
                if (m == "ci"):
                    log()
                    text = ulist.select(self.n(), self.models__[self.space])
                    if (not text == None and not text == ""):
                        ci.set_text(text)
                        ci.logci(text)
                    return None
                elif (s.st(m, "ci ")):
                    log()
                    m = s.cf(m, "ci ")
                    l = self.models__[self.space]
                    l = s._filter_(l, s.isf, m)
                    text = ulist.select(self.n(), l)
                    if (not text == None and not text == ""):
                        ci.set_text(text)
                        ci.logci(text)
                    return None
                return m
            
            def clean(self, m):  # @UnusedVariable
                return m
            
            def main__(self, m):
                self.do_go_model(m)
                return m
            
            def do_go_model(self, m):
                if (m == "m"):
                    l = self.models__[self.space]
                else:
                    l = s._filter_(self.models__[self.space], s.isf, m)
                log()
                n = ulist.select(self.n(), l)
                if (not n == None and not n == ""):
                    self.do_go_model__(n)
                    log()
            
            def do_go_model__(self, n):
                url = "http://{0}:{1}/vitria-oi/app/?username=vtbaadmin&password=vitria#uri=/app/spark/space/{2}/sparkm/{3}"
                log("open: " + n)
                n = s.cv(n, " ", "%20")
                url = url.format(self.ip, self.port, self.space, n)
                try:
                    ulog.tmp_silent()
                    open_chrome(url)
                finally:
                    ulog.no_tmp_silent()
            
        notification_models = notification_models_sub_console()
        notification_models.run()

