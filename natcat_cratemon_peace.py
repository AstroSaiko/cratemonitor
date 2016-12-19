#!/usr/bin/env python

###############################################################################

import os
import socket
import sys
sys.path.append('/home/xtaldaq/PeaceNegotiator')

import pdb
from rrdtool import update as rrd_update
import subprocess
import datetime #for debugging and errorlog
from peaceNegotiator import PeaceNegotiator

###############################################################################

def errorMessage(errorMsg):
    f = open('/home/xtaldaq/cratemonitor_v3/logs/mchErrorLog.log', 'a')
    now = datetime.datetime.now() #Time of event   
    f.write(now.strftime("%Y-%b-%d %H:%M:%S") + ':'  ' {0}\n'.format(errorMsg))
    f.close()

def processChecker(keywordList):
    #Checks the computer for running processes
    #that can cause an inconvenient conflict.
    ps = subprocess.Popen(('ps', 'aux'), stdout=subprocess.PIPE)
    output = ps.communicate()[0]
    for line in output.split('\n'):
        for keyword in keywordList:
            if keyword in line:
                print "Found {0}, initiating self-termination".format(keyword)
                errorMessage("Found {0}, initiating self-termination".format(keyword))
                sys.exit()
    print "Did not find any conflicting processes, carry on"

def rack(mch_address):
        return str.split(mch_address, '-')[1]

def crate(mch_address):
        return str.split(mch_address, '-')[2]

def natcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try :
        s.connect((hostname, port))
    except :
        print 'Unable to connect'
        errorMessage('Unable to connect to {0}'.format(hostname))
        sys.exit()
    s.sendall(content)
    s.sendall("exit\r\n")
    # s.shutdown(socket.SHUT_WR)
    data = []
    while True:
        try :
            tmp = s.recv(1024)
        except :
            print 'receiving failed, MCH is probably busy'
            errorMessage('Receiving failed, {0} is probably busy'.format(hostname))
            break
        if not len(tmp):
            break
        data.append(tmp)
    s.close()
    res = "".join(data)
    # End of natcat().
    return res

###############################################################################

if __name__ == "__main__":
    #=================================
    # Processes that will interfere with
    # this script and cause bad things to happen
    processList = ['fpgaconfig',
                   'firmware_jump',
                   'mmc_interface',
                   'firmware_list',
                   'firmware_write']
    args = sys.argv

    if len(args) < 1:
        print >> sys.stderr, \
            "ERROR Expected one arguments: the MCH IP address"
        sys.exit(1)
    elif ("-h" in args) or ("--help" in args):
        print "Expecting two arguments: the MCH IP address"
        sys.exit(0)

    mch_address = args[1]

    peace = PeaceNegotiator('cratemon', rack(mch_address), crate(mch_address)) #Instantiates a peace object of cratemon type

    temperatures = []
    currents = []
    currents12 = []
    voltagesA = []
    voltagesB = []
    sumCurrs = []

    for fru in [5,6,7,8,9,10,11,12,13,14,15,16,30,40,41,50,53]:
        cmd = 'show_sensorinfo {0}\r\n'.format(fru)
        #Check for conflicting processes.
        #processChecker(processList)
        #print 'Querying FRU #{0}'.format(fru)
        if peace.requestAccess():
            peace.IAmWorking()
            data = natcat(mch_address, 23, cmd)
        elif peace.firmtoolInLine() : 
            peace.giveWay() #Writes 'Go ahead' to negotiations file. Firmware tool will read this and do its thing.
            print 'Giving way to firmtool in line'
            errorMessage('{0} giving way to firmtool in line'.format(mch_address))
            sys.exit()
        else :
            peaceStr = peace.getLine()
            print peaceStr + ' exiting'
            errorMessage('Negotiations file not "Done!" for {0}, exiting. Line = {1}'.format(mch_address, peaceStr))
            sys.exit()
        peace.done() #The work is finished and "Done!" is printed to the negotiations file
        #print data
        temperature = 'U'
        current = 'U'
	current12 = 'U'
        voltageA = 'U'
        voltageB = 'U'
        sumCurr = 'U'

        for item in data.split("\n"):
            if "FPGA Temp" in item:
             #   print item.strip()
                temperature = item.strip().split(" ")[16]
            if "30   Full" in item:
            #    print item.strip()
                current12 = item.strip().split(" ")[13]
            if "28   Full" in item:
           #     print item.strip()
                current = item.strip().split(" ")[13]
	# AMC 13
            if "T2 Temp" in item:
        #        print item.strip()
                temperature = item.strip().split(" ")[16]
            if "5   Full     Temp    0x1e" in item:
          #      print item.strip()
                temperature = item.strip().split(" ")[16]
	    if "1   Full     Temp    0x1e" in item:
         #       print item.strip()
                temperature = item.strip().split(" ")[16]
        # Power Modules    
            if "T-Base" in item:
                #print item.strip()                                                                                                      
                temperature = item.strip().split(" ")[16]
                #print temperature                                                                                                                                    
                #print item.strip().split(" ")                                                                                                                        
            if "VOUT-A" in item:
                #print item.strip()                                                                                                                                   
                voltageA = item.strip().split(" ")[13]
                #print voltage                                                                                                                                        
                #print item.strip().split(" ")                                                                                                                        
            if "VOUT-B" in item:
                #print item.strip()                                                                                                                                   
                voltageB = item.strip().split(" ")[13]
                #print voltage                                                                                                                                        
                #print item.strip().split(" ")
            if "Current(SUM)" in item:
                sumCurr = item.strip().split(" ")[13]
                #print sumCurr
                #print item.strip()
        
        #print 'The Temperature is ' + temperature + ' C'
        #print 'The Current is ' + current + ' A'
	#print 'The 12V current is ' + current12 + 'A'
        temperatures.append(temperature)
        currents.append(current)
	currents12.append(current12)
        voltagesA.append(voltageA)
        voltagesB.append(voltageB)
        sumCurrs.append(sumCurr)
   # print temperatures
   # print currents
   # print currents12
   # print "Done"
    #print sumCurrs

###############################################################################
ret = rrd_update('/home/xtaldaq/cratemonitor_v3/rrd/{0}.rrd'.format(mch_address), 'N:{0[0]}:{0[1]}:{0[2]}:{0[3]}:{0[4]}:{0[5]}:{0[6]}:{0[7]}:{0[8]}:{0[9]}:{0[10]}:{0[11]}:{0[12]}:{0[13]}:{0[14]}:{0[15]}:{0[16]}:{1[0]}:{1[1]}:{1[2]}:{1[3]}:{1[4]}:{1[5]}:{1[6]}:{1[7]}:{1[8]}:{1[9]}:{1[10]}:{1[11]}:{2[0]}:{2[1]}:{2[2]}:{2[3]}:{2[4]}:{2[5]}:{2[6]}:{2[7]}:{2[8]}:{2[9]}:{2[10]}:{2[11]}:{3[15]}:{3[16]}:{4[15]}:{4[16]}:{5[15]}:{5[16]}'.format(temperatures,currents, currents12, voltagesA, voltagesB, sumCurrs))
print "Done"
