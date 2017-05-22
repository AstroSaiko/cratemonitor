#!/usr/bin/env python

import netsnmp
import os
import sys
from rrdtool import update as rrd_update

os.environ['MIBS'] = 'ACX-MIB:SNMPv2-SMI' # To add the acdc controller's MIB to snmp's path

hostname = sys.argv[1] # Call the script with a hostname

temp = [None] * 4 
outVolt = [None] * 4
inVolt = [None] * 4
outCurr = [None] * 4

for module in [0, 1, 2, 3]: # There are 4 rectifier modules
    temp[module] = netsnmp.Varbind("temperature.{0}".format(module))
    outVolt[module] = netsnmp.Varbind("outputVoltage.{0}".format(module)) # V*10
    inVolt[module] = netsnmp.Varbind("inputVoltage.{0}".format(module))
    outCurr[module] = netsnmp.Varbind("outputCurrent.{0}".format(module)) # A*10

ph1Volt = netsnmp.Varbind("acPhase1Voltage.0")
ph2Volt = netsnmp.Varbind("acPhase2Voltage.0")
ph3Volt = netsnmp.Varbind("acPhase3Voltage.0")

data = netsnmp.snmpget(temp[0], temp[1], temp[2], temp[3], \
                outVolt[0], outVolt[1], outVolt[2], outVolt[3], \
                inVolt[0], inVolt[1], inVolt[2], inVolt[3], \
                outCurr[0], outCurr[1], outCurr[2], outCurr[3], \
                ph1Volt, ph2Volt, ph3Volt, \
                Version = 2, \
                DestHost = hostname, \
                Community = 'accread')

outVoltAdjusted = [float(data[4])/10, float(data[5])/10, float(data[6])/10, float(data[7])/10]
outCurrAdjusted = [float(data[12])/10, float(data[13])/10, float(data[14])/10, float(data[15])/10]
                
ret = rrd_update('/home/xtaldaq/cratemonitor_v3/acdcmonitor/{0}.rrd'.format(hostname), \
                     'N:{0[0]}:{0[1]}:{0[2]}:{0[3]}:{1[0]}:{1[1]}:{1[2]}:{1[3]}:{0[8]}:{0[9]}:{0[10]}:{0[11]}:{2[0]}:{2[1]}:{2[2]}:{2[3]}:{0[16]}:{0[17]}:{0[18]}'.format(data, outVoltAdjusted, outCurrAdjusted))
