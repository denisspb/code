#!/usr/bin/python
#
# python mcsimple.py

import sys
import memcache

server = 'localhost:11211'
iterations = 100
datasize = 100

 
mc_server = memcache.Client([server], debug=0)

mc_server.set("den", "xxx_data")
print mc_server.get("den")

print 'done'