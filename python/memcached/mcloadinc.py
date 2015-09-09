#!/usr/bin/python
#
# time python mccpuloadtest.py 

import sys
import hashlib
import threading
import memcache
import random
import time
import datetime

class myIncThread (threading.Thread):
    def __init__(self, threadId, name):
        threading.Thread.__init__(self)
        self.threadID = threadId
        self.name = name        

    def run(self):
        print "Starting " + self.name
        do_mc_inc(self.threadID, writeiterations, )

def do_mc_inc(threadId, iterations):
    mc_server = memcache.Client([server], debug=0)    

    for i in range(iterations):         
        mc_server.incr(key)
        
    print("SET %d done." % threadId)


server = 'localhost:11211'
num_servers = 1
writeiterations = 10000
readiterations =  15000
datasize = 383
writethreadscount = 10
readthreadscount = 10

 
if (len(sys.argv) > 1):
    server = str(sys.argv[1])

if (len(sys.argv) > 2):
    num_servers = int(sys.argv[2])

if (len(sys.argv) > 3):
    writeiterations = int(sys.argv[3])

if (len(sys.argv) > 4):
    writethreadscount = int(sys.argv[4])

if (len(sys.argv) > 5):
    datasize = int(sys.argv[5])

key = "test_key_den"
mc_server1 = memcache.Client([server], debug=0)
mc_server1.set("den", "mc_xxx_data" + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
print mc_server1.get("den")

mc_server1.set(key, 0)

start_time = time.time()

# Create threads
threads = []
for j in range(writethreadscount):
    name = "Thread-SET-" + str(j)
    mythread = myIncThread(j, name)
    mythread.start()
    threads.append(mythread)

# Wait for all threads to complete
for t in threads:
    t.join()

print("MC --- %s seconds ---" % (time.time() - start_time))

print mc_server1.get(key)

print "Exiting Main Thread"