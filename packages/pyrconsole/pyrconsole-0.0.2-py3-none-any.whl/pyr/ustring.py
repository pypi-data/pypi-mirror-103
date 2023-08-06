import cons            as cons

# xxx.encode('utf-8')
ju_hao           = b'\xe3\x80\x82'.decode("utf-8")
wen_hao          = b'\xef\xbc\x9f'.decode("utf-8")
dou_hao          = b'\xef\xbc\x8c'.decode("utf-8")
fen_hao          = b'\xef\xbc\x9b'.decode("utf-8")
mao_hao          = b'\xef\xbc\x9a'.decode("utf-8")
dun_hao          = b'\xe3\x80\x81'.decode("utf-8")
liang_ge_kong_ge = b'\xe3\x80\x80\xe3\x80\x80'.decode("utf-8")


def af(s, n):
    if (not st(s, n)):
        s = n + s
    return s


def al(s, n):
    if (not end(s, n)):
        s = s + n
    return s


def lf(s, sep):
    if (ct(s, sep)):
        return s[0: s.find(sep)]
    return s


def lfw(s, sep):
    if (ct(s, sep)):
        return s[0: s.find(sep) + len(sep)]
    return s


def rt(s, sep):
    if (ct(s, sep)):
        return s[s.rfind(sep) + len(sep): len(s)]
    return s


def rtw(s, sep):
    if (ct(s, sep)):
        return s[s.rfind(sep): len(s)]
    return s


def clf(s, sep):
    if (ct(s, sep)):
        return s[s.find(sep) + len(sep): len(s)]
    return s


def clf_(s, sep, n=1):  # repeat
    for i in range(n):  # @UnusedVariable
        s = trimleft(clf(s, sep))
    return s


def clfw(s, sep):
    if (ct(s, sep)):
        return s[s.find(sep): len(s)]
    return s


def crt(s, sep):
    if (ct(s, sep)):
        return s[0: s.rfind(sep)]
    return s


def crtw(s, sep):
    if (ct(s, sep)):
        return s[0: s.rfind(sep) + len(sep)]
    return s


def cf(s, *p):
    if (len(p) == 0):
        p = [1]
    for i in p:
        s00 = s
        s = cf_one(s, i)
        if (s00 != s):
            break
    return s


def cf_eq(s, p):
    if (s == p):
        return ""
    elif (st(s, p)):
        return cf(s, p)
    else:
        return s


def cf_one(s, p):
    if (isinstance(p, int)):
        return s[int(p): len(s)]
    else:
        if (st(s, p)):
            return s[len(p): len(s)]
    return s


def cl(s, *p):
    if (len(p) == 0):
        p = [1]
    for i in p:
        s00 = s
        s = cl_one(s, i)
        if (s00 != s):
            break
    return s


def cl_eq(s, p):
    if (s == p):
        return ""
    elif (end(s, p)):
        return cl(s, p)
    else:
        return s


def cl_one(s, p):
    if (isinstance(p, int)):
        return s[0: len(s) - int(p)]
    else:
        if (end(s, p)):
            return s[0: len(s) - len(p)]
    return s


def sf(s, n):
    if (n < 0):
        n = len(s) + n
    return s[0: n]


def sl(s, n):
    if (n < 0):
        n = len(s) + n
    return s[len(s) - n: len(s)]


def st(s, *p):
    if (s != None):
        for i in p:
            if (do_st(s, i)):
                return True
    return False


def stic(s, *p):
    if (s != None):
        for i in p:
            if (do_stic(s, i)):
                return True
    return False


def nst(s, *p):
    if (s != None):
        for i in p:
            if (do_st(s, i)):
                return False
    return True


def nstic(s, *p):
    if (s != None):
        for i in p:
            if (do_stic(s, i)):
                return False
    return True


def end(s, *p):
    if (s != None):
        for i in p:
            if (do_end(s, i)):
                return True
    return False


def endic(s, *p):
    if (s != None):
        for i in p:
            if (do_endic(s, i)):
                return True
    return False


def nend(s, *p):
    if (s != None):
        for i in p:
            if (do_end(s, i)):
                return False
    return True


def nendic(s, *p):
    if (s != None):
        for i in p:
            if (do_endic(s, i)):
                return False
    return True


def do_st(s, i):
    return s.startswith(i) and not s == i


def do_stic(s, i):
    s = s.lower()
    i = i.lower()
    return s.startswith(i) and not s == i


def do_end(s, i):
    return s.endswith(i) and not s == i


def do_endic(s, i):
    s = s.lower()
    i = i.lower()
    return s.endswith(i) and not s == i


def ct(s, *p):
    if (s != None):
        for i in p:
            if (do_ct(s, i)):
                return True
    return False


def ctic(s, *p):
    if (s != None):
        for i in p:
            if (do_ctic(s, i)):
                return True
    return False


def ctic_isf(s, *p):
    if (s != None):
        for i in p:
            if (do_ctic_isf(s, i)):
                return True
    return False


def ctic_con(s, p):
    if (s != None):
        if (is_wrapped(p, "in()")):
            return in_(s, unwrap(p, "in()"))
        elif (is_wrapped(p, "match()")):
            return match(s, unwrap(p, "match()"))
        case = has_p(p, "c")
        if (case):
            p = rm_p(p, "c")
        ct_func = [ct, ctic][not case]
        if (ct(p, "and(", "or(", "not(")):
            and_list = find_wrapped_list(p, "and()")
            p = rm_wrapped_all(p, "and()")
            or_list = find_wrapped_list(p, "or()")
            p = rm_wrapped_all(p, "or()")
            not_list = find_wrapped_list(p, "not()")
            p = rm_wrapped_all(p, "not()")
    
            for or_key in or_list:
                if (ct_func(s, or_key)):
                    return True
            if (not ct_func(s, p)):
                return False
            for not_key in not_list:
                if (ct_func(s, not_key)):
                    return False
            for and_key in and_list:
                if (not ct_func(s, and_key)):
                    return False
            return True
        else:
            return ct_func(s, p)
    return False


def nct(s, *p):
    if (s != None):
        for i in p:
            if (do_ct(s, i)):
                return False
    return True


def nctic(s, *p):
    if (s != None):
        for i in p:
            if (do_ctic(s, i)):
                return False
    return True


def nctic_isf(s, *p):
    if (s != None):
        for i in p:
            if (do_ctic_isf(s, i)):
                return False
    return True


def do_ct(s, i):
    return s.find(i) > -1


def do_ctic(s, i):
    return s.lower().find(i.lower()) > -1


def do_ct_isf(s, i):
    if (ct(i, "##")):
        for ii in i.split("##"):
            if (do_ct(s, ii)):
                return True
        return False
    else:
        return do_ct(s, i)


def do_ctic_isf(s, i):
    if (ct(i, "##")):
        for ii in i.split("##"):
            if (do_ctic(s, ii)):
                return True
        return False
    else:
        return do_ctic(s, i)


def isf(s, p):
    if (s != None):
        if (p == None or p == ""):
            return True
        if (st(p, "no ")):
            p = cf(p, "no ")
            return not isf_or(s, p)
        
        keys = to_isf_keys(p)
        for i in keys:
            if (is_wrapped(i, "or()")):
                i = unwrap(i, "or()")
                if (isf(s, i)):
                    return True
        
        for i in keys:
            if (is_wrapped(i, "not()")):
                i = unwrap(i, "not()")
                if (isf(s, i)):
                    return False
        
        for i in keys:
            if (is_wrapped(i, "or()")):
                pass
            elif (is_wrapped(i, "not()")):
                pass
            elif (is_wrapped(i, "()")):
                i = unwrap(i, "()")
                if (not eq(s, i)):
                    return False
            elif (is_wrapped(i, "st()")):
                i = unwrap(i, "st()")
                if (not stic(trimleft(s), i)):
                    return False
            elif (is_wrapped(i, "end()")):
                i = unwrap(i, "end()")
                if (not endic(s, i)):
                    return False
            elif (is_wrapped(i, "fn()")):
                i = unwrap(i, "fn()")
                if (not isf(_r_("fileio.get_file_name", s), i)):
                    return False
            else:
                if (nctic_isf(s, i)):
                    return False
        return True
    return False


def to_isf_keys(m):
    left_indent = get_left_indent(m)
    right_indent = get_right_indent(m)
    if (left_indent != "" or right_indent != ""):
        m = cf(m, left_indent)
        m = cl(m, right_indent)
        isf_keys = to_isf_keys_parts(m)
        isf_keys[0] = left_indent + isf_keys[0]
        isf_keys[len(isf_keys) - 1] = isf_keys[len(isf_keys) - 1] + right_indent
        return isf_keys
    isf_keys = to_isf_keys_parts(m)
    return isf_keys


def to_isf_keys_parts(m):
    ks = []
    while (True):
        found = None
        if (st(m, "st(")):
            found = find_wrapped_with(m, "st()")
        elif (st(m, "end(")):
            found = find_wrapped_with(m, "end()")
        elif (st(m, "or(")):
            found = find_wrapped_with(m, "or()")
        elif (st(m, "not(")):
            found = find_wrapped_with(m, "not()")
        elif (st(m, "(")):
            found = find_wrapped_with(m, "()")
        else:
            found = lf(m, " ")
        ks.append(found)
        if (m == found):
            break
        else:
            m = trimleft(cf(m, found))
    return ks


def isf_or(s, p):
    if (s != None):
        for i in p.split(" "):
            if (ctic_isf(s, i)):
                return True
    return False


def n(s, p):
    return s.count(p)


def cv(s, a, b):
    if (s != None):
        if (ct(s, a)):
            return s.replace(a, b)
    return s


def cvic(s, a, b):
    if (s != None):
        output = s
        from_s = a
        to_s = b
        camel_case = None
        upper_case = None
        lower_case = None  # @UnusedVariable
        output = output.replace(to_lower_case(from_s), "__LOWER_CASE__")
        lower_case = to_lower_case(to_s)
        if (need_upper(from_s, to_s)):
            output = output.replace(to_upper_case(from_s), "__UPPER_CASE__")
            upper_case = to_upper_case(to_s)
        if (need_camel(from_s, to_s)):
            output = output.replace(to_camel_case(from_s), "__CAMEL_CASE__")
            camel_case = to_camel_case(to_s)
        if (camel_case != None):
            output = output.replace("__CAMEL_CASE__", camel_case)
        if (upper_case != None):
            output = output.replace("__UPPER_CASE__", upper_case)
        if (lower_case != None):
            output = output.replace("__LOWER_CASE__", lower_case)
        return output
    return s


def cv_(s, func, *args):  # map
    if (s != None):
        if (isinstance(s, list)):
            return list(map(lambda x: func(x, *args), s))
        else:
            return func(s, *args)
    return s


def _cv_(s, func, *args):  # map
    return cv_(s, func, *args)


def filter_(lines, p, func=isf):  # filter
    if (lines != None):
        is_str = False
        if (isinstance(lines, str)):
            lines = sp(lines)
            is_str = True
        if (isinstance(p, list)):

            def filter_func(x, p):
                for i in p:
                    if (func(x, i)):
                        return True
                return False

            lines = list(filter(lambda x:filter_func(x, p), lines))
        else:
            lines = list(filter(lambda x:func(x, p), lines))
        if (is_str):
            lines = conn(lines)
    return lines


def _filter_(lines, func=isf, *args):  # filter
    if (lines != None):
        is_str = False
        if (isinstance(lines, str)):
            lines = sp(lines)
            is_str = True
        lines = list(filter(lambda x:func(x, *args), lines))
        if (is_str):
            lines = conn(lines)
    return lines


def need_upper(from_s, to_s):
    return from_s != to_upper_case(from_s) or to_s != to_upper_case(to_s)


def need_camel(from_s, to_s):
    return from_s != to_camel_case(from_s) or to_s != to_camel_case(to_s)


def is_chinese(word):
    if (word != None):
        for ch in word:
            if (is_chinese_char(ch)):
                return True
    return False


def is_chinese_char(ch):
    if (ch != None):
        return '\u4e00' <= ch <= '\u9fff'
    return False


def is_first_chinese(word):
    if (word != None):
        first = word[0:1]
        return is_chinese(first)
    return False


def is_number(s):
    if (s != None):
        return s.isnumeric()
    return False


def str_to_hex_str(string):
    str_bin = string.encode('GBK')
    import binascii
    hex_str = binascii.hexlify(str_bin).decode('GBK')
    out = ''
    for i in range(int(len(hex_str) / 2)):
        out += '%' + hex_str[2 * i:2 * i + 2].upper()
    return out


def rm(s, *p):
    if (s != None):
        for i in p:
            s = cv(s, i, "")
    return s


def trim(s):
    if (s != None):
        if (isinstance(s, list)):
            trimmed = []
            for i in s:
                trimmed.append(trim(i))
            return trimmed
        else:
            return s.strip()
    return s


def trimleft(s):
    if (s != None):
        if (isinstance(s, list)):
            trimmed = []
            for i in s:
                trimmed.append(trim(i))
            return trimmed
        else:
            return s.lstrip()
    return s


def trimright(s):
    if (s != None):
        if (isinstance(s, list)):
            trimmed = []
            for i in s:
                trimmed.append(trim(i))
            return trimmed
        else:
            return s.rstrip()
    return s


def c(s, a, b):
    if (s != None):
        s = clf(s, a)
        s = lf(s, b)
    return s


def c_2(s, a, b):  # find () or or()
    if (s != None):
        if (ct(s, a)):
            start = s.find(a) + len(a)
            n = 1
            idx = start
            if (len(a) > 1):
                a = sl(a, 1)
            while (True):
                ch = s[idx]
                if (ch == a):
                    n += 1
                elif (ch == b):
                    n -= 1
                if (n == 0):
                    break
                idx += 1
                if (idx > len(s) - 1):
                    break
            end = idx
            return s[start:end]
    return None


def max_len_(l):  # return string
    num = 0
    r = ""
    for i in l:
        if (len(i) > num):
            num = len(i)
            r = i
    return r


def max_len(l):  # return length of string
    return len(max_len_(l))


def no_line_sep(l):
    return list(map(clean_line_sep, l))


def clean_line_sep(s):
    if (s == "\n"):
        return ""
    else:
        return cl(s, "\n")


def clean_line_sep_n(s):
    while (end(s, "\n")):
        s = cl(s, "\n")
    return s


def nul(s):
    return s == None or len(s) == 0


def nnl(s):
    return not nul(s)


def iss(s, *l):
    return eq(s, *l)


def eq(s, *l):
    if (s != None):
        for i in l:
            if (s == i):
                return True
    return False


def issic(s, *l):
    if (s != None):
        for i in l:
            if (s.lower() == i.lower()):
                return True
    return False


def match(s, *regex):
    if (s != None):
        import re
        for regexOne in regex:
            if (re.match("'" + regexOne + "'", "'" + s + "'") != None):
                return True
    return False


def get_param_match(s, regex):
    if (s != None):
        import re
        matched = re.match(" " + regex + " ", " " + s + " ")
        if (matched):
            return trim(matched.group())
    return None


def get_param_matches(s, regex):
    import re
    return trim(re.findall(" " + regex + " ", " " + s + " "))


def rm_param_match(s, regex):
    matched = get_param_match(s, regex)
    return trim(cv(" " + s + " ", " " + matched + " ", ""))


def sp(s, sep="\n", no_el=False):
    if (s != None):
        l = s.split(sep)
        if (no_el):
            l = noel(l)
        return l
    return s


def get_parts(s, format_line="", keys=["(;;)", ";;", ";", " "], no_el=True):
    if (s != None):
        for key in keys:
            if (ct(s, key)):
                l = sp(s, key)
                if (format_line != ""):
                    l = to_format_args(l, format_line, key)
                if (no_el):
                    l = get_parts_no_empty_str(l, key)
                return l
        return [s]
    return s


def to_format_args(l, format_line, key):  # {0:4}{1}
    if (ct(format_line, "{")):
        while (True):
            n = len(l)
            last_s = str(n - 1)
            last_ph = wrap(last_s, "{}")
            last_ph2 = wrap(last_s, "{:")
            if (ct(format_line, last_ph, last_ph2)):
                break
            else:
                l[n - 2] = l[n - 2] + key + l[n - 1]
                l.pop()
    return l


def get_parts_no_empty_str(l, key):
    append_keys = ""
    while (True):
        n = len(l)
        last = l[n - 1]
        if (last != ""):
            if (append_keys != ""):
                l[n - 1] += append_keys
            break
        else:
            append_keys += key
            l.pop()
    return l


def today():
    return now().strftime('%Y-%m-%d')


def today2():
    return now().strftime('%Y%m%d')


def today3():
    return now().strftime('%m%d')


def now():  # now time object
    import datetime
    return datetime.datetime.now()


def now4():
    return now().strftime('%Y-%m-%d %H:%M:%S')


def this_year():
    return lf(now4(), "-")


def nowts():  # milli seconds
    import time
    return int(round(time.time() * 1000))


def nowts_f():  # float seconds
    import time
    return time.time()


def count_chinese_characters(s):
    count = 0
    for ch in s:
        if (is_chinese(ch)):
            count = count + 1
    return count


def find_position(s, p):
    if (is_wrapped_(p, "st()", "()")):
        p = unwrap_(s, "st()", "()")
    index = s.lower().find(p.lower())
    left_part = s[0:index]
    chinese_characters = count_chinese_characters(left_part)
    return index, chinese_characters


def get_repeat_string(s, n):
    r = ""
    for i in range(n):  # @UnusedVariable
        r = r + s
    return r


def reverse(s):
    return s[::-1]


def get_indent_size(s):
    size = 0
    for ch in s:
        if (ch == " "):
            size = size + 1
        else:
            return size
    return size


def get_left_indent_size(s):
    return get_indent_size(s)


def get_right_indent_size(s):
    s = reverse(s)
    return get_indent_size(s)


def get_indent(s):
    return get_repeat_string(" ", get_indent_size(s))


def get_indent_string(n):
    return get_repeat_string(" ", n)


def get_left_indent(s):
    return get_repeat_string(" ", get_left_indent_size(s))


def get_right_indent(s):
    return get_repeat_string(" ", get_right_indent_size(s))


def wrap(s, wrappers="\""):
    if (len(wrappers) == 1):  # ""
        return wrappers + s + wrappers
    elif (len(wrappers) == 2):  # ()
        return wrappers[0] + s + wrappers[1]
    else:  # and()
        return sf(wrappers, -1) + s + sl(wrappers, 1)
    return s


def wrap_sp(s, c="\""):  # if starts or ends with space
    if (st(s, " ") or end(s, " ")):
        return wrap(s, c)
    return s


def unwrap(s, wrappers="\""):
    if (is_wrapped(s, wrappers)):
        return do_unwrap(s, wrappers)
    return s


def unwrap_(s, *wrappers):
    for a_wrappers in wrappers:
        if (do_is_wrapped(s, a_wrappers)):
            s = unwrap(s, a_wrappers)
    return s


def do_unwrap(s, wrappers=""):
    if (len(wrappers) <= 2):
        return s[1: len(s) - 1]
    else:
        return s[len(wrappers) - 1: len(s) - 1]


def is_wrapped(s, *wrappers):
    for a_wrappers in wrappers:
        if (do_is_wrapped(s, a_wrappers)):
            return True
    return False


def is_wrapped_(s, *wrappers):
    return is_wrapped(s, *wrappers)


def do_is_wrapped(s, wrappers):
    if (len(wrappers) == 1):  # ""
        return st(s, wrappers) and end(s, wrappers)
    elif (len(wrappers) == 2):  # ()
        return st(s, wrappers[0]) and end(s, wrappers[1])
    else:  # and()
        return st(s, sf(wrappers, -1)) and end(s, sl(wrappers, 1))
    return False


def has_wrapped(s, wrappers):
    wrapped = find_wrapped(s, wrappers)
    if (wrapped):
        wrapped_with_wrappers = wrap(wrapped, wrappers)
        return ct(s, wrapped_with_wrappers)
    return False


def find_wrapped_with(s, wrappers):
    return wrap(find_wrapped(s, wrappers), wrappers)


def find_wrapped(s, wrappers):
    if (len(wrappers) == 1):  # ""
        return c(s, wrappers, wrappers)
    elif (len(wrappers) == 2):  # ()
        return c_2(s, wrappers[0], wrappers[1])
    else:  # and()
        return c_2(s, sf(wrappers, -1), sl(wrappers, 1))
    return None


def find_wrapped_list(s, wrappers):
    wrapped_list = []
    while (has_wrapped(s, wrappers)):
        wrapped = find_wrapped(s, wrappers)
        s = rm_wrapped(s, wrappers)
        wrapped_list.append(wrapped)
    return wrapped_list


def rm_wrapped_all(s, wrappers):
    while (has_wrapped(s, wrappers)):
        s = rm_wrapped(s, wrappers)
    return s


def rm_wrapped(s, wrappers, no_space=False):
    wrapped = find_wrapped(s, wrappers)
    if (wrapped):
        wrapped_with_wrappers = wrap(wrapped, wrappers)
        if (no_space):
            s = cv(s, wrapped_with_wrappers, "")
        else:
            s = cv(s, " " + wrapped_with_wrappers, "")
    return s


def is_single_line(s):
    return not ct(s, "\n")


def is_empty_line(s):
    return trim(s) == ""


def not_empty_line(s):
    return not is_empty_line(s)


def cv_line_sep(s, indent_size=0):
    return cv(s, "$$LINE_SEP$$", "\n" + get_repeat_string(" ", indent_size))


def conn(l, sep="\n"):
    if (isinstance(l, list)):
        r = ""
        for s in l:
            r = r + s + sep
        if (r == sep):
            r = ""
        else:
            r = cl(r, sep)
        return r
    else:
        return conns(l, sep)


def conns(s, sep="\n"):  # connect as one string
    if (isinstance(s, list)):
        return conn(s, sep)
    else:
        return cv(s, "\n", sep)


def to_upper_case(s):
    return s.upper()


def to_lower_case(s):
    return s


def to_camel_case(s):
    return s[0].upper() + s[1:len(s)]


def to_lower_case_real(s):
    return s.lower()


def to_camel_words(s):
    words = sp(s, " ")
    words = cv_(words, to_camel_case)
    return conn(words, " ")


def lower(s):
    return to_lower_case_real(s)


def upper(s):
    return to_upper_case(s)


def camel(s):
    return to_camel_words(s)


def as_str(s):
    if (s == None):
        return ""
    return s


def to_int(s):
    if (is_number(s)):
        return int(s)
    return s


def encode_for_replace(s):
    s = cv(s, "\\n", "\n")
    s = cv(s, "\\t", "\t")
    return s


def encode_for_replace_back(s):
    s = cv(s, "\n", "\\n")
    s = cv(s, "\t", "\\t")
    return s


def encode_for_format(s):
    s = cv(s, "\\{", "_LB_")
    s = cv(s, "\\}", "_RB_")
    return s


def encode_for_format_back(s):
    s = cv(s, "_LB_", "{")
    s = cv(s, "_RB_", "}")
    return s


def format_str(s, *args):
    s = encode_for_format(s)
    s = s.format(*args)
    s = encode_for_format_back(s)
    return s


def format_s(s, length):  # format string to given length, append ' ' for completion
    string_len = get_length(s)
    return s + get_repeat_string(" ", length - string_len)


def format_f(f):
    return "{:0,.2f}".format(f)


def format_json_or_xml(s):
    return _r_("ulog_format.format_json_or_xml", s)


def format_json(s):
    return _r_("ulog_format.format_json", s)


def format_xml(s):
    return _r_("ulog_format.format_xml", s)


def get_length(s):
    length = 0
    for ch in s:
        if (is_chinese_char(ch)):
            length += 2
        else:
            length += 1
    return length


def do_line_op(line, line_op_func, args=None):
    argcount = line_op_func.__code__.co_argcount
    if (args == None):
        line = line_op_func(line)
    elif (argcount > 2 or line_op_func in [no_dup]):
        line = line_op_func(line, *get_parts(args))
    else:
        line = line_op_func(line, to_int(args))
    return line


def do_lines_op(s, line_op_func, args=None):
    lines = s.split("\n")
    return_lines = []
    for line in lines:
        r = do_line_op(line, line_op_func, args)
        if (isinstance(r, bool)):
            if (bool(r)):
                return_lines.append(line)
        else:
            if (isinstance(r, list)):
                return_lines += r
            else:
                return_lines.append(r)
    return conn(return_lines, "\n")


def noel(s):  # no empty line
    if (isinstance(s, list)):
        return sp(noel(conn(s)))
    return do_lines_op(s, not_empty_line)


def no_multi_el(s):  # no multiple empty line
    is_list = False
    if (isinstance(s, list)):
        s = conn(s)
        is_list = True
    s = no_spaces(s, "\n")
    s = no_dup(s, 2, "\n")
    if (is_list):
        s = sp(s)
    return s


def nomel(s):
    return no_multi_el(s)


def no_dup(s, n=1, *k):  # no dup specified sub strings in given string
    n = int(n)
    for k_ in k:
        _k__ = get_repeat_string(k_, n + 1)
        _k_ = get_repeat_string(k_, n)
        while (ct(s, _k__)):
            s = cv(s, _k__, _k_)
    return s


def no_spaces(s, *k):
    for k_ in k:
        while (ct(s, k_ + " ")):
            s = cv(s, k_ + " ", k_)
    return s


def no_multi_spaces(s, *k):
    for k_ in k:
        while (ct(s, k_ + "  ")):
            s = cv(s, k_ + "  ", k_ + " ")
    return s


def rmdup(s):  # no duplicate lines
    r = []
    is_list = False
    if (isinstance(s, list)):
        lines = s
        is_list = True
    else:
        lines = sp(s)
    for line in lines:
        if (not r.__contains__(line)):
            r += [line]
    if (is_list):
        return r
    else:
        return conn(r)


def shrinkel(s):  # no empty lines
    return noel(s)


def tol(s, n=0):  # to one line
    if (n == 0):
        return cv(s, "\n", "")
    else:
        lines = sp(s)
        return_lines = []
        for i in range(0, len(lines), n):
            sub_lines = lines[i: i + n]
            return_lines += [conn(sub_lines, "")]
        return conn(return_lines)


def sort(s, by_column=None, reverse=False, sort_key_func=None):  # sort
    is_list = False
    if (not isinstance(s, list)):
        lines = sp(s)
    else:
        lines = s
        is_list = True
    if (not by_column == None):
        lines.sort(key=lambda x: sp(x, " ", no_el=True)[int(by_column) - 1], reverse=to_bool(reverse))
    elif (not sort_key_func == None):
        lines.sort(key=lambda x: sort_key_func(x), reverse=to_bool(reverse))
    else:
        lines.sort(reverse=to_bool(reverse))
    if (is_list):
        return lines
    else:
        return conn(lines)


def to_bool(s):
    if (s == "y"):
        return True
    elif (s == "n"):
        return False
    else:
        return bool(s)


def sortreverse(s, by_column=None):
    return sort(s, by_column=by_column, reverse=True)


def dup(s, args):  # dup
    lines = sp(s)
    r = []
    r += lines
    indent = get_left_indent(lines[0])
    need_empty_line = (lines[len(lines) - 1] == indent + "}")
    from_to_s_list = get_parts(args, format_line="", keys=["(;;)", ";;", ";"])
    to_lines_map = dict()
    dup_count = 0
    for from_to_s in from_to_s_list:  # a a1 a2 a3;b b1 b2 b3
        camel = has_p(from_to_s, ".")
        if (camel):
            from_to_s = rm_p(from_to_s, ".")
        ks = sp(from_to_s, " ")  # a, a1, a2, a3
        from_s = ks[0]
        dup_count = len(ks) - 1
        for i in range(dup_count):
            to_s = ks[i + 1]
            if (not to_lines_map.__contains__(i + 1)):
                to_lines = []
                to_lines += lines
            else:
                to_lines = to_lines_map[i + 1]
            to_lines_new = []
            for line in to_lines:
                if (camel):
                    to_lines_new += [cvic(line, from_s, to_s)]
                else:
                    to_lines_new += [cv(line, from_s, to_s)]
            to_lines_map[i + 1] = to_lines_new
    for i in range(dup_count):
        if (need_empty_line):
            r += [""]
        r += to_lines_map[i + 1]
    return conn(r)


def nl(s, nl_line):  # new line
    if (ct(nl_line, "{")):
        return nl_line.format(*get_parts(s, nl_line))
    else:
        return cv(nl_line, "LINE", s)


def use(s, n):  # @UnusedVariable
    return n


def has_p(s, p):
    if (s != None):
        s = " " + trim(s) + " "
        return ct(s, " " + trim(p) + " ")
    return False


def rm_p(s, p):
    indent_left = get_left_indent(s);
    indent_right = get_right_indent(s);
    s = " " + trim(s) + " ";
    s = cv(s, " " + trim(p) + " ", " ");
    s = trim(s);
    s = indent_left + s + indent_right;
    return s


def is_linux():
    return _r_("fileio.exists__", "/root")


def is_windows():
    return not is_linux()


def to_linux_path(s):
    return cv(s, "\\", "/")


def to_windows_path(s):
    return cv(s, "/", "\\")


def rp_(p):
    if (is_linux()):
        return to_linux_path(p)
    else:
        return to_windows_path(p)


def bat_(n):
    return rp_(cons.bat_dir + sep(cons.bat_dir) + n + ".bat")


def cwd_(n):
    return rp_(cons.cwd_dir + sep(cons.cwd_dir) + n)


def alogs_(n):
    return rp_(cons.alogs_dir + sep(cons.alogs_dir) + n)


def format_paragraph(s):
    if (ct(s, dou_hao)):  # chinese
        for k in [ju_hao, wen_hao, "]"]:
            s = cv(s, k, k + "\n")
        for k in [fen_hao, dou_hao, mao_hao]:
            s = cv(s, k, k + "\n\t")
        for k in [liang_ge_kong_ge]:
            s = cv(s, k, "")
        for k in [dun_hao]:
            lines = sp(s)
            for line in lines:
                line00 = line
                tab_n = n(line, "\t")
                if (len(line) > 40):
                    line = cv(line, k, k + "\n" + get_repeat_string("\t", tab_n + 1))
                    s = cv(s, line00, line)
        s = no_dup(s, 2, "\n")
    else:  # english
        s = no_multi_el(s)
        s = no_multi_spaces(s, ".", ",", "?", "!")
        s = no_dot(s)
        for k in [".", "?", "!"]:
            s = cv(s, k + " ", k + "\n\n")
        for k in [",", ";"]:
            s = cv(s, k + " ", k + "\n\t")
        s = cv(s, " (", " \n\t(")
        s = cv(s, ") ", ") \n\t")
        connectors = [
            "which", "what", "why",     "when",   "whether",
            "where", "that", "if",      "unless", "for",
            "then",  "or",   "because", "and",    "but",
            "in",
        ]
        for k in connectors:
            s = cv(s, " " + k + " ", " \n\t" + k + " ")
        s = cv(s, " \n", "\n")
        s = dot_back(s)
        s = no_dup(s, 2, "\n")
    return s


def no_dot(s):
    for k in [".g."]:
        k2 = cv(k, ".", "_dot_")
        s = cv(s, k, k2)
    for i in range(10):
        k = str(i + 1) + "."
        k2 = cv(k, ".", "_dot_")
        s = cv(s, k, k2)
    return s


def dot_back(s):
    s = cv(s, "_dot_", ".")
    return s


def countn(s):
    return str(len(sp(s)))


def rnlog(s):
    if (ct(s, ".log")):
        s = cv(s, ".log", "")
        s = al(s, ".log")
    return s


def swc(s, n):  # select with confirm
    return _r_("ulist.select", n, sp(s))


def _r_(n, *args):  # reflection, n = module.func
    func = _func_(n)
    return func(*args)


def _func_(n):
    module = lf(n, ".")
    name = clf(n, ".")
    m = __import__(module, fromlist=True)
    func = getattr(m, name)
    return func


def is_http(s):
    return st(s, "http://", "https://")


def md5(s):
    import hashlib
    return hashlib.md5(s.encode()).hexdigest()


def duiqi(s, k=":"):
    is_str = False
    if (isinstance(s, str)):
        lines = sp(s)
        is_str = True
    else:
        lines = s
    a = cv_(lines, lf, k)
    a = cv_(a, trimright)
    a_len = max_len(a)
    msg = "{0:" + str(a_len) + "} {1} {2}"
    lines = cv_(lines, duiqi_encode, k)
    lines = cv_(lines, lambda x:msg.format(trimright(lf(x, k)), k, trimleft(clf(x, k))))
    lines = cv_(lines, duiqi_encode_back, k)
    if (is_str):
        s = conn(lines)
    else:
        s = lines
    return s


def duiqi_encode(s, k):
    if (k == ":"):
        s = cv(s, "b:", "b;")
    return s


def duiqi_encode_back(s, k):
    if (k == ":"):
        s = cv(s, "b;", "b:")
    return s


def duiqi2(s, k=","):
    is_str = False
    if (isinstance(s, str)):
        lines = sp(s)
        is_str = True
    indent = get_indent(s)
    lines = cv_(lines, trimright)
    lines = cv_(lines, cl, k)
    a = cv_(lines, lambda x: sp(x, k))  # [][]
    a = cv_(a, lambda x: cv_(x, lambda y: trim(y) + k))  # [][]
    a_len = []
    for i in range(len(a[0])):
        column = []
        for j in range(len(a)):
            try:
                item = a[j][i]
            except:
                item = ""
            column += [item]
        if (k == " "):
            column_len = max_len(column)
        else:
            column_len = max_len(column) + 1
        a_len += [column_len]
    msg = ""
    for i in range(len(a_len) - 1):
        msg += "{" + str(i) + ":" + str(a_len[i]) + "}"
    msg += "{" + str(len(a_len) - 1) + "}"

    def fmt_func(x):
        x = sp(x, k)
        x = cv_(x, trim)
        x = cv_(x, al, k)
        while (True):
            try:
                r = msg.format(*x)
                break
            except:
                x += [""]
        return r

    lines = cv_(lines, fmt_func)
    lines = cv_(lines, trimright)
    lines = cv_(lines, af, indent)
    if (is_str):
        s = conn(lines)
    else:
        s = lines
    return s


def is_find_command(m):
    return st(m, "f ", "q ", "fs ", "filelistfind f ", "filelistfind q ", "filelistfind fs ")


def is_message_code(m):
    if (ct(m, "=")):
        a = lf(m, "=")
        return n(a, ".") == 1 and nct(m, " ", ":", "/")
    return False


def is_locale_code(m):
    if (ct(m, "MessageCode.")):
        return True
    return False


def get_input_p():
    return cons.file_system.get_input_p()


def get_input_p__():
    return cons.p


def input_async(m):
    if (cons.input_result__ == None):
        input_result__ = input_result()

        def input_t(m, ir):
            ir.input_r = input(m)

        import threading
        t = threading.Thread(target=input_t, args=(m, input_result__))
        t.start()
        cons.input_result__ = input_result__
    else:
        print(m)
    while True:
        if (not cons.input_result__.input_r == None):
            r_cmd = cons.input_result__.input_r
            cons.input_result__ = None
            return r_cmd
        elif (is_quit_all()):
            return "q"
        elif (is_run_all()):
            ra_cmd = get_run_all_cmd()
            print(ra_cmd)
            return ra_cmd
        else:
            sleep(1)


def is_quit_all():
    return _r_("fileio.is_quit_all")


def is_run_all():
    return _r_("fileio.is_run_all")


def get_run_all_cmd():
    return _r_("fileio.get_run_all_cmd")


def sleep(ms):
    import time
    time.sleep(float(ms) / 1000)


class input_result:
    input_r = None


def is_linux_path(f):
    if (st(f, "[") and ct(f, "]")):
        f = clf(f, "]")
    return st(f, "/") or f == "/"


def is_windows_path(f):
    return not is_linux_path(f)


def sep(f=None):
    if (f):
        if (f == "/"):
            return ""
        elif (is_linux_path(f)):
            return "/"
        else:
            if (len(f) == 3 and f[1] == ":"):
                return ""
            else:
                return "\\"
    else:
        return cons.sep


def format_sep(f):
    f = cv(f, "/", cons.sep)
    f = cv(f, "\\", cons.sep)
    return f


def no_space_cmds(m, *ks):
    for k in ks:
        if (st(m, k) and nct(m, " ")):
            m = k + " " + cf(m, k)
    return m


def resolve_repeat_ids(m):
    '''
    + cv1..1 cv1..2 1..10
    '''
    if (ct(m, "..")):
        for i in range(100, 0, -1):
            h = str(i) + ".."
            if (ct(m, h)):
                r = []
                last = rt(m, " ")
                from_ = i
                to_ = int(cf(last, h))
                m = cl(m, " " + last)
                for j in range(from_, to_ + 1, 1):
                    r += [cv(m, h, str(j))]
                return r
    return m


def in_(s, p):
    if (_r_("tar.is_file_key", p)):
        p = _r_("tar.rp", p)
        lines = _r_("fileio.lwc", p)
        return s in lines
    return False


def get_package(f):
    for k in ["com", "org"]:
        if (ct(f, "\\" + k + "\\")):
            f = k + "\\" + clf(f, "\\" + k + "\\")
            f = crt(f, ".")
            f = cv(f, "\\", ".")
            break
    return f

