#!/usr/bin/env python

###############################################################################

import os
import socket
import sys

import pdb
import rrdtool

###############################################################################

if __name__ == "__main__":

    for crate in ['s1e02-27','s1e02-18','s1e02-10','s1e03-36','s1e03-27','s1e03-18']:
        print "{0}.rrd".format(crate)
        ret = rrdtool.fetch("{0}.rrd".format(crate), "AVERAGE", "-s -2min")
        print ret

        
		
			
