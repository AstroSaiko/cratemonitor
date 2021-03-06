#!/usr/bin/env python 

import subprocess
import sys
import os
import signal
import time

HOSTNAME = "mch-e1a04-18"

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

                          
#def getPMData(slot):
#    class PM:
#        def __init__(self, PMIndex):
#            self.PMIndex = PMIndex
#            self.entity = "10.{0}".format(str(96 + self.PMIndex))
#            self.tempA = None
#            self.tempB = None
#            self.tempBase = None
#            self.VIN = None
#            self.VOutA = None
#            self.VOutB = None
#            self.volt12 = None
#            self.volt3V3 = None
#            self.current = None
#           self.getData()
#
#        def getData(self):
#            proc = subprocess.Popen(("ipmitool -H mch-e1a04-18 -U '' -P '' sdr entity {0}".format(self.entity)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
#            (self.data, self.err) = proc.communicate()
#            if self.err != '':
#                #if not "Get HPM.x Capabilities request failed, compcode = c9" in err:                                                                                                                                                     # 
#                if self.err != "Get HPM.x Capabilities request failed, compcode = c9\n":
#                    print self.err
#                    return -1
#            self.data = self.data.split('\n')
#            if "NAT-PM-DC840" in self.data[0]:
#                print "hello!"
#
#    PM1 = PM(1)
#    PM2 = PM(2)
#    PM3 = PM(3)
#    PM4 = PM(4)
#
#    if slot == 1:
#        PM = "0xc2"
#    elif slot == 2:
#        PM = "0xc4"
#    elif slot == 3:
#        PM = "0xc6"
#    elif slot == 4:
#        PM = "0xc8"
#    else:
#        print "Please insert a valid slot (1-4)"
#        return -1 
#    proc = subprocess.Popen(("ipmitool -H mch-e1a04-18 -U '' -P '' -T 0x82 -b 7 -B 0 -t {0} sdr".format(PM)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
#    (data, err) = proc.communicate()
#    if err != '':
#        #if not "Get HPM.x Capabilities request failed, compcode = c9" in err:
#       if err != "Get HPM.x Capabilities request failed, compcode = c9\n":
#           print err
#           return -1
#   data = data.split('\n')
#   return data

def getCUData(CU_index):
    if CU_index == 1:
        CU = "0xa8"
    elif CU_index == 2:
        CU = "0xaa"
    else:
        print "Please insert a valid index (1 or 2)"
        return -1
    proc = subprocess.Popen(("ipmitool -H mch-e1a04-18 -U '' -P '' -T 0x82 -b 7 -B 0 -t {0} sdr".format(CU)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    (data, err) = proc.communicate()
    if err != '':
        #if not "Get HPM.x Capabilities request failed, compcode = c9" in err:
        if err != "Get HPM.x Capabilities request failed, compcode = c9\n":    
            print err
            return -1
    data = data.split('\n')
    return data

def getAMC13Data():
    proc = subprocess.Popen(("ipmitool -H mch-e1a04-18 -U admin -P admin sdr entity 193.122").split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    (data, err) = proc.communicate()
    if err != '':
        #if not "Get HPM.x Capabilities request failed, compcode = c9" in err:
        if err != "Get HPM.x Capabilities request failed, compcode = c9\n":
            print err
            return -1
    data = data.split('\n')
    return data

if __name__ == "__main__":

    PM1 = PM(1)
    PM2 = PM(2)
    PM1.printSensorValues()
    PM2.printSensorValues()
    MCH = MCH()
    MCH.printSensorValues()
    CU1 = CU(1)
    CU2 = CU(2)
    CU1.printSensorValues()
    CU2.printSensorValues()
    amc13 = AMC13()
    amc13.printSensorValues()
    
    #For PMs
    PMVoltages = []
    PMTemperatures = []
    PMCurrents = []

    #For CUs
    CUVoltages = []
    CUTemperatures = []
    fanSpeeds = []
    
    #for AMC13
    #T2Temp = []
    #amc1312V = []
    #amc133V3 = []
    #amc131V2 = []

    for i in [1, 2]:

        #for PMs
        #empA = None
        #empB = None
        #empBase = None
        #IN = None
        #OutA = None
        #OutB = None
        #urrent = None
        #olt12 = None
        #volt3V3 = None

        #data = getPMData(i)
        #if data == -1:
        #    print "Error or whatever"
        #else:
        #    for item in data:
        #        #Temperatures
        #        if "TBrick-A" in item:
        #            tempA = item.strip().split(" ")[10]
       #        elif "TBrick-B" in item:
        #            tempB = item.strip().split(" ")[10]
        #        elif "T-Base" in item:
         #           tempBase = item.strip().split(" ")[12]
         #       #Input Voltage
        #        elif "VIN" in item:
        #            VIN = item.strip().split(" ")[15]
        #        #Output Voltage
         #       elif "VOUT-A" in item:   
         #           VOutA = item.strip().split(" ")[12]
         #           #print VOutA
         #       elif "VOUT-B" in item:                                                                                                            
         #           VOutB = item.strip().split(" ")[12]
         #           #print VOutB
         #       #12V
         #       elif "12V" in item:
         #           volt12 = item.strip().split(" ")[15]
         #           #print volt12
         #       #3.3V
         #       elif "3.3V" in item:
         #           volt3V3 = item.strip().split(" ")[14]
          ##          #print volt3V3
          #      #Total utput current
          #      elif "Current(SUM)" in item:
          #          current = item.strip().split(" ")[6]
          #          #print current
                #print tempA
                #print tempB
        #print tempBase
        #PMTemperatures.append(tempA)
        #PMTemperatures.append(tempB)
        #PMTemperatures.append(tempBase)
        #PMVoltages.append(VIN)
        #PMVoltages.append(VOutA)
        #PMVoltages.append(VOutB)
        ##MVoltages.append(volt12)
        #PMVoltages.append(volt3V3)
        #PMCurrents.append(current)

        #For CUs
        CU3V3 = None
        CU12V = None
        CU12V_1 = None
        LM75Temp = None
        LM75Temp2 = None
        fan1 = None
        fan2 = None
        fan3 = None
        fan4 = None
        fan5 = None
        fan6 = None

        #dataCU = getCUData(i)
        #if dataCU == -1:
        #    print "CU error"
        #else:
        #    for item in dataCU:
        #        if "+3.3V" in item:
        #            CU3V3 = item.strip().split(" ")[13]
        #        elif "+12V " in item:
        #            CU12V = item.strip().split(" ")[14]
        #        elif "+12V_1" in item:
        #            CU12V_1 = item.strip().split(" ")[12]
         #       elif "LM75 Temp " in item:
         ##           LM75Temp = item.strip().split(" ")[10]
          #      elif "LM75 Temp2" in item:
         #           LM75Temp2 = item.strip().split(" ")[9]
         ##       elif "Fan 1" in item:
         #           fan1 = item.strip().split(" ")[14]
           #     elif "Fan 2" in item:
           #         fan2 = item.strip().split(" ")[14]
           #     elif "Fan 3" in item:
           #         fan3 = item.strip().split(" ")[14]
           #     elif "Fan 4" in item:
           #         fan4 = item.strip().split(" ")[14]
           #     elif "Fan 5" in item:
           #         fan5 = item.strip().split(" ")[14]
            #    elif "Fan 6" in item:
           #         fan6 = item.strip().split(" ")[14]
        #CUVoltages.append(CU3V3)
        #CUVoltages.append(CU12V)
        #CUVoltages.append(CU12V_1)
        #CUTemperatures.append(LM75Temp)
        #CUTemperatures.append(LM75Temp2)
        #fanSpeeds.append(fan1)
        #fanSpeeds.append(fan2)
        #fanSpeeds.append(fan3)
        #fanSpeeds.append(fan4)
        #fanSpeeds.append(fan5)
        #fanSpeeds.append(fan6)

    
    #for AMC13
    amc13data = getAMC13Data()
    if amc13data == -1:
        print "amc13 error"
    else:
        for item in amc13data:
            if "T2 Temp" in item:
                T2Temp = item.strip().split(" ")[19]
            elif "+12V" in item:
                amc13_12V = item.strip().split(" ")[21]
            elif "+3.3V" in item:
                amc13_3V3 = item.strip().split(" ")[20]
            elif "+1.2V" in item:
                amc13_1V2 = item.strip().split(" ")[20]

    def printData():
        print ''
        print "Data:"
        print ''
        print "MCH: [tempCPU, tempIO, volt1V2, volt1V8, volt2V5, volt3V3, volt12V, current]"
        print getMCHData(HOST)
        print ''
        print "PMTemperatures: [PM1 tbrick-a, PM1 tbrick-b, PM1 t-base, PM2 trick-a, PM2 tbrick-b, PM2, t-base]"
        print "              ", PMTemperatures
        print "PMVoltages: [PM1 VIN, PM1 VOutA, PM1 VOutB, PM1 12V, PM1 3.3V, PM2 VIN, PM2 VOutA, PM2 VOutB, PM2 12V, PM2 3.3V]"
        print "              ", PMVoltages
        print "PMCurrents: [PM1 Current(sum), PM2 current(sum)]"
        print "          ", PMCurrents
        print ''
        print "CUVoltages: [CU1 3.3V, CU1 12V, CU1 12V_1, CU2 3.3V, CU2 12V, CU2 12V_1]"
        print "            ", CUVoltages
        print "CUTemperatures: [CU1 LM75Temp, CU1 LM75Temp2, CU2 LM75Temp, CU2 LM75Temp2]"
        print "             ", CUTemperatures
        print "fanSpeeds: [CU1 fan1, CU1 fan2, CU1 fan3, CU1 fan4, CU1 fan5, CU1 fan6, CU2 fan1, CU2 fan2, CU3 fan3, C21 fan4, CU2 fan5, CU2 fan6]"
        print "           ", fanSpeeds
        print ''
        print "AMC13: [T2Temp, 12V, 3.3V, 1.2V]"
        print "       ", [T2Temp, amc13_12V, amc13_3V3, amc13_1V2]
        print ''
    
    #printData()
        
    #if everything is fine
    sys.exit(0)

    
