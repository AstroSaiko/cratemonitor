#!/bin/env python

import uhal
import sys

def fmcPresent(hostname):
    uhal.setLogLevelTo( uhal.LogLevel.WARNING)
    manager = uhal.ConnectionManager("file://FEDconnection.xml")
    try:
        fed = manager.getDevice(hostname)
    except:
        print "Could not connect to {0}".format(hostname)
        return False 
    device_id = fed.id()
    
    # Read the value back.                                                                                                       
    # NB: the reg variable below is a uHAL "ValWord", not just a simple integer   
    fmc_l8_present = fed.getNode("status.fmc_l8_present").read()

    # Send IPbus transactions                                                                                                  
    fed.dispatch()

    # Return status
    if hex(fmc_l8_present) == '0x1':
        return True
    else:
        return False

if __name__ == '__main__':

    print fmcPresent(sys.argv[1])
