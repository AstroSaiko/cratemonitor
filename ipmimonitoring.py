#!/usr/bin/env python 

import subprocess
import sys
import os
import signal
import time

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
        return -1 
    proc = subprocess.Popen(("ipmitool -H mch-e1a04-18 -U '' -P '' -T 0x82 -b 7 -B 0 -t {0} sdr".format(PM)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    (data, err) = proc.communicate()
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
        return -1
    proc = subprocess.Popen(("ipmitool -H mch-e1a04-18 -U '' -P '' -T 0x82 -b 7 -B 0 -t {0} sdr".format(CU)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    (data, err) = proc.communicate()
    if err != '':
        print err
        return -1
    data = data.split('\n')
    return data

if __name__ == "__main__":

    #For PMs
    PMTempA = []
    PMTempB = []
    PMTempBase = []
    PMVINs = []
    PMVOutsA = []
    PMVOutsB = []
    PM12Vs = []
    PM3V3s = []
    PMCurrents = []

    PMVoltages = []
    PMTemperatures = []

    for i in [1]:
        tempA = None
        tempB = None
        tempBase = None
        VIN = None
        VOutA = None
        VOutB = None
        current = None
        volt12 = None
        volt3V3 = None

        data = getPMData(i)
        if data == -1:
            print "Error or whatever"
        else:
            for item in data:
                #Temperatures
                if "TBrick-A" in item:
                    print item.strip().split(" ")[10]
                    tempA = item.strip().split(" ")[10]
                elif "TBrick-B" in item:
                    print item.strip().split(" ")[10]                                                                                                                                                                                      
                    tempB = item.strip().split(" ")[10]
                elif "T-Base" in item:
                    print item.strip().split(" ")[12]
                    tempBase = item.strip().split(" ")[12]
                #Input Voltage
                elif "VIN" in item:
                    #print item.strip().split(" ")[15]
                    VIN = item.strip().split(" ")[15]
                #Output Voltage
                elif "VOUT-A" in item:                                                                                                                                   
                    VOutA = item.strip().split(" ")[12]
                    #print VOutA
                elif "VOUT-B" in item:                                                                                                            
                    VOutB = item.strip().split(" ")[12]
                    #print VOutB
                #12V
                elif "12V" in item:
                    volt12 = item.strip().split(" ")[15]
                    #print volt12
                #3.3V
                elif "3.3V" in item:
                    volt3V3 = item.strip().split(" ")[14]
                    #print volt3V3
                #Total utput current
                elif "Current(SUM)" in item:
                    current = item.strip().split(" ")[6]
                    #print current
                #print tempA
                #print tempB
        print tempBase
                #PMTemperatures.append(tempA)
                #PMTemperatures.append(tempB)
                #PMTemperatures.append(tempBase)
                #PMVoltages.append(VIN)
             #PMVoltages.append(VOutA)
                #PMVoltages.append(VOutB)
                #PMVoltages.append(volt12)
                #PMVoltages.append(volt3V3)
