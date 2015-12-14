#!/usr/bin/env python

###############################################################################

import os
import socket
import sys

import pdb

###############################################################################

def natcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try :
        s.connect((hostname, port))
    except :
        print 'Unable to connect'
        sys.exit()
    s.sendall(content)
    s.sendall("exit\r\n")
    # s.shutdown(socket.SHUT_WR)
    data = []
    while True:
        try :
            tmp = s.recv(1024)
        except :
            print 'receiving failed, MCH is probably busy'
            break
        if not len(tmp):
            break
        data.append(tmp)
    s.close()
    res = "".join(data)
    # End of natcat().
    return res

###############################################################################

if __name__ == "__main__":

    args = sys.argv
    if len(args) < 1:
        print >> sys.stderr, \
            "ERROR Expected one arguments: the MCH IP address"
        sys.exit(1)
    elif ("-h" in args) or ("--help" in args):
        print "Expecting two arguments: the MCH IP address"
        sys.exit(0)

    mch_address = args[1]

    temperatures = []
    currents = []
    for fru in [5,6,7,8,9,10,11,12,13,14,15,16,30,40,41]:
        cmd = 'show_sensorinfo {0}\r\n'.format(fru)
        print 'Querying FRU #{0}'.format(fru)
        data = natcat(mch_address, 23, cmd)
#        print data
        temperature = 'U'
        current = 'U'
        for item in data.split("\n"):
            if "FPGA Temp" in item:
#                print item.strip()
                temperature = item.strip().split(" ")[16]
            if "28   Full" in item:
#                print item.strip()
                current = item.strip().split(" ")[13]
            if "T2 Temp" in item:
#                print item.strip()
                temperature = item.strip().split(" ")[16]
            if "5   Full     Temp    0x1e" in item:
#                print item.strip()
                temperature = item.strip().split(" ")[16]
#        print 'The Temperature is ' + temperature + ' C'
#        print 'The Current is ' + current + ' A'
        temperatures.append(temperature)
        currents.append(current)
    print temperatures
    print currents
    print "Done"

###############################################################################
