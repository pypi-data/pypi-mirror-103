#!/usr/bin/env python3

import libABCD
import time
import json
import sys


def log(data,channel):
    libABCD.logger.info("{} - {}".format(channel,json.dumps(data))) # log all messages

libABCD.add_handler("_default",log)

printonly=False
if len(sys.argv)>1:
    if sys.argv[1] == "-h":
        print("run S.py to log all messages")
        print("running S.py <topic> makes it only listen to this topic and output everything to stdout")
        quit()
    printonly=True

if printonly:
    libABCD.init("printonly")
    libABCD.subscribe(sys.argv[1])
else:
    libABCD.init("Spy")
    libABCD.subscribe('#') # request all messages/listen to all topics

try:
    while True:
        libABCD.handle()
except: # here catching also Interrupt and kill
    libABCD.die()
