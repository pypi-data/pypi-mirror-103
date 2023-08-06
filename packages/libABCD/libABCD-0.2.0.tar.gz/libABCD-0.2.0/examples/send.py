#!/usr/bin/env python3

import selectors
import socket

import libABCD
import time
import json
import sys
import logging

if len(sys.argv)<2:
    print("Syntax: {} 'msg'".format(sys.argv[0]))
    print("  message must be a correctly formatted JSON string")

libABCD.init("send",loglevel=logging.WARNING)
libABCD.addmessage(sys.argv[1])
libABCD.handle(1)
