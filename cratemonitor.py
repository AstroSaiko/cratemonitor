#!/usr/bin/env python 

import subprocess
import sys
import os
#import signal

#======================================
#Defining which crate we're working with

if len(sys.argv) > 1:
    HOSTNAME = sys.argv[1]
else:
    HOSTNAME = "mch-e1a04-18"
#=====================================

#Defining every board as a class, hence treating each card as an object with sensor data

#===============
# Start PM Class
#===============
class PM:
    """Power module object"""
    def __init__(self, PMIndex):
        self.PMIndex = PMIndex #PM index in crate
        self.entity = "10.{0}".format(str(96 + self.PMIndex)) #converting PM index to ipmi entity
        self.hostname = HOSTNAME
        #Initializing empty variables
        self.tempA = None
        self.tempB = None
        self.tempBase = None
        self.VIN = None
        self.VOutA = None
        self.VOutB = None
        self.volt12V = None
        self.volt3V3 = None
        self.currentSum = None
        self.flavor = None
        #Get data upon instantiation
        self.sensorValueList = self.getData()

    def setHostname(self, hostname):
        self.hostname = hostname
         
    def getData(self):
        self.proc = subprocess.Popen(("ipmitool -H {0} -U '' -P '' sdr entity {1}".format(self.hostname, self.entity)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        (self.data, self.err) = self.proc.communicate()
        if self.err != '':
                #if not "Get HPM.x Capabilities request failed, compcode = c9" in err:                                                                                                                                                      
            if self.err != "Get HPM.x Capabilities request failed, compcode = c9\n":
                print self.err
                return -1
        self.data = self.data.split('\n')
        #=========================================#
        # This block is for NAT-PM-DC840 type PMs #
        #=========================================#
        if "NAT-PM-DC840" in self.data[0]:
            self.flavor = "NAT-PM-DC840"
            if self.data == '':
                print "Error or whatever"
            else:
                for item in self.data:
                    #Temperatures                                                                                                                                                                                                           
                    if "TBrick-A" in item:
                        self.tempA = item.strip().split(" ")[17]    
                    elif "TBrick-B" in item:
                        self.tempB = item.strip().split(" ")[17]
                    elif "T-Base" in item:
                        self.tempBase = item.strip().split(" ")[19]
                    #Input Voltage                                                                                                                                                                                                          
                    elif "VIN" in item:
                        self.VIN = item.strip().split(" ")[22]
                    #Output Voltage                                                                                                                                                                                                         
                    elif "VOUT-A" in item:
                        self.VOutA = item.strip().split(" ")[19]
                    elif "VOUT-B" in item:
                        self.VOutB = item.strip().split(" ")[19]
                    #12V                                                                                                                                                                                                                    
                    elif "12V" in item:
                        self.volt12V = item.strip().split(" ")[22]
                    elif "3.3V" in item:
                        self.volt3V3 = item.strip().split(" ")[21]
                    #Total utput current                                                                                                                                                                                                    
                    elif "Current(SUM)" in item:
                        self.currentSum = item.strip().split(" ")[13]
        #==========================================#
        # End NAT-PM-DC840 block                   #
        #==========================================#
        return [self.tempA, self.tempB, self.tempBase, self.VIN, self.VOutA, self.VOutB, self.volt12V, self.volt3V3, self.currentSum]

    def printSensorValues(self):
        #self.getData()
        if self.flavor == "NAT-PM-DC840":
            print ''
            print "==============================="
            print "    Sensor Values for PM{0}    ".format(self.PMIndex)
            print "==============================="
            print ''
            print "TBrick-A:", self.tempA, "degC"
            print "TBrick-B:", self.tempB, "degC"
            print "T-Base:", self.tempBase, "degC"
            print "Input Voltage:", self.VIN, "V"
            print "Ouput Voltage A:", self.VOutA, "V"
            print "Output Voltage B:", self.VOutB, "V"
            print "12V:", self.volt12V, "V"
            print "3.3V:", self.volt3V3, "V"
            print "Total Current:", self.currentSum, "V"
            print ""

        else:
            print "Unknown PM flavor. Check code and PM class"

#=============
# End PM class
#=============

#================
# Start MCH class
#================

class MCH:
    """MCH object"""
    def __init__(self, MCHIndex = 1):
        self.MCHIndex = MCHIndex                                                                                                                                                                                                      
        self.entity = "194.{0}".format(str(96 + self.MCHIndex)) #converting MCH index to ipmi entity                                                                                                                                        
        self.hostname = "mch-e1a04-18"
        #Initializing empty variables
        self.flavor = None
        self.tempCPU = None
        self.tempIO = None
        self.volt1V5 = None
        self.volt1V8 = None
        self.volt2V5 = None
        self.volt3V3 = None
        self.volt12V = None
        self.current = None
        #Get data upon instantiation                                                                                                                                                                                                        
        self.sensorValueList = self.getData()

    def setHostname(self, hostname):
        self.hostname = hostname

    def getData(self):
        self.proc = subprocess.Popen(("ipmitool -H {0} -U admin -P admin sdr entity {1}".format(self.hostname, self.entity)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        (self.data, self.err) = self.proc.communicate()
        if self.err != '':
        #if not "Get HPM.x Capabilities request failed, compcode = c9" in err:                                                                                                                                                              
            if self.err != "Get HPM.x Capabilities request failed, compcode = c9\n":
                print self.err
                return -1
        self.data = self.data.split('\n')
       #=========================================#
       # This block is for NAT-MCH-MCMC type MCH #
       #=========================================#
        if "NAT-MCH-MCMC" in self.data[0]:
            self.flavor = "NAT-MCH-MCMC"
            for item in self.data:
                if "Temp CPU" in item:
                    self.tempCPU = item.strip().split(" ")[18]
                elif "Temp I/O" in item:
                    self.tempIO = item.strip().split(" ")[18]
                elif "Base 1.2V" in item:
                    self.volt1V2 = item.strip().split(" ")[17]
                elif "Base 1.5V" in item:
                    self.volt1V5 = item.strip().split(" ")[17]
                elif "Base 1.8V" in item:
                    self.volt1V8 = item.strip().split(" ")[17]
                elif "Base 2.5V" in item:
                    self.volt2V5 = item.strip().split(" ")[17]
                elif "Base 3.3V" in item:
                    self.volt3V3 = item.strip().split(" ")[17]
                elif "Base 12V" in item:
                    self.volt12V = item.strip().split(" ")[18]
                elif "Base Current" in item:
                    self.current = item.strip().split(" ")[14]
        #==========================================#                                                                                                                                                                                        
        # End NAT-MCH-MCMC block                   #                                                                                                                                                                                        
        #==========================================#            
        return [self.tempCPU, self.tempIO, self.volt1V2, self.volt1V8, self.volt2V5, self.volt3V3, self.volt12V, self.current]

    def printSensorValues(self):
        #self.getData()
        if self.flavor == "NAT-MCH-MCMC":
            print ''
            print "==============================="
            print "    Sensor Values for MCH{0}      ".format(self.MCHIndex)
            print "==============================="
            print ''
            print "Temp CPU:", self.tempCPU, "degC"
            print "Temp I/O:", self.tempIO, "degC"
            print "Base 1.2V:", self.volt1V2, "V"
            print "Base 1.5V:", self.volt1V5, "V"
            print "Base 1.8V:", self.volt1V8, "V"
            print "Base 2.5V:", self.volt2V5, "V"
            print "Base 3.3V:", self.volt3V3, "V"
            print "Base 12V:", self.volt12V, "V"
            print "Base Current:", self.current, "V"
            print ""

        else:
            print "Unknown MCH flavor, check code and MCH class"

#==============
# End MCH class
#==============

#================
# Start CU class 
#================

class CU:
    '''Cooling Unit object'''
    def __init__(self, CUIndex):
        self.hostname = HOSTNAME
        self.CUIndex = CUIndex
        self.entity = "30.{0}".format(96 + CUIndex)
        if self.CUIndex == 1:
            self.target = "0xa8"
        else:
            self.target = "0xaa"
        #Initializing empty variables
        self.flavor = None
        self.CU3V3 = None
        self.CU12V = None
        self.CU12V_1 = None
        self.LM75Temp = None
        self.LM75Temp2 = None
        self.fan1 = None
        self.fan2 = None
        self.fan3 = None
        self.fan4 = None
        self.fan5 = None
        self.fan6 = None
        #Get data upon instantiation
        self.sensorValueList = self.getData()

    def setHostname(self, hostname):
        self.hostname = hostname

    def checkFlavor(self, flavor):
        self._proc = subprocess.Popen(("ipmitool -H {0} -U admin -P admin sdr entity {1}".format(self.hostname, self.entity)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        (self._data, self._err) = self._proc.communicate()
        self._data = self._data.split('\n')
        if flavor in self._data[0]:
            self.flavor = flavor
            return True
        else:
            return False

    def getData(self):
        self.proc = subprocess.Popen(("ipmitool -H {0} -U '' -P '' -T 0x82 -b 7 -t {1} -B 0 sdr".format(self.hostname, self.target)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        (self.data, self.err) = self.proc.communicate()
        if self.err != '':
        #if not "Get HPM.x Capabilities request failed, compcode = c9" in err:                                                                                                                                                              
            if self.err != "Get HPM.x Capabilities request failed, compcode = c9\n":
                print self.err
                return -1
        self.data = self.data.split('\n')
        #=====================================================#                                                                                                                                                                      
        # This block is for Schroff uTCA CU type Cooling Unit #                                                                       
        #=====================================================#                                                                                                        
        if self.checkFlavor("Schroff uTCA CU"):
            for item in self.data:
                if "+3.3V" in item:
                    self.CU3V3 = item.strip().split(" ")[13]
                elif "+12V " in item:
                    self.CU12V = item.strip().split(" ")[14]
                elif "+12V_1" in item:
                    self.CU12V_1 = item.strip().split(" ")[12]
                elif "LM75 Temp " in item:
                    self.LM75Temp = item.strip().split(" ")[10]
                elif "LM75 Temp2" in item:
                    self.LM75Temp2 = item.strip().split(" ")[9]
                elif "Fan 1" in item:
                    self.fan1 = item.strip().split(" ")[14]
                elif "Fan 2" in item:
                    self.fan2 = item.strip().split(" ")[14]
                elif "Fan 3" in item:
                    self.fan3 = item.strip().split(" ")[14]
                elif "Fan 4" in item:
                    self.fan4 = item.strip().split(" ")[14]
                elif "Fan 5" in item:
                    self.fan5 = item.strip().split(" ")[14]
                elif "Fan 6" in item:
                    self.fan6 = item.strip().split(" ")[14]
        #=====================================================#
        # END Schroff uTCA CU type Cooling Unit block         #                                                                                                                                                                             
        #=====================================================#
        return [self.CU3V3, self.CU12V, self.CU12V_1, self.LM75Temp, self.LM75Temp2, self.fan1, self.fan2, self.fan3, self.fan4, self.fan5, self.fan6]

    def printSensorValues(self):
        #self.getData()
        if self.flavor == "Schroff uTCA CU":
            print ''
            print "==============================="
            print "    Sensor Values for CU{0}    ".format(self.CUIndex)
            print "==============================="
            print ''
            print "+3.3V:", self.CU3V3, "V"
            print "+12V:", self.CU12V, "V"
            print "+12V_1:", self.CU12V_1, "V"
            print "LM75 Temp:", self.LM75Temp, "degC"
            print "LM75 Temp2:", self.LM75Temp2, "degC"
            print "Fan 1:", self.fan1, "rpm"
            print "Fan 2:", self.fan2, "rpm"
            print "Fan 3:", self.fan3, "rpm"
            print "Fan 4:", self.fan4, "rpm"
            print "Fan 5:", self.fan5, "rpm"
            print "Fan 6:", self.fan6, "rpm"
            print ""

        else:
            print "Unkown CU type, check code and CU class"

#=============
# END CU class
#=============

#################
# Start AMC13 class
#################

class AMC13:
    '''AMC13 object'''
    def __init__(self):
        self.hostname = HOSTNAME
        #Initializing empty variables                                                                                                                                                                                                       
        self.flavor = None
        self.T2Temp = None
        self.volt12V = None
        self.volt3V3 = None
        self.volt1V2 = None
        #Get data upon instantiation                                                                                                                                                                                                        
        self.sensorValueList = self.getData()

    def setHostname(self, hostname):
        self.hostname = hostname

    def getData(self):
        self.proc = subprocess.Popen(("ipmitool -H {0} -U admin -P admin sdr entity 193.122".format(self.hostname)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        (self.data, self.err) = self.proc.communicate()
        if self.err != '':
        #if not "Get HPM.x Capabilities request failed, compcode = c9" in err:                                                                                                                                                              
            if self.err != "Get HPM.x Capabilities request failed, compcode = c9\n":
                print self.err
                return -1
        self.data = self.data.split('\n')
        #=====================================================#                                                                                                                                                                             
        # This block is for BU AMC13 type amc13               #                                                                                                                                                                             
        #=====================================================#
        if "BU AMC13" in self.data[0]:
            self.flavor = "BU AMC13"
            for item in self.data:
                if "T2 Temp" in item:
                    self.T2Temp = item.strip().split(" ")[19]
                elif "+12V" in item:
                    self.volt12V = item.strip().split(" ")[21]
                elif "+3.3V" in item:
                    self.volt3V3 = item.strip().split(" ")[20]
                elif "+1.2V" in item:
                    self.volt1V2 = item.strip().split(" ")[20]
        #=====================================================#                                                                                                                                                                             
        # END BU AMC13 type block                             #                                                                                                                                                                             
        #=====================================================#
        return [self.T2Temp, self.volt12V, self.volt3V3, self.volt1V2]

    def printSensorValues(self):
        #self.getData()                                                                                                                                                                                                                     
        if self.flavor == "BU AMC13":
            print ''
            print "==============================="
            print "    Sensor Values for AMC13    "
            print "==============================="
            print ''
            print "T2Temp:", self.T2Temp, "degC"
            print "+12V:", self.volt12V, "V"
            print "+3.3V:", self.volt3V3, "V"
            print "+1.2V:", self.volt1V2, "V"
            print ''
        else:
            print "Unkown AMC13 type, check code and AMC13 class"

if __name__ == "__main__":
    
    try :
        #Instantiate the objects in the crate
        MCH = MCH()
        PM1 = PM(1)
        PM2 = PM(2)
        CU1 = CU(1)
        CU2 = CU(2)
        AMC13 = AMC13()

        #Print sensor values
        MCH.printSensorValues()
        PM1.printSensorValues()
        PM2.printSensorValues()
        CU1.printSensorValues()
        CU2.printSensorValues()
        AMC13.printSensorValues()

        sys.exit(0) #Everything is normal

    except:
        sys.exit(1) # Warning

    
