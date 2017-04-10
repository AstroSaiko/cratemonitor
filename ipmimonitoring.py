#!/usr/bin/env python 

import subprocess
import sys
import os
import signal
import time

HOST = "mch-e1a04-18"

def getCrateInfo(mch_hostname):
    return 0

def getMCHData(mch_hostname):
    tempCPU = None
    tempIO = None
    volt1V5 = None
    volt1V8 = None
    volt2V5 = None
    volt3V3 = None
    volt12V = None
    current = None
    proc = subprocess.Popen(("ipmitool -H {0} -U admin -P admin sdr entity 194.97".format(mch_hostname)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    (data, err) = proc.communicate()
    if err != '':
        #if not "Get HPM.x Capabilities request failed, compcode = c9" in err:                                                                                                                                                              
        if err != "Get HPM.x Capabilities request failed, compcode = c9\n":
            print err
            return -1
    data = data.split('\n')
    if "NAT-MCH-MCMC" in data[0]:
        for item in data:
            if "Temp CPU" in item:
                tempCPU = item.strip().split(" ")[18]
            elif "Temp I/O" in item:
                tempIO = item.strip().split(" ")[18]
            elif "Base 1.2V" in item:
                volt1V2 = item.strip().split(" ")[17]
            elif "Base 1.5V" in item:
                volt1V5 = item.strip().split(" ")[17]
            elif "Base 1.8V" in item:
                volt1V8 = item.strip().split(" ")[17]
            elif "Base 2.5V" in item:
                volt2V5 = item.strip().split(" ")[17]
            elif "Base 3.3V" in item:
                volt3V3 = item.strip().split(" ")[17]
            elif "Base 12V" in item:
                volt12V = item.strip().split(" ")[18]
            elif "Base Current" in item:
                current = item.strip().split(" ")[14]
    return [tempCPU, tempIO, volt1V2, volt1V8, volt2V5, volt3V3, volt12V, current]
                           
def getPMData(slot):
    class PM:
        def __init__(self, PMIndex):
            self.PMIndex = PMIndex
            self.entity = "10.{0}".format(str(96 + self.PMIndex))
            self.tempA = None
            self.tempB = None
            self.tempBase = None
            self.VIN = None
            self.VOutA = None
            self.VOutB = None
            self.volt12 = None
            self.volt3V3 = None
            self.current = None
            self.getData()

        def getData(self):
            proc = subprocess.Popen(("ipmitool -H mch-e1a04-18 -U '' -P '' sdr entity {0}".format(self.entity)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
            (self.data, self.err) = proc.communicate()
            if self.err != '':
                #if not "Get HPM.x Capabilities request failed, compcode = c9" in err:                                                                                                                                                      
                if self.err != "Get HPM.x Capabilities request failed, compcode = c9\n":
                    print self.err
                    return -1
            self.data = self.data.split('\n')
            if "NAT-PM-DC840" in self.data[0]:
                print "hello!"

    PM1 = PM(1)
    PM2 = PM(2)
    PM3 = PM(3)
    PM4 = PM(4)

    if slot == 1:
        PM = "0xc2"
    elif slot == 2:
        PM = "0xc4"
    elif slot == 3:
        PM = "0xc6"
    elif slot == 4:
        PM = "0xc8"
    else:
        print "Please insert a valid slot (1-4)"
        return -1 
    proc = subprocess.Popen(("ipmitool -H mch-e1a04-18 -U '' -P '' -T 0x82 -b 7 -B 0 -t {0} sdr".format(PM)).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    (data, err) = proc.communicate()
    if err != '':
        #if not "Get HPM.x Capabilities request failed, compcode = c9" in err:
        if err != "Get HPM.x Capabilities request failed, compcode = c9\n":
            print err
            return -1
    data = data.split('\n')
    return data

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
        tempA = None
        tempB = None
        tempBase = None
        VIN = None
        VOutA = None
        VOutB = None
        current = None
        volt12 = None
        volt3V3 = None

        data = getPMData(i)
        if data == -1:
            print "Error or whatever"
        else:
            for item in data:
                #Temperatures
                if "TBrick-A" in item:
                    tempA = item.strip().split(" ")[10]
                elif "TBrick-B" in item:
                    tempB = item.strip().split(" ")[10]
                elif "T-Base" in item:
                    tempBase = item.strip().split(" ")[12]
                #Input Voltage
                elif "VIN" in item:
                    VIN = item.strip().split(" ")[15]
                #Output Voltage
                elif "VOUT-A" in item:   
                    VOutA = item.strip().split(" ")[12]
                    #print VOutA
                elif "VOUT-B" in item:                                                                                                            
                    VOutB = item.strip().split(" ")[12]
                    #print VOutB
                #12V
                elif "12V" in item:
                    volt12 = item.strip().split(" ")[15]
                    #print volt12
                #3.3V
                elif "3.3V" in item:
                    volt3V3 = item.strip().split(" ")[14]
                    #print volt3V3
                #Total utput current
                elif "Current(SUM)" in item:
                    current = item.strip().split(" ")[6]
                    #print current
                #print tempA
                #print tempB
        #print tempBase
        PMTemperatures.append(tempA)
        PMTemperatures.append(tempB)
        PMTemperatures.append(tempBase)
        PMVoltages.append(VIN)
        PMVoltages.append(VOutA)
        PMVoltages.append(VOutB)
        PMVoltages.append(volt12)
        PMVoltages.append(volt3V3)
        PMCurrents.append(current)

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

        dataCU = getCUData(i)
        if dataCU == -1:
            print "CU error"
        else:
            for item in dataCU:
                if "+3.3V" in item:
                    CU3V3 = item.strip().split(" ")[13]
                elif "+12V " in item:
                    CU12V = item.strip().split(" ")[14]
                elif "+12V_1" in item:
                    CU12V_1 = item.strip().split(" ")[12]
                elif "LM75 Temp " in item:
                    LM75Temp = item.strip().split(" ")[10]
                elif "LM75 Temp2" in item:
                    LM75Temp2 = item.strip().split(" ")[9]
                elif "Fan 1" in item:
                    fan1 = item.strip().split(" ")[14]
                elif "Fan 2" in item:
                    fan2 = item.strip().split(" ")[14]
                elif "Fan 3" in item:
                    fan3 = item.strip().split(" ")[14]
                elif "Fan 4" in item:
                    fan4 = item.strip().split(" ")[14]
                elif "Fan 5" in item:
                    fan5 = item.strip().split(" ")[14]
                elif "Fan 6" in item:
                    fan6 = item.strip().split(" ")[14]
        CUVoltages.append(CU3V3)
        CUVoltages.append(CU12V)
        CUVoltages.append(CU12V_1)
        CUTemperatures.append(LM75Temp)
        CUTemperatures.append(LM75Temp2)
        fanSpeeds.append(fan1)
        fanSpeeds.append(fan2)
        fanSpeeds.append(fan3)
        fanSpeeds.append(fan4)
        fanSpeeds.append(fan5)
        fanSpeeds.append(fan6)

    
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
    
    printData()
        
    #if everything is fine
    sys.exit(0)

    
