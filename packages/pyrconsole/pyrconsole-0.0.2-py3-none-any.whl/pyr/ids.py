import ustring         as s
from   ulog            import log

import cons            as cons


def is_ids(m, *k):
    for i in k:
        if (do_is_ids(m, i)):
            return True
    return False


def do_is_ids(m, k):
    if (s.ct(m, k + " ")):  # handle args
        m = s.cl(s.lfw(m, k + " "), " ")
    return s.match(m, "\\d+" + k, "(\\d+ )+" + k)


def is_pure_ids(m):
    if (s.ct(m, " ")):
        return is_ids(m + " key", "key")
    else:
        return is_ids(m + "key", "key")


def to_ids_from_pure(m, k):  # m = "1 2 3", m = "123"
    if (is_pure_ids(m)):
        if (s.ct(m, " ")):
            return m + " " + k
        else:
            return m + k
    return m


def rm_ids(m, k):
    return s.clfw(m, k)


def get_ids(m, k):  # starting with 0
    if (s.ct(m, k + " ")):  # handle args
        m = s.cl(s.lfw(m, k + " "), " ")
    m = s.cl(m, k)
    select_ids = []
    if (not s.ct(m, " ")):
        for i in range(len(m)):
            idx = int(m[i]) - 1
            select_ids.append(idx)
    else:
        m = s.trim(m)
        ids = m.split(" ")
        for idStr in ids:
            idx = int(idStr) - 1
            select_ids.append(idx)
    return select_ids


def get_selected(a_list, m, *k_list):
    if (len(k_list) == 0):
        m = to_ids_from_pure(m, "key")
        k_list = ["key"]
    for k in k_list:
        if (is_ids(m, k)):
            select_ids = get_ids(m, k)
            selected = []
            for idx in select_ids:
                selected.append(a_list[idx])
            return selected
    return a_list


def get_pure_ids(m):
    return get_ids(m + " key", "key")

