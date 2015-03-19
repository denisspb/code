#!/usr/bin/python
# fills memcached with object of size 'datasize' and keys aXXX (a1...a'writeiterations')
# 
# time python mccpuloadtest.py 

import sys
import hashlib
import threading
import memcache
import random
import time
import datetime


server = 'dsamoylov2:11211'
num_servers = 1
writeiterations = 1000
readiterations =  15000
datasize = 300000
writethreadscount = 10
readthreadscount = 10

 
if (len(sys.argv) > 1):
	server = str(sys.argv[1])

if (len(sys.argv) > 2):
	num_servers = int(sys.argv[2])

if (len(sys.argv) > 3):
	writeiterations = int(sys.argv[3])

if (len(sys.argv) > 4):
	readiterations = int(sys.argv[4])

if (len(sys.argv) > 5):
	readthreadscount = int(sys.argv[5])

if (len(sys.argv) > 6):
	writethreadscount = int(sys.argv[6])

if (len(sys.argv) > 7):
	datasize = int(sys.argv[7])

string_val = "x" * (datasize - 6)
string_val = "000" + string_val + "999"

mc_server1 = memcache.Client([server], debug=0)

mc_server1.set("den", "mc_xxx_data" + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
print mc_server1.get("den")

for j in range(writeiterations):
	mc_server1.set("a" + str(j), string_val)


print("DONE")