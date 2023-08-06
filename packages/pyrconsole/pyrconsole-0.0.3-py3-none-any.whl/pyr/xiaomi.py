import ustring         as s
from   ulog            import log

import cons            as cons
import env             as env
import fileio          as fileio
import lastop          as lastop
import ulog            as ulog

gu_ben = {
    "xm" : "251.97",
    "tx" : "95.95",
    "mt" : "58.88",
}

gu_jia = {
    "xm" : "29.55",
    "tx" : "745",
    "mt" : "439.2",
}

cheng_ben = {
    "xm": {
        "price" : "17.709",
        "count" : "54200",
    },
    "tx": {
        "price" : "337.600",
        "count" : "200",
    },
}


def translate(m):
    m00 = m
    m = tr_huilv(m)
    ulog.log_trans(m00, m)
    return m


def tr_huilv(m):
    if (m in ["h hl", "hl?"]):
        huilv_help = {
            "start"     : "input \"hl\" in Python R to start",
            "output"    : "each line output the calculate result in three formats: HK, RMB, US",
            "hk/rmb/us" : "change the default currency",
            "xm 30"     : "specify price of xiaomi",
            "tx 800"    : "specify price of tencent",
            "yl"        : "calculate earnings",
            "yl 30"     : "calculate earnings based on xiaomi price: 30",
            "yl 30-40"  : "calculate earnings based on xiaomi price: from 30 to 40, interval is 1",
            "yl 30-40 " : "calculate earnings based on xiaomi price: from 30 to 40, interval is 0.1",
            "sz"        : "calculate market value",
            "only"      : "only number",
            "c"         : "view only number",
            "v"         : "clean up",
        }
        ulog.logh("huilv", huilv_help)
        m = cons.ignore_cmd
    if (m == "hl"):
        log()
        huilv_input = input("huilv [HK -> RMB or US -> RMB]: ")
        if (huilv_input == ""):
            huilv_input = lastop.do_get_last_input("huilv") + " from_history"
        else:
            lastop.do_put_last_input("huilv", huilv_input)
        if (not huilv_input == cons.ignore_cmd):
            m = "xiaomi huilv " + huilv_input
        else:
            m = cons.ignore_cmd
        log()
    return m


def handle(m):
    if (m == "price"):
        do_price()
    if (s.st(m, "huilv ")):
        m = s.cf(m, "huilv ")
        do_huilv(m)


def do_price():
    price = float(input("HK Dollar: "))
    log()
    gu = 251.441
    hk = price * gu
    log("HK:        {:.2f}".format(hk))
    rmb = price * gu * 0.845
    log("RMB:       {:.2f}".format(rmb))
    us = price * gu / 7.75
    log("US Dollar: {:.2f}".format(us))


def do_load_gujia():
    for k in gu_jia:
        gu_jia[k] = lastop.do_get_last_input(k)


def do_huilv(m):
        us_hk = 7.75
        hk_rmb = 0.83
        us_rmb = us_hk * hk_rmb
        
        do_load_gujia()
        
        from_history = s.has_p(m, "from_history")
        if (from_history):
            m = s.rm_p(m, "from_history")
        
        n = float(m)
        if (n < 1):
            hk_rmb = n
        elif (n > 6):
            us_rmb = n
            hk_rmb = us_rmb / us_hk
        
        from subconsole import sub_console

        class huilv_sub_console(sub_console):
            
            input = "hk"
            hk = 0
            rmb = 0
            us = 0
            view_only_number = False
            
            def n(self):
                return "huilv"
            
            def callback(self, m):
                if (s.st(m, "yl ") and s.ct(m, "-")):
                    self.do_callback_yl(m)
                elif (s.st(m, "xm ") and s.ct(m, "-")):
                    self.do_callback_xm(m)
                else:
                    m = self.translate(m)
                    if (m):
                        self.try_(self.main__, m)
            
            def do_callback_yl(self, m):
                m = s.cf(m, "yl ")
                if (s.end(m, " ")):
                    interval = 0.1
                else:
                    interval = 1
                m = s.trim(m)
                from_ = float(s.lf(m, "-"))
                to_ = float(s.clf(m, "-"))
                i = from_
                while (i <= to_):
                    log()
                    log("xiaomi price: " + "{0:0,.2f}".format(i))
                    try:
                        ulog.increase_log_tab(4, all_=True)
                        m = "yl " + "{0:0,.2f}".format(i)
                        m = self.translate(m)
                        self.try_(self.main__, m)
                        i += interval
                    finally:
                        ulog.decrease_log_tab(4, all_=True)
            
            def do_callback_xm(self, m):
                m = s.cf(m, "xm ")
                if (s.end(m, " ")):
                    interval = 0.1
                else:
                    interval = 1
                m = s.trim(m)
                from_ = float(s.lf(m, "-"))
                to_ = float(s.clf(m, "-"))
                i = from_
                while (i <= to_):
                    log()
                    log("xiaomi price: " + "{0:0,.2f}".format(i))
                    try:
                        ulog.increase_log_tab(4, all_=True)
                        m = "xm " + "{0:0,.2f}".format(i)
                        m = self.translate(m)
                        self.try_(self.main__, m)
                        i += interval
                    finally:
                        ulog.decrease_log_tab(4, all_=True)
            
            def translate(self, m):
                m00 = m
                m = self.only_(m)
                if (m == None):
                    return m
                m = self.clean_up_(m)
                if (m == None):
                    return m
                m = self.va_(m)
                if (m == None):
                    return m
                m = self.v_(m)
                if (m == None):
                    return m
                m = self.vj_(m)
                if (m == None):
                    return m
                m = self.vc_(m)
                if (m == None):
                    return m
                for k in gu_ben:
                    if (s.st(m, k + "sz")):
                        m = s.trim(s.cf(m, k + "sz"))
                        m = m + " / " + gu_ben[k]
                    if (s.st(m, k + "yl")):
                        m = s.trim(s.cf(m, k + "yl"))
                        m = "({0} - {1}) * {2}".format(m, cheng_ben[k]["price"], cheng_ben[k]["count"])
                    elif (s.st(m, k)):
                        m = s.trim(s.cf(m, k))
                        gu_jia[k] = m
                        lastop.do_put_last_input(k, m)
                        m = m + " * " + gu_ben[k]
                if (s.st(m, "yl ")):
                    m = s.cf(m, "yl ")
                    if (s.ct(m, " ")):
                        gu_jia["xm"] = s.lf(m, " ")
                        gu_jia["tx"] = s.clf(m, " ")
                    else:
                        gu_jia["xm"] = m
                    m = "yl"
                if (m == "yl"):
                    m = ""
                    for k in cheng_ben:
                        m += "{0} * {1}".format(gu_jia[k], cheng_ben[k]["count"])
                        m += " + "
                    m = m + "1053.41 / " + str(hk_rmb)
                    m = m + " - 790000 / " + str(hk_rmb)
                if (m == "sz"):
                    m = ""
                    for k in cheng_ben:
                        m += "{0} * {1}".format(gu_jia[k], cheng_ben[k]["count"])
                        m += " + "
                    m = m + "1053.41 / " + str(hk_rmb)
                ulog.log_trans(m00, m)
                return m
            
            def only_(self, m):
                if (m == "only"):
                    log()
                    log("only number")
                    log()
                    self.view_only_number = True
                    return None
                return m

            def clean_up_(self, m):
                if (m == "c"):
                    log()
                    log("clean up")
                    log()
                    self.view_only_number = False
                    return None
                return m

            def va_(self, m):
                if (m == "va"):
                    self.v_("v")
                    self.vc_("vc")
                    self.vj_("vj")
                    return None
                return m

            def v_(self, m):
                if (m == "v"):
                    log()
                    log("view_only_number = " + str(self.view_only_number))
                    log()
                    return None
                return m

            def vj_(self, m):
                if (m == "vj"):
                    log()
                    for k in gu_jia:
                        log("{0:6}{1:>8}".format(k + ":", "{0:0,.2f}".format(float(gu_jia[k]))))
                    log()
                    return None
                return m

            def vc_(self, m):
                if (m == "vc"):
                    log()
                    log("{0:6}{1:>8}".format("HK -> RMB" + ":", "{0:0,.4f}".format(float(hk_rmb))))
                    log("{0:6}{1:>8}".format("US -> RMB" + ":", "{0:0,.4f}".format(float(us_rmb))))
                    log()
                    return None
                return m
            
            def clean(self, m):  # @UnusedVariable
                return m
            
            def main__(self, m):
                if (m == "v"):
                    self.do_v()
                elif (m == "use"):
                    self.do_v_use()
                elif (m in ["hk", "rmb", "us"]):
                    self.input = m
                    log()
                    log("use: " + m)
                    log()
                else:
                    self.do_cal(m)
                return m
            
            def do_v(self):
                us_rmb = hk_rmb * 7.75
                log()
                log("HK -> RMB: {0:0,.4f}".format(hk_rmb))
                log("US -> RMB: {0:0,.4f}".format(us_rmb))
                log()
            
            def do_v_use(self):
                log()
                log("use: " + self.input)
                log()

            def do_eval(self, m):
                import cal
                to_eval = cal.translate_expression(m)
                result = '%.2f' % float(eval(to_eval))
                return result
            
            def do_cal(self, m):
                m = self.do_eval(m)
                if (self.input == "hk"):
                    self.hk = float(s.trim(m))
                    self.rmb = self.hk * hk_rmb
                    self.us = self.hk / us_hk
                elif (self.input == "rmb"):
                    self.rmb = float(s.trim(m))
                    self.hk = self.rmb / hk_rmb
                    self.us = self.hk / us_hk
                elif (self.input == "us"):
                    self.us = float(s.trim(m))
                    self.hk = self.us * us_hk
                    self.rmb = self.hk * hk_rmb
                self.view__()
            
            def view__(self):
                log()
                if (self.view_only_number):
                    log("{0:>12}".format("{0:0,.2f}".format(self.rmb)))
                else:
                    log("hk:  {0:>12}".format("{0:0,.2f}".format(self.hk)))
                    log("rmb: {0:>12}".format("{0:0,.2f}".format(self.rmb)))
                    log("us:  {0:>12}".format("{0:0,.2f}".format(self.us)))
                log()
    
        huilv = huilv_sub_console()
        huilv.do_v()
        huilv.run()

