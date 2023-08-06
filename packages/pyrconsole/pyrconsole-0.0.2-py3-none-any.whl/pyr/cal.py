import ustring         as s
from   ulog            import log

import cons            as cons
import ulog            as ulog


def translate(m):
    m00 = m
    m = trans_cal(m)
    m = fang_jia(m)
    m = cal_total(m)
    ulog.log_trans(m00, m)
    return m


def trans_cal(m):
    if (((s.ct(m, "+", "-", "*", "/") and s.nct(m, " ") and not s.end(m, "-") and len(m) >= 3) or s.ct(m, " + ", " - ", " * ", " / ")) and (s.is_number(m[0]) or (s.iss(m[0], "-", "(") and s.is_number(m[1])))):
        m = "cal " + m
    return m


def fang_jia(m):
    if (s.st(m, "fangjia ")):
        m = s.cf(m, "fangjia ")
        w = 10000
        price = float(m) * w
        cost = 150 * w
        month = 71
        daikuan = 1.3 * w * month
        lixi = daikuan * 0.65
        benjin = daikuan * 0.35
        touru = cost + lixi
        jiazhi = price * 70 - 225 * w + benjin
        jiazhi = jiazhi / w
        log("jiazhi:   %.2f" % jiazhi)
        touru = touru / w
        log("touru:    %.2f" % touru)
        lixi = lixi / w
        log("lixi:      %.2f" % lixi)
        yingli = (jiazhi - touru) * 100 / touru
        log("yingli:   %.2f" % yingli + "%")
        import math
        nianhua = math.pow(1 + yingli / 100, 1 / 6)
        nianhua = (nianhua - 1) * 100
        log("nianhua:   %.2f" % nianhua + "%")
        m = cons.ignore_cmd
    return m


def cal_total(m):
    if (m in ["cal total", "calt"]):
        do_cal_total()
        m = cons.ignore_cmd
    return m


def do_cal_total():
    import traceback
    from subconsole import sub_console

    class cal_sub_console(sub_console):
        total = 0
        precision = 2
        
        def n(self):
            return "calculate total"
        
        def help(self):
            cal_help = {
                "a b"   : "a ^ b",
                ".n"    : "precision to n",
                "v"     : "view total",
                "va"    : "view precision",
                "ci"    : "copy total to clipboard",
                "syl x" : "calculate PE, x is increase percentage",
            }
            return cal_help
        
        def callback(self, m):
            m = self.translate_pow(m)
            if (s.ct(m, " ^ ")):
                m = self.try_(self.pow__, m)
                if (m == None):
                    return
            m = self.translate(m)
            self.try_(self.main__, m)
        
        def translate_pow(self, m):
            if (s.n(m, " ") == 1 and s.is_number(s.lf(m, " "))):
                m = s.cv(m, " ", " ^ ")
            return m
        
        def translate(self, m):
            m00 = m
            
            m = self.v_(m)
            if (m == None):
                return m
            m = self.va_(m)
            if (m == None):
                return m
            m = self.ci_(m)
            if (m == None):
                return m
            m = self.precision_(m)
            if (m == None):
                return m
            m = self.syl_(m)
            if (m == None):
                return m
            
            # no comma
            m = s.cv(m, ",", "")
            # percentage
            if (s.end(m, "p")):
                m = s.cl(m, "p")
                m = "* {0}%".format(m)
            # w
            m = s.cv(m, "w", " * 10000")
            
            ulog.log_trans(m00, m)
            return m

        def ci_(self, m):
            if (m == "ci"):
                import ci
                text = str(self.total)
                ci.set_text(text)
                log()
                ci.logci(text)
                m = None
            return m
        
        def precision_(self, m):
            if (s.match(m, "\\.\\d")):
                self.precision = int(s.cf(m, "."))
                self.v_("v")
                m = None
            return m
        
        def syl_(self, m):
            if (s.st(m, "syl ")):
                m = s.cf(m, "syl ")
                rate = float(m) / 100 + 1
                r = 0
                base = 1
                for i in range(10):  # @UnusedVariable
                    base *= rate
                    r += base
                log()
                log("PE: " + self.f_(r))
                log()
                m = None
            return m
        
        def v_(self, m):
            if (m == "v"):
                log()
                log("total: " + self.f_(self.total))
                log()
                return None
            return m

        def va_(self, m):
            if (m == "va"):
                log()
                log("precision = " + str(self.precision))
                log()
                return None
            return m

        def clean(self, m):  # @UnusedVariable
            self.total = 0
            m = "0"
            return m

        def pow__(self, m):
            a = s.trim(s.lf(m, " ^ "))
            a = s.cv(a, ",", "")
            a = float(a)
            b = s.trim(s.clf(m, " ^ "))
            b = s.cv(b, ",", "")
            b = float(b)
            import math
            self.total = math.pow(a, b)
            m = "0"
            return m
        
        def main__(self, m):
            if (s.st(m, "+", "-", "*", "/")):
                op = m[0]
                args = s.trim(s.cf(m))
                m = op + " " + args
                to_eval = translate_expression(m)
                to_eval = str(self.total) + " " + to_eval
                self.total = float(eval(to_eval))
            else:
                to_eval = translate_expression(m)
                self.total += float(eval(to_eval))
            log()
            log("total: " + self.f_(self.total))
            log()
            return m
        
        def f_(self, f):
            f__ = "{0:0,." + str(self.precision) + "f}"
            return f__.format(f)

    cal = cal_sub_console()
    cal.run()


def handle(m):
    to_eval = translate_expression(m)
    result = '%.2f' % float(eval(to_eval))
    log(m + " = " + result)
    cons.cal_result = result


def translate_expression(m):
    m00 = m
    m = no_comma(m)
    m = percentage(m)
    ulog.log_trans(m00, m)
    return m


def no_comma(m):
    m = s.cv(m, ",", "")
    return m


def percentage(m):
    while (s.ct(m, "%")):
        left = s.lf(m, "%")
        num = s.rt(left, " ")
        m = s.cv(m, num + "%", "(" + num + " / 100)")
    return m

