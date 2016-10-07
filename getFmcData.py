#!/usr/bin/env python

# Author: Laurent CHARLES (IPHC Strasbourg)
# PixFED project - CMS Upgrade Ph.1
# Edited by Birk Engegaard (CERN) for monitoring purposes

#========================================================
# This script will return T_INT, V1, V2, V3, V4 and VCC
# from the FITEL FED.
# Run as $python fmcmonitor.py hostname
# =======================================================

from time import sleep
from struct import *
import sys; sys.path.append('/home/xtaldaq/PyChips')  #To set PYTHONPATH to the PyChips installation src folder
from time import *

import os
import socket
import pdb
from rrdtool import update as rrd_update

# -*- coding: cp1252 -*-
#  Import the PyChips code - PYTHONPATH must be set to the PyChips installation src folder!
from PyChipsUser import *

#t = time() #for timing

##--=======================================--
##=> IP address
##--=======================================--
# Read in an address table by creating an AddressTable object (Note the forward slashes, not backslashes!)

##################################################################                    
# To read IP address or host name  from command line or ipaddr.dat               
##################################################################
args = sys.argv

if len(args) > 1:

   ipaddr = args[1]

else:
   f = open('/home/xtaldaq/cratemonitor_v3/ipaddr.dat', 'r')
   ipaddr = f.readline()
   f.close()
hostname = str.lower(ipaddr) #for the rrd database at the bottom of the script

##################################################################
#For the rrd database
def rack(hostname):
   return str.split(hostname, '-')[1]

def crate(hostname):
   return str.split(hostname, '-')[2]

def amc(hostname):
   return str.split(hostname, '-')[3]

##################################################################



fc7AddrTable = AddressTable('/home/xtaldaq/cratemonitor_v3/fc7AddrTable.dat')
#f = open('./ipaddr.dat', 'r')
#ipaddr = f.readline()
#f.close()
fc7 = ChipsBusUdp(fc7AddrTable, ipaddr, 50001)
print
print "--=======================================--"
print "  Opening FC7 with IP", ipaddr
print "--=======================================--"
##--=======================================--



#************************************************************************#
#----> INIT AT STARTUP
#************************************************************************#
#fc7.write("PC_config_ok",0)
#i2c controller reset + fifo TX & RX reset
fc7.write("fitel_i2c_cmd_reset",1) #1: EN
sleep(0.200)
fc7.write("fitel_i2c_cmd_reset",0) #0: DIS
#
fc7.write("fitel_rx_i2c_req",0) #0: DIS
fc7.write("fitel_sfp_i2c_req",0) #0: DIS


#************************************************************************#
#----> CONSTANTS
#************************************************************************#
# general
i2c_cmd_rd  = 3
i2c_cmd_wr  = 1
# LTC2990: see the datasheet
single      = 1
repeat      = 0
measureNb   = 6 #T_INT, V1, V2, V3, V4 and VCC
regNb       = 2*measureNb # by device / 2 reg necessary for each measure
trig        = 0x01 
acq         = single
ctrl        = (acq<<6)+0x1f # mode V1,V2,V3,V4 voltage measurements
dataFormat  = 15 # format: 15-bit signed. This is for the voltage measurements. The temperature word is 13-bit unsigned.
fullScale   = 2**(dataFormat) 

#**********************************************************************************************************************************************#
#----> USER CHOICES !!!!!
#**********************************************************************************************************************************************#
#=>DEVICE ACCESS SELECTED BY THE USER
#with this order => (FMCL8_FRR1, FMCL8_FRR2, FMCL12_FRR1, FMCL12_FRR2)
FITEL_ACCESS = (1,1,0,0)

#=>Computing of the number of devices
FITEL_DEVICE_NB_MAX = 4
FITEL_DEVICE_NB = 0
for i in range(0, 4):
   FITEL_DEVICE_NB = FITEL_DEVICE_NB + FITEL_ACCESS[i]
print "-> FITEL_DEVICE_NB =", FITEL_DEVICE_NB

#**********************************************************************************************************************************************#
#----> END USER CHOICES !!!!!
#**********************************************************************************************************************************************#   



#**********************************************************************************************************************************************#
#----> START FIRST ACCESS
#**********************************************************************************************************************************************#
print "-> Start First Access"



#************************************************************************#
#----> VECTORS DECLARATION FOR THE I2C TRANSACTIONS
#************************************************************************#
regAddr  = range(regNb*FITEL_DEVICE_NB)
wrData   = range(regNb*FITEL_DEVICE_NB)
fmcSel   = range(regNb*FITEL_DEVICE_NB)
fitelSel = range(regNb*FITEL_DEVICE_NB)


#************************************************************************#
#----> VECTORS INIT FOR THE I2C TRANSACTIONS
#************************************************************************#
index = 0
for i in range(0, 4):
    if FITEL_ACCESS[i] == 1:
        regAddr[index]     = 0x01
        wrData[index]      = ctrl       
        regAddr[index+1]   = 0x02
        wrData[index+1]    = trig        
        if      i == 0:
            fmcSel[index]     = 0
            fitelSel[index]   = 0
            fmcSel[index+1]   = 0
            fitelSel[index+1] = 0            
        elif    i == 1:
            fmcSel[index]     = 0
            fitelSel[index]   = 1
            fmcSel[index+1]   = 0
            fitelSel[index+1] = 1             
        elif    i == 2:
            fmcSel[index]     = 1
            fitelSel[index]   = 0
            fmcSel[index+1]   = 1
            fitelSel[index+1] = 0             
        elif    i == 3:
            fmcSel[index]     = 1
            fitelSel[index]   = 1         
            fmcSel[index+1]   = 1
            fitelSel[index+1] = 1
        index = index + 2


#************************************************************************#
#----> CHECKING / I2C Transactions
#************************************************************************#
disp = 1
if disp == 1:
   print "-> Checking:"
   print "--------------------------------------------------------------------------------"
   for j in range (index):
       print "fmcSel =",fmcSel[j],"fitelSel =",fitelSel[j],"\t|\t","regAddr =",hex(regAddr[j]),"\t|\t","wrData =",hex(wrData[j])
   print "--------------------------------------------------------------------------------"

#************************************************************************#
#----> Fill-in of FIFO TX
#************************************************************************#
i2cWordNb  = index #FITEL_DEVICE_NB * 2
wrBuffer = []
for i in range(0, i2cWordNb):
    wrBuffer.append(fmcSel[i]<<24 | fitelSel[i]<<20 | regAddr[i]<<8 | wrData[i])
    print hex(wrBuffer[i])    
fc7.fifoWrite("fitel_config_fifo_tx", wrBuffer, 0)
print "->",i2cWordNb,"words to write to FIFO TX..."


#************************************************************************#
#----> I2C CMD
#************************************************************************#
#fc7.write("fitel_i2c_addr",0x77) # Global Sync Address
fc7.write("fitel_i2c_addr",0x4c) 
#print "fitel_i2c_addr = ",bin(fc7.read("fitel_i2c_addr"))
sleep(0.010)
fc7.write("fitel_rx_i2c_req", i2c_cmd_wr) # see higher



#************************************************************************#
#----> ACK
#************************************************************************#
while fc7.read("fitel_i2c_ack") == 0:
##   print "fitel_rx_i2c_req = ",bin(fc7.read("fitel_rx_i2c_req"))
##   print "fitel_i2c_ack = ",bin(fc7.read("fitel_i2c_ack"))    
   sleep(0.010)
if    fc7.read("fitel_i2c_ack") == 0b01:
   print "-> i2c ok and ADC in acquisition"  
elif  fc7.read("fitel_i2c_ack") == 0b11:
   print "-> i2c ko"   

#************************************************************************#
#----> RELEASE - HANDSHAKING WITH F/W
#************************************************************************#
fc7.write("fitel_rx_i2c_req", 0) #cmd : 0=no / 1=rd / 3=wr  
while fc7.read("fitel_i2c_ack") != 0:
   sleep(0.010)
   print "-> fitel_i2c_ack:", glib.read("fitel_i2c_ack")



#************************************************************************#
#----> SLEEP
#************************************************************************#
print "sleep"
#fc7.write("fitel_i2c_cmd_reset",1) #1: EN
sleep(1.0)
#fc7.write("fitel_i2c_cmd_reset",0) #0: DIS

print "-> End First Access"
#**********************************************************************************************************************************************#
#----> END FIRST ACCESS
#**********************************************************************************************************************************************#
#
#
#
#
#**********************************************************************************************************************************************#
#----> START SECOND ACCESS
#**********************************************************************************************************************************************#
print
print
print "-> Start Second Access"

#TEST
##        regAddr[index+0]   = 0x06    
##        regAddr[index+1]   = 0x07      
##        regAddr[index+2]   = 0x08
##        regAddr[index+3]   = 0x09
##        regAddr[index+4]   = 0x0a
##        regAddr[index+5]   = 0x0b
##        regAddr[index+6]   = 0x0c
##        regAddr[index+7]   = 0x0d
##        regAddr[index+8]   = 0x0e
##        regAddr[index+9]   = 0x0e





#************************************************************************#
#----> VECTORS INIT FOR THE I2C TRANSACTIONS
#************************************************************************#
index = 0
for i in range(0, 4):
    if FITEL_ACCESS[i] == 1:
       for j in range(regNb):
          wrData[index+j]  = 0
          regAddr[index+j] = 0x04 + j #from @0x04: see datasheet
          if      i == 0:
             fmcSel[index+j]     = 0
             fitelSel[index+j]   = 0          
          elif    i == 1:
             fmcSel[index+j]     = 0
             fitelSel[index+j]   = 1          
          elif    i == 2:
             fmcSel[index+j]     = 1
             fitelSel[index+j]   = 0          
          elif    i == 3:
             fmcSel[index+j]     = 1
             fitelSel[index+j]   = 1
       index = index + regNb


#************************************************************************#
#----> CHECKING / I2C Transactions
#************************************************************************#
disp2 = 1
if disp2 == 1:
   print "-> Checking:"
   print "--------------------------------------------------------------------------------"
   for j in range (index):
       print "fmcSel =",fmcSel[j],"fitelSel =",fitelSel[j],"\t|\t","regAddr =",hex(regAddr[j]),"\t|\t","wrData =",hex(wrData[j])
   print "--------------------------------------------------------------------------------"




#************************************************************************#
#----> Fill-in of FIFO TX
#************************************************************************#
i2cWordNb  = index
wrBuffer2 = []
for i in range(0, i2cWordNb):
    wrBuffer2.append(fmcSel[i]<<24 | fitelSel[i]<<20 | regAddr[i]<<8 | 0)
fc7.fifoWrite("fitel_config_fifo_tx", wrBuffer2, 0)
print "->",i2cWordNb,"words to write to FIFO TX..."

##for i in range(0, i2cWordNb):
##    print hex(wrBuffer2[i])
##    #print regAddr[i]

#************************************************************************#
#----> I2C CMD
#************************************************************************#
fc7.write("fitel_i2c_addr",0x4c)
#print "fitel_i2c_addr = ",bin(fc7.read("fitel_i2c_addr"))
sleep(0.010)
fc7.write("fitel_rx_i2c_req", i2c_cmd_rd) # see higher



#************************************************************************#
#----> ACK
#************************************************************************#
while fc7.read("fitel_i2c_ack") == 0:  #do not suppress else error
    sleep(0.010)
if    fc7.read("fitel_i2c_ack") == 0b01:
   print "-> i2c ok and reading done"  
elif  fc7.read("fitel_i2c_ack") == 0b11:
   print "-> i2c ko"  


#************************************************************************#
#----> RELEASE - HANDSHAKING WITH F/W
#************************************************************************#
fc7.write("fitel_rx_i2c_req", 0) #cmd : 0=no / 1=rd / 3=wr  
while fc7.read("fitel_i2c_ack") != 0:
   sleep(0.010)
   print "-> fitel_i2c_ack:", fc7.read("fitel_i2c_ack")


#************************************************************************#
#----> Readout of FIFO RX
#************************************************************************#
print "->",i2cWordNb," words to read from FIFO_RX..."
rdBuffer = []
rdBuffer = fc7.fifoRead("fitel_config_fifo_rx", i2cWordNb, 0)

##for i in range (0, i2cWordNb): #to check the moment where the RX FIFO is empty
##   print "-> fitel_config_fifo_rx_empty:", fc7.read("fitel_config_fifo_rx_empty")    
##   toto =  fc7.read("fitel_config_fifo_rx")  
##   print "-> fitel_config_fifo_rx_empty:", fc7.read("fitel_config_fifo_rx_empty")
   
#************************************************************************#
#----> CHECKING / CONTENTS FROM FIFO RX 
#************************************************************************#
disp = 1
if disp == 1:
   print "-> Checking:"
   for i in range (0, i2cWordNb):
      #rdBuffer[i] = rdBuffer[i] & 0xff
      print "->", hex(rdBuffer[i])     
   print "--------------------"  

#************************************************************************#
#----> Mask on rdBuffer - Keep only the reg data byte = LSB
#************************************************************************#
for i in range (0, i2cWordNb):
   rdBuffer[i] = rdBuffer[i] & 0xff



#************************************************************************#
#----> Measurement Computing 
#************************************************************************#

#####test
##rdBuffer[0]   = 0xaa   
##rdBuffer[1]   = 0x50
##rdBuffer[2]   = 0xaa
##rdBuffer[3]   = 0x52
##rdBuffer[4]   = 0xaa
##rdBuffer[5]   = 0x54
##rdBuffer[6]   = 0xaa
##rdBuffer[7]   = 0x56
##rdBuffer[8]   = 0xaa
##rdBuffer[9]   = 0x58
##rdBuffer[10]  = 0xaa
##rdBuffer[11]  = 0x5a
##rdBuffer[12]  = 0xaa
##rdBuffer[13]  = 0x5c
##rdBuffer[14]  = 0xaa
##rdBuffer[15]  = 0x5e
####rdBuffer[16]  = 0xac #  see datasheet p17/24: 0b1010_1100_1100_1101 = 0xac_cd  => 3,5V
####rdBuffer[17]  = 0xcd
##rdBuffer[16]  = 0xfc #  see datasheet p17/24: 0b1111_1100_0010_1001 = 0xfc_29  => -0.3V
##rdBuffer[17]  = 0x29   
##rdBuffer[18]  = 0x82 #  see datasheet p17/24 for VCC: 0b1000_0010_1000_1111 = 0x82_8f => 2.7V
##rdBuffer[19]  = 0x8f
###RdBuffer = [255]*regNb




# lst=[[0]*col]*ln 
LTC2990  = [[0.0]*measureNb]*4 #FITEL_DEVICE_NB_MAX = 4

T_INT = []
V1 = []
V2 = []
V3 = []
V4 = []
VCC = []


index = 0
for i in range(0, 4):
   if FITEL_ACCESS[i] == 1:
      if    i==0:        
         print "-> Measurement for ADC from Fitel FMCL8_FRR1"
      elif  i==1:       
         print "-> Measurement for ADC from Fitel FMCL8_FRR2"    
      elif  i==2:         
         print "-> Measurement for ADC from Fitel FMCL12_FRR1"
      elif  i==3:        
         print "-> Measurement for ADC from Fitel FMCL12_FRR2"
      #
      for j in range(measureNb):

         ###################################################################################
         #Debugging
         #if j == 0: #for temp
         #    debugBits = rdBuffer[index + 2*j] << 5  # show bit 7, 6 and 5 of MSB. See documentation                                                   
         #    print('DV, SS, SO: ' + bin(debugBits)[2] + ', ' + bin(debugBits)[3] + ', ' + bin(debugBits)[4])
         #else: #for voltages
         #debugBits = rdBuffer[index + 2*j] >> 6 # show bit 7 and 6 of MSB. See documentation
         #print('DV, Sign: ' + bin(debugBits)[2] + ', ' + bin(debugBits)[3])

         ###################################################################################
         
         ###################################################################################

         if j == 0: 
            data = (((rdBuffer[index+2*j] & 0x1f)   << 8) + rdBuffer[index+2*j+1]) #generates the unisgned 13-bit word for T_INT
            T_INT.append(float(data)/16) # [Fitel 1 RX 1, Fitel 1 RX 2, Fitel 2 RX1, Fitel 2 RX2, ...]
         else:
            data = (((rdBuffer[index+2*j] & 0x7f)   << 8) + rdBuffer[index+2*j+1]) # generates the signed 15-bit word  
            sign = data >> 14 #bit(14)
            if j == 1:
               if sign == 0b1:
                  V1.append(-(fullScale - data) * 0.00030518)
               else:
                  V1.append(data * 0.00030518)
            elif j == 2:
               if sign == 0b1:
                  V2.append(-(fullScale - data) * 0.00030518)
               else:
                  V2.append(data * 0.00030518)
            elif j == 3:
               if sign == 0b1:
                  V3.append(-(fullScale - data) * 0.00030518)
               else:
                  V3.append(data * 0.00030518)
            elif j == 4:
               if sign == 0b1:
                  V4.append(-(fullScale - data) * 0.00030518)
               else:
                  V4.append(data * 0.00030518)
            elif j == 5:
               if sign == 0b1:
                  VCC.append(-(fullScale - data) * 0.00030518 + 2.5)
               else:
                  VCC.append(data * 0.00030518 + 2.5)

            #data2sComp = fullScale - data # 2's complement of data  
         ###################################################################################   
         if j == 0: #For T_INT
            LTC2990[i][j] = float(data)/16 
         elif j == 5: #for V5: VCC
            if sign == 0b1:
               LTC2990[i][j] = -(fullScale - data) * 0.00030518 + 2.5
            else:
               LTC2990[i][j] = data * 0.00030518 + 2.5            
         else: #for the rest of the voltages
            if sign == 0b1:
               LTC2990[i][j] = -(fullScale - data) * 0.00030518
            else:
               LTC2990[i][j] = data * 0.00030518
         #                  
         #print "->  V[",j+1,"]  =  %.4fV" % (LTC2990[i][j])
         if    j==0:
            print "1)\tT_INT(degC)  =  %.4fdegC\t\t-> Internal temperature" % (LTC2990[i][j])
         elif  j==1:
            print "2)\tV1(V)\t     =   %.5fV\t\t-> 3V3" % (LTC2990[i][j])
         elif  j==2:
            print "3)\tV2(V)\t     =   %.5fV\t\t-> 3V3" % (LTC2990[i][j]) 
         elif  j==3:
            print "4)\tV3(mV)\t     =  %.5fmV\t\t-> RSSI" % (LTC2990[i][j]*1000)
            print "\tV3(V)\t     =  %.8fV\t\t-> RSSI" % (LTC2990[i][j])             
         elif  j==4:
            print "5)\tV4(V)\t     =  %.5fV\t\t-> GND" % (LTC2990[i][j]) 
         elif  j==5:
            print "6)\tV5(V)\t     =   %.5fV\t\t-> VCC" % (LTC2990[i][j])
##         print "unsigned data","\tin hex =", hex(data), "\tin dec =",data
##         print "__signed data","\tin hex =", hex(data), "\tin dec =",fullScale-data         
##         print "sign =", sign
      index = index + 2*measureNb
   

#**********************************************************************************************************************************************#
#----> END SECOND ACCESS
#**********************************************************************************************************************************************#

#ret = rrd_update('/home/xtaldaq/python_scripts/fmcmonitor/{0}.rrd'.format(ipaddr), 'N:{0[0]}:{0[1]}:{1[0]}:{1[1]}:{2[0]}:{3[0]}:{3[1]}:{4[0]}:{4[1]}:{5[0]}:{5[1]}'.format(T_INT, V1, V2, V3, V4, VCC))

#one database for each AMC. Database format = [RX1TEMP, RX2TEMP, RX1V1, RX2V1, ... ]

rack = rack(hostname)
crate = crate(hostname)
amc = amc(hostname)

ret = rrd_update('/home/xtaldaq/cratemonitor_v3/rrd/amc-{0}-{1}-{2}.rrd'.format(rack, crate, amc), 'N:{0[0]}:{0[1]}:{1[0]}:{1[1]}:{2[0]}:{2[1]}:{3[0]}:{3[1]}\
:{4[0]}:{4[1]}:{5[0]}:{5[1]}'.format(T_INT, V1, V2, V3, V4, VCC))


print   
print          
print "-> End"

#elapsed = time() - t
#print(elapsed)
          
