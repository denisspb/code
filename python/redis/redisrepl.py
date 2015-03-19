#!/usr/bin/python
#

import sys
import threading
import redis


if (len(sys.argv) == 3): 
    serverMaster = str(sys.argv[1])
    port = int(sys.argv[2])
    serverSlave = str(sys.argv[3])

    rserver = redis.Redis(server, port)
    rserver.slaveof(serverMaster, port)

    print "Done" 
else
    print "Wrong params" 


    

