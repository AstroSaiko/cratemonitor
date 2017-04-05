#!/usr/bin/env python 

import subprocess
import sys
import os
import signal
import time


line = []

def getPMData(slot):
    if slot == 1:
        PM = "0xc2"
    elif slot == 2:
        PM = "0xc4"
    elif slot == 3:
        PM = "0xc6"
    elif slot == 4:
        PM = "0xc8"
    else:
        print "Please insert a valid slot (1-4)"
        sys.exit() #Get standard exit codes here?
    proc = subprocess.Popen(("ipmitool -H mch-e1a04-18 -P '' -T 0x82 -b 7 -B 0 -t {0} sdr".format(PM)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    (data, err) = proc.communicate()
    #print out
    if err != '':
        print err
        return -1
    data = data.split('\n')
    return data

def getCUData(CU_index):
    if CU_index == 1:
        CU = "0xa8"
    elif CU_index == 2:
        CU = "0xaa"
    else:
        print "Please insert a valid index (1 or 2)"
        sys.exit()
    proc = subprocess.Popen(("ipmitool -H mch-e1a04-18 -P '' -T 0x82 -b 7 -B 0 -t {0} sdr".format(CU)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    (data, err) = proc.communicate()
    #print out                                                                                                                                                                                                                               
    if err != '':
        print err
        return -1
    data = data.split('\n')
    return data

if __name__ == "__main__":
    for i in [1,2,3,4]:
        data = getCUData(i)
        print data

