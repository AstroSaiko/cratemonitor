#!/bin/bash
# This script will create the rrds needed to hold network monitoring data for TCDS controlhub


# For PowerOne testing
# rrdtool create psu-s1e01-20-01.rrd             \
#             --start 920804400          \
#             DS:speed:COUNTER:600:U:U   \
#             RRA:AVERAGE:0.5:1:24       \
#             RRA:AVERAGE:0.5:6:10
            
            
# 1,440 samples of 1 minute  (24 hours)
# 720 samples of 30 mins (24 hrs + 14 days = 15 days)
# 780 samples of 2 hours    (15 + 50 days = 65 days)
# 800 samples of 1 day      (65 days plus 2 yrs rounded to 800)

	rrdtool create --step=60 /home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd         \
             DS:NetTxBytes:COUNTER:120:U:U   \
             DS:NetRxBytes:COUNTER:120:U:U  \
             DS:NetTxErrors:COUNTER:120:U:U   \
             DS:NetRxErrors:COUNTER:120:U:U  \
             RRA:AVERAGE:0.5:1:1440      \
             RRA:AVERAGE:0.5:30:720      \
             RRA:AVERAGE:0.5:120:780     \
             RRA:AVERAGE:0.5:1440:800    \
             RRA:MAX:0.5:1:1440      \
             RRA:MAX:0.5:30:720      \
             RRA:MAX:0.5:120:780     \
             RRA:MAX:0.5:1440:800    \
             RRA:MIN:0.5:1:1440      \
             RRA:MIN:0.5:30:720      \
             RRA:MIN:0.5:120:780     \
             RRA:MIN:0.5:1440:800    
