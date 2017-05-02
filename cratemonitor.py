#!/usr/bin/env python 

#==================================================
# Author: Birk Engegaard
# birk.engegaard@cern.ch / birkengegaard@gmail.com
# Call script with mch address of the crate you 
# want to monitor, or hardcode the mch address into
# the variable HOSTNAME below
#==================================================

import subprocess
import sys
import os


#======================================
#Defining which crate we're working with

if len(sys.argv) > 1:
    HOSTNAME = sys.argv[1]
else:
    HOSTNAME = "mch-s1g04-18-01" # Insert hostname of mch here

crate = str.upper(str.split(HOSTNAME, '-')[1] + '-' + str.split(HOSTNAME, '-')[2]) # Gives the crate name, e.g. e1a04-18 

# =============================================================
# This will be used at the end of the script to determine
# how the script exits. If a class experiences an error it will 
# update this variable.

class EXITCODE:
    """Quick class to let the classes update the exit code
       0 - OK, 1 - Warning, 2 Critical, 3 Unkown"""
    def __init__(self):
        self.code = 0 # When everything is OK
        self.msg = "OK"
    def getCode(self):
        return self.code
    def setCode(self, newExitCode, string="Something happened"):
        # Will only update exit code if the new exit code is more serious than the previous
        if newExitCode > self.code:
            self.code = newExitCode
            self.msg = string
    def setMsg(self, string):
        self.msg = string
    def getMsg(self):
        return self.msg

# =============================================================


#=====================================
#Defining every board as a class, hence treating each card as an object with sensor data

#===============
# Start PM Class
#===============
class PM:
    """Power module object"""
    def __init__(self, PMIndex):
        self.PMIndex = PMIndex # PM index in crate
        self.entity = "10.{0}".format(str(96 + self.PMIndex)) # converting PM index to ipmi entity
        self.hostname = HOSTNAME # Global variable
        # Initializing empty variables
        self.tempA = None # Temperature of brick-A
        self.tempB = None # Temperature of brick-B
        self.tempBase = None # Base temperature
        self.VIN = None # Input voltage
        self.VOutA = None # Output voltage A
        self.VOutB = None # Output voltage B
        self.volt12V = None # 12V
        self.volt3V3 = None # 3.3V
        self.currentSum = None # total current
        self.flavor = None # PM type
        # Get data upon instantiation
        self.output = self.getData()

    def setHostname(self, hostname):
        self.hostname = hostname
         
    def getData(self):
        self.proc = subprocess.Popen(("ipmitool -H {0} -U '' -P '' sdr entity {1}".format(self.hostname, self.entity)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        (self.data, self.err) = self.proc.communicate()
        if self.err != '':
            if self.err != "Get HPM.x Capabilities request failed, compcode = c9\n": # This error can safely be ignored
                # print self.err
                EXITCODE.setCode(2, self.err) # sys.exit(EXITCODE) will use this at the end
        if self.data == '':
            EXITCODE.setCode(1, "No data received from one or more crate objects") # sys.exit(EXITCODE) will use this at the end
        self.data = self.data.split('\n')
        #=========================================#
        # This block is for NAT-PM-DC840 type PMs #
        #=========================================#
        if "NAT-PM-DC840" in self.data[0]:
            self.flavor = "NAT-PM-DC840"
            for item in self.data:
                    if "TBrick-A" in item:
                        self.tempA = item.strip().split(" ")[17]    
                    elif "TBrick-B" in item:
                        self.tempB = item.strip().split(" ")[17]
                    elif "T-Base" in item:
                        self.tempBase = item.strip().split(" ")[19]
                    elif "VIN" in item:
                        self.VIN = item.strip().split(" ")[22]
                    elif "VOUT-A" in item:
                        self.VOutA = item.strip().split(" ")[19]
                    elif "VOUT-B" in item:
                        self.VOutB = item.strip().split(" ")[19]
                    elif "12V" in item:
                        self.volt12V = item.strip().split(" ")[22]
                    elif "3.3V" in item:
                        self.volt3V3 = item.strip().split(" ")[21]
                    elif "Current(SUM)" in item:
                        self.currentSum = item.strip().split(" ")[13]
        #==========================================#
        # End NAT-PM-DC840 block                   #
        #==========================================#
        return "PM{0}_tempA={1};;;; PM{0}_tempB={2};;;; PM{0}_tempBase={3};;;; \
PM{0}_VIN={4};;;; PM{0}_VOutA={5};;;; PM{0}_VOutB={6};;;; PM{0}_12V={7};;;; \
PM{0}_3.3V={8};;;; PM{0}_currentSum={9};;;;"\
            .format(self.PMIndex, self.tempA, self.tempB, self.tempBase, self.VIN, self.VOutA, self.VOutB, self.volt12V, self.volt3V3, self.currentSum)

    def printSensorValues(self):
       # if self.flavor == "NAT-PM-DC840":
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
            print "Total Current:", self.currentSum, "A"
            print ""

       # else:
           # print "Unknown PM flavor. Check code and PM class"

#=============
# End PM class
#=============

#================
# Start MCH class
#================

class MCH:
    """MCH object"""
    def __init__(self, MCHIndex = 1):
        self.MCHIndex = MCHIndex # Some crates have multiple locations for MCHs         
        self.entity = "194.{0}".format(str(96 + self.MCHIndex)) # converting MCH index to ipmi entity                  
        self.hostname = HOSTNAME # Global variable
        # Initializing empty variables
        self.flavor = None # MCH type
        self.tempCPU = None # CPU temperature
        self.tempIO = None # I/O temperature
        self.volt1V5 = None # 1.5V
        self.volt1V8 = None # 1.8V
        self.volt2V5 = None # 2.5V
        self.volt3V3 = None # 3.3V
        self.volt12V = None # 12V
        self.current = None # base current
        # Get data upon instantiation                                                                                                                                                                                                
        self.output = self.getData()

    def setHostname(self, hostname):
        self.hostname = hostname

    def getData(self):
        self.proc = subprocess.Popen(("ipmitool -H {0} -U admin -P admin sdr entity {1}".format(self.hostname, self.entity)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        (self.data, self.err) = self.proc.communicate()
        if self.err != '':
            if self.err != "Get HPM.x Capabilities request failed, compcode = c9\n": # this error can safely be ignored
                # print self.err
                EXITCODE.setCode(2, self.err)
                return -1
        if self.data == '':
            EXITCODE.setCode(1, "No data received from one or more objects in the crate")
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
        # return [self.tempCPU, self.tempIO, self.volt1V2, self.volt1V8, self.volt2V5, self.volt3V3, self.volt12V, self.current]
        return "MCH{0}_tempCPU={1};;;; MCH{0}_tempIO={2};;;; MCH{0}_1.2V={3};;;; \
MCH{0}_1.5V={4};;;; MCH{0}_1.8V={5};;;; MCH{0}_2.5V={6};;;; MCH{0}_3.3V={7};;;; \
MCH{0}_12V={8};;;; MCH{0}_baseCurrent={9};;;;"\
            .format(self.MCHIndex, self.tempCPU, self.tempIO, self.volt1V2, self.volt1V5, self.volt1V8, self.volt2V5, self.volt3V3, self.volt12V, self.current)
 
    def printSensorValues(self):
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
            print "Base Current:", self.current, "A"
            print ""

        # else:
            # print "Unknown MCH flavor, check code and MCH class"

#==============
# End MCH class
#==============

#================
# Start CU class 
#================

class CU:
    '''Cooling Unit object'''
    def __init__(self, CUIndex):
        self.hostname = HOSTNAME # global variable
        self.CUIndex = CUIndex # CU index 
        self.entity = "30.{0}".format(96 + CUIndex) # converting index to entity number
        if self.CUIndex == 1:
            self.target = "0xa8" # converting index to target ID
        else:
            self.target = "0xaa" # converting index to target ID
        # Initializing empty variables
        self.flavor = None # CU type
        self.CU3V3 = None # 3.3V
        self.CU12V = None # 12V
        self.CU12V_1 = None # 12V_1
        self.LM75Temp = None # temperature
        self.LM75Temp2 = None # temperature 2
        self.fan1 = None # fan speed
        self.fan2 = None # fan speed
        self.fan3 = None # fan speed
        self.fan4 = None # fan speed
        self.fan5 = None # fan speed
        self.fan6 = None # fan speed
        # Get data upon instantiation
        self.output = self.getData()

    def setHostname(self, hostname):
        self.hostname = hostname

    def checkFlavor(self, flavor):
        self._proc = subprocess.Popen(("ipmitool -H {0} -U admin -P admin sdr entity {1}".format(self.hostname, self.entity)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        (self._data, self._err) = self._proc.communicate()
        if self._err != '':
            if self._err != "Get HPM.x Capabilities request failed, compcode = c9\n": # this error can be ingored
                # print self._err
                EXITCODE.setCode(2, self._err)
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
            if self.err != "Get HPM.x Capabilities request failed, compcode = c9\n": # this error can be ingored
                # print self.err
                EXITCODE.setCode(2, self.err)
                return -1
        if self.data == '':
            EXITCODE.setCode(1, "No data received from one or more objects in the crate")
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
        # return [self.CU3V3, self.CU12V, self.CU12V_1, self.LM75Temp, self.LM75Temp2, self.fan1, self.fan2, self.fan3, self.fan4, self.fan5, self.fan6]
        return "CU{0}_temp1={1};;;; CU{0}_temp2={2};;;; CU{0}_3.3V={3};;;; \
CU{0}_12V={4};;;; CU{0}_12V_1={5};;;; CU{0}_fan1={6};;;; CU{0}_fan2={7};;;; \
CU{0}_fan3={8};;;; CU{0}_fan4={9};;;; CU{0}_fan5={10};;;; CU{0}_fan6={10};;;;"\
            .format(self.CUIndex, self.LM75Temp, self.LM75Temp2, self.CU3V3, self.CU12V, self.CU12V_1, self.fan1, self.fan2, self.fan3, self.fan4, self.fan5, self.fan6)

    def printSensorValues(self):
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

        # else:
            # print "Unkown CU type, check code and CU class"

#=============
# END CU class
#=============

#################
# Start AMC13 class
#################

class AMC13:
    '''AMC13 object'''
    def __init__(self):
        self.hostname = HOSTNAME # global variable
        # Initializing empty variables             
        self.flavor = None # amc13 type
        self.T2Temp = None # T2 temperature
        self.volt12V = None # 12V
        self.volt3V3 = None # 3.3V
        self.volt1V2 = None # 1.2V
        # Get data upon instantiation     
        self.output = self.getData()

    def setHostname(self, hostname):
        self.hostname = hostname

    def getData(self):
        self.proc = subprocess.Popen(("ipmitool -H {0} -U admin -P admin sdr entity 193.122".format(self.hostname)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        (self.data, self.err) = self.proc.communicate()
        if self.err != '':
            if self.err != "Get HPM.x Capabilities request failed, compcode = c9\n": # this error can be ignored
                # print self.err
                EXITCODE.setCode(2, self.err)
        if self.data == '':
            EXITCODE.setCode(1, "No data received from one or more objects in the crate")
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
        # return [self.T2Temp, self.volt12V, self.volt3V3, self.volt1V2]
        return "AMC13_T2Temp={0};;;; AMC13_1.2V={1};;;; AMC13_3.3V={2};;;; AMC13_12V={3};;;;"\
            .format(self.T2Temp, self.volt1V2, self.volt3V3, self.volt12V)

    def printSensorValues(self):
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
        # else:
            # print "Unkown AMC13 type, check code and AMC13 class"

###################
# END AMC13 class
##################

#================
# Start FC7 class
#================

class FC7:
    '''FC7 object'''
    def __init__(self, FC7Index):
        self.hostname = HOSTNAME # global variable
        self.FC7Index = FC7Index # amc index / slot number in crate
        self.entity = "193.{0}".format(96 + FC7Index) # index to entity id
        # Initializing empty variables                                 
        self.flavor = None # FC7 type
        self.humidity = None # humidity
        self.temperature = None # temperature
        self.volt3V3 = None # 3.3V
        self.current3V3 = None # 3.3V current
        self.volt5V = None # 5V
        self.current5V = None # 5V current
        self.l12_VADJ = None # l12 ADJ voltage
        self.l12_IADJ = None # l12 ADJ curent
        self.volt2V5 = None # 2.5V
        self.current2V5 = None # 2.5V current
        self.volt1V8 = None # 1.8V
        self.current1V8 = None # 1.8V current
        self.voltMP3V3 = None # MP 3.3V
        self.currentMP3V3 = None # MP 3.3V current
        self.volt12V = None # 12V
        self.current12V = None # 12V current
        self.volt1V5 = None # 1.5V 
        self.current1V5 = None # 1.5V current
        self.volt1V = None # 1V
        self.current1V = None # 1V current
        self.volt1V8_GTX = None # gtx 1.8V
        self.current1V8_GTX = None # gtx 1.8V current
        self.volt1V_GTX = None # gtx 1V
        self.current1V_GTX = None # gtx 1V current
        self.volt1V2_GTX = None # gtx 1.2V
        self.current1V2_GTX = None # gtx 1.2V current
        self.l8_VADJ = None # l8 ADJ voltage 
        self.l8_IADJ = None # l8 ADJ current
        # Get data upon instantiation                                                                                                            
        self.sensorValueList = self.getData()

    def setHostname(self, hostname):
        self.hostname = hostname

    def checkFlavor(self, flavor):
        self._proc = subprocess.Popen(("ipmitool -H {0} -U admin -P admin sdr entity {1}".format(self.hostname, self.entity)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        (self._data, self._err) = self._proc.communicate()
        if self._err != '':
            if self._err != "Get HPM.x Capabilities request failed, compcode = c9\n": # this error can be ingored  
                # print self._err
                EXITCODE.setCode(2, self._err)
                return -1
        self._data = self._data.split('\n')
        if flavor in self._data[0]:
            self.flavor = flavor
            return True
        else:
            return False

    def getData(self):
        self.proc = subprocess.Popen(("ipmitool -H {0} -U admin -P admin sdr entity {1}".format(self.hostname, self.entity)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        (self.data, self.err) = self.proc.communicate()
        if self.err != '':
            if self.err != "Get HPM.x Capabilities request failed, compcode = c9\n": # this error can be ignored
                print self.err
                EXITCODE.setCode(2, self.err)
        if self.data == '':
            EXITCODE.setCode(1, "No data received from one or more objects in the crate")
            return -1
        self.data = self.data.split('\n')
        if "ICL-CERN FC7" in self.data[0]:
            # =======================================
            # This block is for the ICL-CERN FC7 type
            # ======================================
            print "ICL-CERN FC7 not available"
            return 0

        elif "FC7-R2" in self.data[0]:
            # =======================================
            # This is for the FC7-R2 MMC
            # =======================================
            return 0

    def printSensorValues(self):
        print "This function is not yet completed"

if __name__ == "__main__":

    EXITCODE = EXITCODE() # For proper exit codes
    # Instantiate the objects in the crate
    
    # =========================================
    # Basic uTCA crate / Common for every crate
    # =========================================
    PM1 = PM(1)
    PM4 = PM(4)
    CU1 = CU(1)
    CU2 = CU(2)
    MCH = MCH()
    amc13 = AMC13()
    # =========================================
    # FC7s and crate specifics
    # =========================================
    
    # =========================================
    # Format output
    # =========================================
    status = ["OK", "WARNING", "CRITICAL", "UNKNOWN"]
    if EXITCODE.getCode() == 0:
        print "Sensor values {0} | {1} {2} {3} {4} {5} {6}".format(status[EXITCODE.getCode()], PM1.output, PM4.output, CU1.output, CU2.output, MCH.output, amc13.output) 
    else:
        print "Sensor values {0}, Message: {1} | {2} {3} {4} {5} {6} {7}".format(status[EXITCODE.getCode()], EXITCODE.getMsg(), PM1.output, PM4.output, CU1.output, CU2.output, MCH.output, amc13.output)
    
    MCH.printSensorValues()
    PM1.printSensorValues()
    PM4.printSensorValues()
    CU1.printSensorValues()
    CU2.printSensorValues()
    amc13.printSensorValues()
    # Exit with appropriate exit code
    sys.exit(EXITCODE.getCode())
