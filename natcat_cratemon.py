#!/usr/bin/env python

###############################################################################

import os
import socket
import sys

import pdb
from rrdtool import update as rrd_update
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
    currents12 = []
    for fru in [5,6,7,8,9,10,11,12,13,14,15,16,30,40,41]:
        cmd = 'show_sensorinfo {0}\r\n'.format(fru)
        #print 'Querying FRU #{0}'.format(fru)
        data = natcat(mch_address, 23, cmd)
#        print data
        temperature = 'U'
        current = 'U'
	current12 = 'U'

        for item in data.split("\n"):
            if "FPGA Temp" in item:
#                print item.strip()
                temperature = item.strip().split(" ")[16]
            if "30   Full" in item:
#                print item.strip()
                current12 = item.strip().split(" ")[13]
            if "28   Full" in item:
#                print item.strip()
                current = item.strip().split(" ")[13]
# AMC 13
#            if "T2 Temp" in item:
#                print item.strip()
#                temperature = item.strip().split(" ")[16]
            if "5   Full     Temp    0x1e" in item:
#                print item.strip()
                temperature = item.strip().split(" ")[16]
        #print 'The Temperature is ' + temperature + ' C'
        #print 'The Current is ' + current + ' A'
	#print 'The 12V current is ' + current12 + 'A'
        temperatures.append(temperature)
        currents.append(current)
	currents12.append(current12)
    print temperatures
    print currents
    print currents12
    print "Done"

###############################################################################
ret = rrd_update('/home/xtaldaq/monitoring/{0}.rrd'.format(mch_address), 'N:{0[0]}:{0[1]}:{0[2]}:{0[3]}:{0[4]}:{0[5]}:{0[6]}:{0[7]}:{0[8]}:{0[9]}:{0[10]}:{0[11]}:{0[12]}:{0[13]}:{0[14]}:{1[0]}:{1[1]}:{1[2]}:{1[3]}:{1[4]}:{1[5]}:{1[6]}:{1[7]}:{1[8]}:{1[9]}:{1[10]}:{1[11]}:{2[0]}:{2[1]}:{2[2]}:{2[3]}:{2[4]}:{2[5]}:{2[6]}:{2[7]}:{2[8]}:{2[9]}:{2[10]}:{2[11]}'.format(temperatures,currents, currents12))
print "Done"
