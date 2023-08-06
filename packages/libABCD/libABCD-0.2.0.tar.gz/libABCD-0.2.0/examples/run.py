#!/usr/bin/env python3

import libABCD
import time
import sys
import json
import shlex,subprocess

if len(sys.argv)<2:
    config="dm2.json"
else:
    config="{}.json".format(sys.argv[1])

def loadconfig(data="",topic=""):
    global processes
    try:
        jsonconfig=json.load(open(config))
        processes={**jsonconfig["run"],**processes}
        libABCD.logger.info("Going to survey and run: {}".format(" ".join(processes)))
        for proc in processes:
            if "time" not in processes[proc]:
                processes[proc]["time"]=time.time()
    except Exception as e:
        print("Error {}. Couldn't JSON parse {} file, quitting".format(e,config))
        sys.exit()

def status(data,topic):
    proc=data["from"]
    libABCD.logger.info("Got new status: {}".format(data))
    if proc in processes:
        processes[proc]["on"]=data["on"]
        if data["on"]:
            processes[proc]["time"]=data["time"]
        else:
            processes[proc]["time"]=time.time()

    return

def checkprocesses():
    for proc in processes:
        if "on" not in processes[proc]:
            processes[proc]["on"]=0
        if processes[proc]["on"]:
            # proc is up
            libABCD.logger.debug("{} is up and running :)".format(proc))
        else:
            # proc is down, start it if it has been down for more than 10 sec
            if time.time()-processes[proc]["time"]>10:
                libABCD.logger.info("{} has been down for {} sec, running {}".format(proc,time.time()-processes[proc]["time"],processes[proc]["cmd"]))
                cmd="screen -dmS {} {}".format(proc,processes[proc]["cmd"])
                try:
                    cmd="ssh {} screen -dmS {} {}".format(processes[proc]["host"],proc,processes[proc]["cmd"])
                except:
                    pass
                args=shlex.split(cmd)
                subprocess.Popen(args)

libABCD.add_handler("reload",loadconfig)
libABCD.add_handler("_default",status)

libABCD.init("run")

processes={}
loadconfig()

libABCD.subscribe("@status/#")

try:
    while True:
        libABCD.handle()
        checkprocesses()
except: # here catching also Interrupt and kill
    libABCD.die()
