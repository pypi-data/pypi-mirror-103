# generic use functions
from .init import init
from .handling import add_handler
from .parse import parsemsg
from .network import setserver,connect,close,handle,addmessage,ignore,hasmessage,on_message,disconnect,subscribe,publish
from .logging import die,quiet,verbose,setstdout,setfilelog
from .watchdog import check,start
#internal functions
from .logging import _init_log_settings

###
# Logging in UTC
###
import logging
import time
logging.Formatter.converter = time.gmtime

# libABCD internal variables
name=__name__
logger=logging.getLogger(__name__)  # by default log as libABCD
cmd_switch={}

import selectors
network_info={}
network_info["host"]='localhost'
#network_info["port"]=9818
network_info["port"]=1883
network_info["selector"]=selectors.DefaultSelector()
network_info["isconnected"]=False
network_info["timeconnected"]=0
network_info["name"]="Unknown"
network_info["outgoing"]=[]
network_info["last_ping"]=time.time()

add_handler("_pong",ignore)
add_handler("_quiet",quiet)
add_handler("_verbose",verbose)

###
# logger init code
###
_init_log_settings(logger)

