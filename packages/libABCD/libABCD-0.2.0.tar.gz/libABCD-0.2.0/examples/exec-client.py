#!/usr/bin/env python3

import libABCD
import time
import sys

def myexec(data,con):
    libABCD.logger.info("Got an exec command: {}".format(data))
    try:
        toexec=data["py"]
        exec(toexec)
    except Exception as e:
        pass

libABCD.add_handler("exec",myexec)

name="exec-client"
if len(sys.argv)>1:
    name=sys.argv[1]
libABCD.init(name)

try:
    while True:
        libABCD.handle(1) # 1 second timeout
        # here goes the client code
except: # here catching also Interrupt and kill
    libABCD.die()
