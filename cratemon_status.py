#!/usr/bin/env python

###############################################################################

import os
import socket
import sys

import pdb
import rrdtool

###############################################################################

if __name__ == "__main__":

    for crate in ['mch01','mch02']:
        print "{0}.rrd".format(crate)
        ret = rrdtool.fetch("{0}.rrd".format(crate), "AVERAGE", "-s -2min")
        print ret

        
		
			
