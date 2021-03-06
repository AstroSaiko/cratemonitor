#!/bin/bash
# This script will fill the psu rrd 

NETTXBYTES=`cat /sys/class/net/rename5/statistics/tx_bytes`
echo 'Tx Bytes ' $NETTXBYTES

NETRXBYTES=`cat /sys/class/net/rename5/statistics/rx_bytes`
echo 'Rx Bytes ' $NETRXBYTES

NETTXERRORS=`cat /sys/class/net/rename5/statistics/tx_errors`
echo 'Tx Errors ' $NETTXERRORS

NETRXERRORS=`cat /sys/class/net/rename5/statistics/rx_errors`
echo 'Rx Errors ' $NETRXERRORS

rrdtool update /home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd N:$NETTXBYTES:$NETRXBYTES:$NETTXERRORS:$NETRXERRORS
