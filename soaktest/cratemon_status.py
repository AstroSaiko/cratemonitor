#!/usr/bin/env python

###############################################################################

import os
import socket
import sys

import pdb
import rrdtool

###############################################################################

if __name__ == "__main__":

    for crate in ['s1g04-18','s1g04-27','s1g04-36','s1g04-45']:
        print "mch-{0}.rrd".format(crate)
        ret = rrdtool.fetch("mch-{0}.rrd".format(crate), "AVERAGE", "-s -2min")
        print ret

        
		
			
