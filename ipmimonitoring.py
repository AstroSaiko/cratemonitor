#!/usr/bin/env python 

import subprocess
import sys
import os
import signal
import time


line = []
proc = subprocess.Popen(("ipmitool -H mch-e1a04-18 -P '' -T 0x82 -b 7 -B 0 -t 0xc2 sdr").split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
#while True:
#    out = proc.stdout.read(1)
#    if out == '' and not proc.poll() == None:
#        break
#    if out != '':
#        sys.stdout.write(out)
#        sys.stdout.flush()

(out, err) = proc.communicate()
print out
if err != '':
    print err

