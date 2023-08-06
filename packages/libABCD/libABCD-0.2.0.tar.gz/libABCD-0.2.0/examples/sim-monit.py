#!/usr/bin/env python3

import libABCD
import time
import random

def monitreq(data,con):
    msg={}
    msg["cmd"]="monit"
    msg["time"]=time.time()
    msg["val1"]=3+random.random()*2
    msg["val2"]=3+random.random()*2
    msg["val3"]=-3+random.random()*2
    msg["val4"]=-3+random.random()*2
    libABCD.publish("@to/monit",payload=msg)

libABCD.add_handler("monitreq",monitreq)

libABCD.init("sim-monit")

try:
    while True:
        libABCD.handle(1) # 1 second timeout
        # here goes the client code
except: # here catching also Interrupt and kill
    libABCD.die()
