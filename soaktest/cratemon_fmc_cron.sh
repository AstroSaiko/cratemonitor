#!/bin/bash

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/cactus/lib

#If this works as excepted, just follow the naming conventions and don't worry about the monitoring.
#Nothing ever works as excpected though.

#for rack in 's1g01' 's1g03' 's1g04'
#do
#    for crate in 18 27 36 45
#    do 
#	for slot in '01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12'
#	do
#	    /home/xtaldaq/cratemonitor_v3/getFmcData.py amc-$rack-$crate-$slot 
#	done
 #   done 
#done

#===================
#Early stage testing
#===================

for rack in 's1g01' 's1g03' 's1g04'
do
    for crate in 18 27 36 45
    do
        for slot in '01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12'
        do
	    if [ $rack == "s1g01" ] && [ "$crate" == 18 ] # Staying away from Satoshi's crate
            then
		continue
	    else
		/home/xtaldaq/cratemonitor_v3/getFmcData.py amc-$rack-$crate-$slot &
	    fi
	done
    done
done