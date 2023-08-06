import ustring         as s
from   ulog            import log

import cons            as cons
import ulog            as ulog
import fileio          as fileio

udp_sites = {
    "3127": {
        "ip"   : "10.111.3.127",
        "port" : 10514,
    },
    "local": {
        "ip"   : "localhost",
        "port" : 10514,
    },
}

udp_default = "local"


def translate(m):
    m00 = m
    m = tr_udp(m)
    ulog.log_trans(m00, m)
    return m


def tr_udp(m):
    if (m == "udp"):
        do_udp_send()
        m = cons.ignore_cmd
    elif (s.st(m, "udp ")):
        do_udp_send(key=s.cf(m, "udp "))
        m = cons.ignore_cmd
    return m


def do_udp_send(key=None):
    # host = input("input host>")
    # port = int(input("input port>"))
    if (key == None):
        key = udp_default
    host = udp_sites[key]["ip"]
    port = udp_sites[key]["port"]
    log()
    do_udp_send__(host, port)


def do_udp_send__(host, port):
    import traceback
    from subconsole import sub_console

    class udp_sub_console(sub_console):
        
        host = None
        port = None
        udp_socket = None
        
        def __init__(self, host, port):
            self.host = host
            self.port = port
            self.init__()
        
        def init__(self):
            import socket
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            log("creating udp sender: [{0}:{1}]".format(self.host, str(self.port)))
            log()
        
        def n(self):
            return "udp send"
        
        def callback(self, m):
            self.try_(self.main__, m)
        
        def clean_up(self):
            self.udp_socket.close()
        
        def main__(self, m):
            if (fileio.exists(m)):
                self.do_udp_send__file(m)
            else:
                self.do_udp_send__one(m)
            return m
        
        def do_udp_send__file(self, m):
            lines = fileio.l(m)
            for line in lines:
                if (not line == ""):
                    self.do_udp_send__one(line)
        
        def do_udp_send__one(self, m):
            self.udp_socket.sendto(m.encode('utf-8'), (host, port))
            log()
            log("udp send [{0}:{1}]: {2}".format(host, str(port), m))
            log()

    udp__ = udp_sub_console(host, port)
    udp__.run()
    
