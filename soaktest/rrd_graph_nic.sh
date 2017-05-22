#!/bin/bash
# This script will graph the psu rrd 

rrdtool graph -A -Y -r /home/xtaldaq/cratemonitor_v3/png/chub_nic_6mo.png --title "TCDS Controlhub NIC last 6 Months" --start -15778463 \
            DEF:rawTx=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:AVERAGE \
            DEF:rawTxMax=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:MAX \
            DEF:rawTxMin=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:MIN \
            DEF:rawRx=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:AVERAGE \
            DEF:rawRxMax=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:MAX \
            DEF:rawRxMin=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:MIN \
            "CDEF:scaledTx=rawTx,8,*" \
            "CDEF:scaledTxMax=rawTxMax,8,*" \
            "CDEF:scaledTxMin=rawTxMin,8,*" \
            "CDEF:scaledRx=rawRx,8,*" \
            "CDEF:scaledRxMax=rawRxMax,8,*" \
            "CDEF:scaledRxMin=rawRxMin,8,*" \
            LINE1:scaledTx#0000FF:"Tx Average (bps)" \
            LINE1:scaledTxMax#000055:"Tx Maximum (bps)" \
            LINE1:scaledTxMin#000088:"Tx Minimum (bps)" \
            LINE1:scaledRx#FF0000:"Rx Average (bps)" \
            LINE1:scaledRxMax#550000:"Rx Maximum (bps)" \
            LINE1:scaledRxMin#880000:"Rx Minimum (bps)" 

rrdtool graph -A -Y -r /home/xtaldaq/cratemonitor_v3/png/chub_nic_xtaldaqth.png --title "TCDS Controlhub NIC last Month" --start -2629743 \
            DEF:rawTx=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:AVERAGE \
            DEF:rawTxMax=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:MAX \
            DEF:rawTxMin=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:MIN \
            DEF:rawRx=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:AVERAGE \
            DEF:rawRxMax=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:MAX \
            DEF:rawRxMin=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:MIN \
            "CDEF:scaledTx=rawTx,8,*" \
            "CDEF:scaledTxMax=rawTxMax,8,*" \
            "CDEF:scaledTxMin=rawTxMin,8,*" \
            "CDEF:scaledRx=rawRx,8,*" \
            "CDEF:scaledRxMax=rawRxMax,8,*" \
            "CDEF:scaledRxMin=rawRxMin,8,*" \
            LINE1:scaledTx#0000FF:"Tx Average (bps)" \
            LINE1:scaledTxMax#000055:"Tx Maximum (bps)" \
            LINE1:scaledTxMin#000088:"Tx Minimum (bps)" \
            LINE1:scaledRx#FF0000:"Rx Average (bps)" \
            LINE1:scaledRxMax#550000:"Rx Maximum (bps)" \
            LINE1:scaledRxMin#880000:"Rx Minimum (bps)" 

rrdtool graph -A -Y -r /home/xtaldaq/cratemonitor_v3/png/chub_nic_week.png --title "TCDS Controlhub NIC One Week" --start -604800 \
            DEF:rawTx=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:AVERAGE \
            DEF:rawTxMax=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:MAX \
            DEF:rawTxMin=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:MIN \
            DEF:rawRx=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:AVERAGE \
            DEF:rawRxMax=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:MAX \
            DEF:rawRxMin=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:MIN \
            "CDEF:scaledTx=rawTx,8,*" \
            "CDEF:scaledTxMax=rawTxMax,8,*" \
            "CDEF:scaledTxMin=rawTxMin,8,*" \
            "CDEF:scaledRx=rawRx,8,*" \
            "CDEF:scaledRxMax=rawRxMax,8,*" \
            "CDEF:scaledRxMin=rawRxMin,8,*" \
            LINE1:scaledTx#0000FF:"Tx Average (bps)" \
            LINE1:scaledTxMax#000055:"Tx Maximum (bps)" \
            LINE1:scaledTxMin#000088:"Tx Minimum (bps)" \
            LINE1:scaledRx#FF0000:"Rx Average (bps)" \
            LINE1:scaledRxMax#550000:"Rx Maximum (bps)" \
            LINE1:scaledRxMin#880000:"Rx Minimum (bps)" 

rrdtool graph -A -Y -r /home/xtaldaq/cratemonitor_v3/png/chub_nic_day.png --title "TCDS Controlhub NIC last Day" --start -86400 \
            DEF:rawTx=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:AVERAGE \
            DEF:rawTxMax=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:MAX \
            DEF:rawTxMin=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:MIN \
            DEF:rawRx=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:AVERAGE \
            DEF:rawRxMax=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:MAX \
            DEF:rawRxMin=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:MIN \
            "CDEF:scaledTx=rawTx,8,*" \
            "CDEF:scaledTxMax=rawTxMax,8,*" \
            "CDEF:scaledTxMin=rawTxMin,8,*" \
            "CDEF:scaledRx=rawRx,8,*" \
            "CDEF:scaledRxMax=rawRxMax,8,*" \
            "CDEF:scaledRxMin=rawRxMin,8,*" \
            LINE1:scaledTx#0000FF:"Tx Average (bps)" \
            LINE1:scaledTxMax#000055:"Tx Maximum (bps)" \
            LINE1:scaledTxMin#000088:"Tx Minimum (bps)" \
            LINE1:scaledRx#FF0000:"Rx Average (bps)" \
            LINE1:scaledRxMax#550000:"Rx Maximum (bps)" \
            LINE1:scaledRxMin#880000:"Rx Minimum (bps)" 

rrdtool graph -A -Y /home/xtaldaq/cratemonitor_v3/png/chub_nic_hour.png --title "TCDS Controlhub NIC last Hour" --start -3600 \
            DEF:rawTx=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:AVERAGE \
            DEF:rawTxMax=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:MAX \
            DEF:rawTxMin=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetTxBytes:MIN \
            DEF:rawRx=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:AVERAGE \
            DEF:rawRxMax=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:MAX \
            DEF:rawRxMin=/home/xtaldaq/cratemonitor_v3/rrd/cmsfpixch001_nic.rrd:NetRxBytes:MIN \
            "CDEF:scaledTx=rawTx,8,*" \
            "CDEF:scaledTxMax=rawTxMax,8,*" \
            "CDEF:scaledTxMin=rawTxMin,8,*" \
            "CDEF:scaledRx=rawRx,8,*" \
            "CDEF:scaledRxMax=rawRxMax,8,*" \
            "CDEF:scaledRxMin=rawRxMin,8,*" \
            LINE1:scaledTx#0000FF:"Tx Average (bps)" \
            LINE1:scaledRx#FF0000:"Rx Average (bps)" 
