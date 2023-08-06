import ustring         as s
from   ulog            import log

import cons            as cons
import ulog            as ulog
import fileio          as fileio


def translate(m):
    m00 = m
    m = jz(m)
    m = view_stock(m)
    ulog.log_trans(m00, m)
    return m


def jz(m):
    if (m == "jz"):
        m = "..  sz;ok;hgt[]"
    return m


def view_stock(m):
    stock_codes = get_stock_codes()
    if (stock_codes.__contains__(m)):
        m = "stock " + stock_codes[m]
    return m


def handle(m):
    stock_info = get_sina_stock(m)
    log(stock_info)


def get_sina_stock(code):  # alias is shortcuts, like gzmt, xmjt
    code = resolve_code(code)
    url = "http://hq.sinajs.cn/?format=text&list=" + code
    import requests
    text = requests.get(url).text
    arr = s.sp(text, ",")
    if (s.st(code, "hk")):
        name = arr[1]
        last_price = arr[3]
        price = arr[6]
    else:
        name = arr[0]
        last_price = arr[2]
        price = arr[3]
    return {"name":name, "last_price":last_price, "price":price}


def resolve_code(code):
    if (not s.is_number(s.sl(code, 1))):
        stock_codes = get_stock_codes()
        return stock_codes[code]
    return code


def get_stock_price(code):
    return get_sina_stock(code)["price"]


def get_stock_codes():
    if (cons.stock_codes == None):
        f = s.bat_("gp")
        lines = fileio.l(f)
        cons.stock_codes = dict()
        for line in lines:
            arr = s.sp(line, " ")
            cons.stock_codes[arr[0]] = arr[1]
    return cons.stock_codes

