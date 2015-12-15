#!/bin/bash
# This script will fill the psu rrd 

NETTXBYTES=`cat /sys/class/net/eth1/statistics/tx_bytes`
echo $NETTXBYTES

NETRXBYTES=`cat /sys/class/net/eth1/statistics/rx_bytes`
#echo $NETRXBYTES

NETTXERRORS=`cat /sys/class/net/eth1/statistics/tx_errors`
#echo $NETTXERRORS

NETRXERRORS=`cat /sys/class/net/eth1/statistics/rx_errors`
#echo $NETRXERRORS

rrdtool update /home/xtaldaq/monitoring/pixp1_chub_nic.rrd N:$NETTXBYTES:$NETRXBYTES:$NETTXERRORS:$NETRXERRORS
