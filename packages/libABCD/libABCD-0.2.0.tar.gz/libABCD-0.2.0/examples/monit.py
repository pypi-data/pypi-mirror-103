#!/usr/bin/env python3

import libABCD
import time
import json


def monit(data,con):
    if "to" in data:
        data.pop("to")
    data.pop("cmd")
    with open("monit.json", "a") as outfile:
        print(json.dumps(data),file=outfile)

libABCD.add_handler("monit",monit)
libABCD.add_handler("monitreq",libABCD.ignore)

libABCD.init("monit")

last_req=time.time()-50 # first call after 10 sec
try:
    while True:
        libABCD.handle()
        if time.time()>last_req+60:
            libABCD.publish(topic="@broadcast",payload='{"cmd":"monitreq"}')
            last_req=time.time()
        # here goes the client code
except: # here catching also Interrupt and kill
    libABCD.die()
