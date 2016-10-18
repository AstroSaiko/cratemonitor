#!/usr/bin/env python

import os
import socket
import sys

import pdb
import rrdtool

if __name__ == "__main__":
    #for rack in 's1g04': #'s1g01' 's1g03' 's1g04':
    rack = 's1g04'
    ret = rrdtool.create('/home/xtaldaq/cratemonitor_v3/acdcmonitor/acdc-{0}-27.rrd'.format(rack),
                         "-s 60",
                         "DS:temperature1:GAUGE:120:U:U",
                         "DS:temperature2:GAUGE:120:U:U",
                         "DS:temperature3:GAUGE:120:U:U",
                         "DS:temperature4:GAUGE:120:U:U",
                         "DS:outputVoltage1:GAUGE:120:U:U",
                         "DS:outputVoltage2:GAUGE:120:U:U",
                         "DS:outputVoltage3:GAUGE:120:U:U",
                         "DS:outputVoltage4:GAUGE:120:U:U",
                         "DS:inputVoltage1:GAUGE:120:U:U",
                         "DS:inputVoltage2:GAUGE:120:U:U",
                         "DS:inputVoltage3:GAUGE:120:U:U",
                         "DS:inputVoltage4:GAUGE:120:U:U",
                         "DS:outputCurrent1:GAUGE:120:U:U",
                         "DS:outputCurrent2:GAUGE:120:U:U",
                         "DS:outputCurrent3:GAUGE:120:U:U",
                         "DS:outputCurrent4:GAUGE:120:U:U",
                         "DS:acPhase1Voltage:GAUGE:120:U:U",
                         "DS:acPhase2Voltage:GAUGE:120:U:U",
                         "DS:acPhase3Voltage:GAUGE:120:U:U",
                         "RRA:AVERAGE:0.5:1:1440",
                         "RRA:AVERAGE:0.5:30:720",
                         "RRA:AVERAGE:0.5:120:780",
                         "RRA:AVERAGE:0.5:1440:800",
                         #"RRA:MAX:0.5:1:1440",                                                                                                                                                                                     
                         "RRA:MAX:0.5:30:720",
                         "RRA:MAX:0.5:120:780",
                         "RRA:MAX:0.5:1440:800",
                         #"RRA:MIN:0.5:1:1440",                                                                                                                                                                                     
                         "RRA:MIN:0.5:30:720",
                         "RRA:MIN:0.5:120:780",
                         "RRA:MIN:0.5:1440:800")
    print ret
