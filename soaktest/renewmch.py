#!/usr/bin/env python

###############################################################################

import os
import socket
import sys

import pdb
import rrdtool

###############################################################################

if __name__ == "__main__":

#    for crate in ['s1e02-27','s1e02-18','s1e02-10','s1e03-36','s1e03-27','s1e03-18']:
    for rack in ['s1g01', 's1g03', 's1g04']:
        print rack
        for crate in ['18', '27', '36', '45']:

# 1,440 samples of 1 minute  (24 hours)
# 720 samples of 30 mins (24 hrs + 14 days = 15 days)
# 780 samples of 2 hours    (15 + 50 days = 65 days)
# 800 samples of 1 day      (65 days plus 2 yrs rounded to 800)
            print crate
        #for the MCH database 
            ret1 = rrdtool.create('/home/xtaldaq/cratemonitor_v3/rrd/mch-{0}-{1}.rrd'.format(rack, crate), 
                                  "-s 60",
                                  "DS:AMC1temp:GAUGE:120:U:U",
                                  "DS:AMC2temp:GAUGE:120:U:U",
                                  "DS:AMC3temp:GAUGE:120:U:U",
                                  "DS:AMC4temp:GAUGE:120:U:U",
                                  "DS:AMC5temp:GAUGE:120:U:U",
                                  "DS:AMC6temp:GAUGE:120:U:U",
                                  "DS:AMC7temp:GAUGE:120:U:U",
                                  "DS:AMC8temp:GAUGE:120:U:U",
                                  "DS:AMC9temp:GAUGE:120:U:U",
                                  "DS:AMC10temp:GAUGE:120:U:U",
                                  "DS:AMC11temp:GAUGE:120:U:U",
                                  "DS:AMC12temp:GAUGE:120:U:U",
                                  "DS:AMC13temp:GAUGE:120:U:U",
                                  "DS:CU1temp:GAUGE:120:U:U",
                                  "DS:CU2temp:GAUGE:120:U:U",
                                  "DS:PM1temp:GAUGE:120:U:U",
                                  "DS:PM2temp:GAUGE:120:U:U",
                                  "DS:AMC1curr1V0:GAUGE:120:U:U",
                                  "DS:AMC2curr1V0:GAUGE:120:U:U",
                                  "DS:AMC3curr1V0:GAUGE:120:U:U",
                                  "DS:AMC4curr1V0:GAUGE:120:U:U",
                                  "DS:AMC5curr1V0:GAUGE:120:U:U",
                                  "DS:AMC6curr1V0:GAUGE:120:U:U",
                                  "DS:AMC7curr1V0:GAUGE:120:U:U",
                                  "DS:AMC8curr1V0:GAUGE:120:U:U",
                                  "DS:AMC9curr1V0:GAUGE:120:U:U",
                                  "DS:AMC10curr1V0:GAUGE:120:U:U",
                                  "DS:AMC11curr1V0:GAUGE:120:U:U",
                                  "DS:AMC12curr1V0:GAUGE:120:U:U",
                                  "DS:AMC1curr12V0:GAUGE:120:U:U",
                                  "DS:AMC2curr12V0:GAUGE:120:U:U",
                                  "DS:AMC3curr12V0:GAUGE:120:U:U",
                                  "DS:AMC4curr12V0:GAUGE:120:U:U",
                                  "DS:AMC5curr12V0:GAUGE:120:U:U",
                                  "DS:AMC6curr12V0:GAUGE:120:U:U",
                                  "DS:AMC7curr12V0:GAUGE:120:U:U",
                                  "DS:AMC8curr12V0:GAUGE:120:U:U",
                                  "DS:AMC9curr12V0:GAUGE:120:U:U",
                                  "DS:AMC10curr12V0:GAUGE:120:U:U",
                                  "DS:AMC11curr12V0:GAUGE:120:U:U",
                                  "DS:AMC12curr12V0:GAUGE:120:U:U",
                                  "DS:PM1VoutA:GAUGE:120:U:U",
                                  "DS:PM2VoutA:GAUGE:120:U:U",
                                  "DS:PM1VoutB:GAUGE:120:U:U",
                                  "DS:PM2VoutB:GAUGE:120:U:U",
                                  "DS:PM1sumCurr:GAUGE:120:U:U",
                                  "DS:PM2sumCurr:GAUGE:120:U:U",
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
			
