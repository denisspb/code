#!/usr/bin/python
#
# time python cpuloadtest.py 

import sys
import hashlib
import threading
import redis
import random
import time

class mySetThread (threading.Thread):
	def __init__(self, threadId, name):
		threading.Thread.__init__(self)
		self.threadID = threadId
		self.name = name        

	def run(self):
		print "Starting " + self.name
		do_redis_set(self.threadID, writeiterations)

def do_redis_set(threadId, iterations):
	rserver = []
	for i in range(num_servers):
		rserver.append(i)

	for i in range(iterations): 
		id = currentItem[threadId]		

		rserver[serverId].set(key, data)

		rserver[0] = threadId

	print("SET %d done. value %d" % threadId, rserver[0])


server = 'localhost'
num_servers = 1
writeiterations = 10000
readiterations =  15000
datasize = 383
writethreadscount = 10
readthreadscount = 10

string_val = "x" * datasize

# Create threads
threads = []
for j in range(writethreadscount):
	name = "Thread-SET-" + str(j)
	mythread = mySetThread(j, name)
	mythread.start()
	threads.append(mythread)

# Wait for all threads to complete
for t in threads:
    t.join()
    
print "Exiting Main Thread"

print("--- %s seconds ---" % (time.time() - start_time))
