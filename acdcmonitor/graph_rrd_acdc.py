#!/usr/bin/env python

import os
import socket
import sys

import pdb
import rrdtool

if __name__ == "__main__":

    filepath = '/home/xtaldaq/cratemonitor_v3/acdcmonitor/'
    hostname = 'acdc-s1g04-27'
    
    for sched in ['daily' , 'weekly', 'monthly']:
        if sched == 'weekly':
            period = 'w'
        elif sched == 'daily':
            period = 'd'
        elif sched == 'monthly':
            period = 'm'
        ret = rrdtool.graph( "{0}{1}-{2}-temperature.png".format(filepath,hostname,period),
                             "--start", "-1{0}".format(period),
                             "--vertical-label=Rectifier Temperature (degC)",
                             "-w 400", "-h 240",
                             #"--slope-mode",                                                                                                                                                                        
                             "-t {0}".format(str.upper(hostname)),
                             "DEF:t1={0}{1}.rrd:temperature1:AVERAGE".format(filepath, hostname),
                             "DEF:t2={0}{1}.rrd:temperature2:AVERAGE".format(filepath, hostname),
                             "DEF:t3={0}{1}.rrd:temperature3:AVERAGE".format(filepath, hostname),
                             "DEF:t4={0}{1}.rrd:temperature4:AVERAGE".format(filepath, hostname),
                             "LINE:t1#000000:Module 1",
                             "LINE:t2#FF0000:Module 2",
                             "LINE:t3#FF6600:Module 3",
                             "LINE:t4#FFFF00:Module 4")

        ret = rrdtool.graph( "{0}{1}-{2}-outVolt.png".format(filepath,hostname,period),
                             "--start", "-1{0}".format(period),
                             "--vertical-label=Rectifier Output Voltage (V)",
                             "-w 400", "-h 240",
                             #"--slope-mode",
                             "-t {0}".format(str.upper(hostname)),
                             "DEF:t1={0}{1}.rrd:outputVoltage1:AVERAGE".format(filepath, hostname),
                             "DEF:t2={0}{1}.rrd:outputVoltage2:AVERAGE".format(filepath, hostname),
                             "DEF:t3={0}{1}.rrd:outputVoltage3:AVERAGE".format(filepath, hostname),
                             "DEF:t4={0}{1}.rrd:outputVoltage4:AVERAGE".format(filepath, hostname),
                             "LINE:t1#000000:Module 1",
                             "LINE:t2#FF0000:Module 2",
                             "LINE:t3#FF6600:Module 3",
                             "LINE:t4#FFFF00:Module 4")

        ret = rrdtool.graph( "{0}{1}-{2}-inVolt.png".format(filepath,hostname,period),
                             "--start", "-1{0}".format(period),
                             "--vertical-label=Rectifier Input Voltage (V)",
                             "-w 400", "-h 240",
                             #"--slope-mode",
                             "-t {0}".format(str.upper(hostname)),
                             "DEF:t1={0}{1}.rrd:inputVoltage1:AVERAGE".format(filepath, hostname),
                             "DEF:t2={0}{1}.rrd:inputVoltage2:AVERAGE".format(filepath, hostname),
                             "DEF:t3={0}{1}.rrd:inputVoltage3:AVERAGE".format(filepath, hostname),
                             "DEF:t4={0}{1}.rrd:inputVoltage4:AVERAGE".format(filepath, hostname),
                             "LINE:t1#000000:Module 1",
                             "LINE:t2#FF0000:Module 2",
                             "LINE:t3#FF6600:Module 3",
                             "LINE:t4#FFFF00:Module 4")

        ret = rrdtool.graph( "{0}{1}-{2}-outCurr.png".format(filepath,hostname,period),
                             "--start", "-1{0}".format(period),
                             "--vertical-label=Rectifier Output Current (A)",
                             "-w 400", "-h 240",
                             #"--slope-mode",                                                                        
                             "-t {0}".format(str.upper(hostname)),
                             "DEF:t1={0}{1}.rrd:outputCurrent1:AVERAGE".format(filepath, hostname),
                             "DEF:t2={0}{1}.rrd:outputCurrent2:AVERAGE".format(filepath, hostname),
                             "DEF:t3={0}{1}.rrd:outputCurrent3:AVERAGE".format(filepath, hostname),
                             "DEF:t4={0}{1}.rrd:outputCurrent4:AVERAGE".format(filepath, hostname),
                             "LINE:t1#000000:Module 1",
                             "LINE:t2#FF0000:Module 2",
                             "LINE:t3#FF6600:Module 3",
                             "LINE:t4#FFFF00:Module 4")

        ret = rrdtool.graph( "{0}{1}-{2}-phaseVolt.png".format(filepath,hostname,period),
                             "--start", "-1{0}".format(period),
                             "--vertical-label=AC Phase Voltage (V)",
                             "-w 400", "-h 240",
                             #"--slope-mode", 
                             "-t {0}".format(str.upper(hostname)),
                             "DEF:t1={0}{1}.rrd:acPhase1Voltage:AVERAGE".format(filepath, hostname),
                             "DEF:t2={0}{1}.rrd:acPhase2Voltage:AVERAGE".format(filepath, hostname),
                             "DEF:t3={0}{1}.rrd:acPhase3Voltage:AVERAGE".format(filepath, hostname),
                             "LINE:t1#000000:Phase 1",
                             "LINE:t2#FF0000:Phase 2",
                             "LINE:t3#FF6600:Phase 3")
