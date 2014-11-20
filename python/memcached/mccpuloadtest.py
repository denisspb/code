#!/usr/bin/python
#
# time python mccpuloadtest.py 

import sys
import hashlib
import threading
import memcache
import random
import time

class mySetThread (threading.Thread):
	def __init__(self, threadId, name):
		threading.Thread.__init__(self)
		self.threadID = threadId
		self.name = name        

	def run(self):
		print "Starting " + self.name
		do_mc_set(self.threadID, writeiterations, )

class myGetThread (threading.Thread):
	def __init__(self, threadId, name):
		threading.Thread.__init__(self)
		self.threadID = threadId
		self.name = name        

	def run(self):
		print "Starting " + self.name
		do_mc_get(self.threadID, readiterations)

def do_mc_set(threadId, iterations):
	mc_server = memcache.Client([server], debug=0)

	keyPrefix = "test_key_" + str(threadId) + "_"

	for i in range(iterations): 
		id = currentItem[threadId]
		key = keyPrefix + str(id)

		data = string_val if (datasize > 0) else str(i)

		serverId = abs(hash(key)) % (num_servers)
		mc_server.set(key, data)

		currentItem[threadId] = id + 1

	print("SET %d done." % threadId)

def do_mc_get(threadId, iterations):
	mc_server = memcache.Client([server], debug=0)

	for i in range(iterations): 
		backetId = random.randrange(0, writethreadscount)
		maxId = currentItem[backetId]
		id = random.randrange(0, maxId)
		keyPrefix = "test_key_" + str(backetId) + "_"
		key = keyPrefix + str(id)

		serverId = abs(hash(key)) % (num_servers)
		mc_server.get(key)

	print("GET %d done." % threadId)

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
	readiterations = int(sys.argv[4])

if (len(sys.argv) > 5):
	readthreadscount = int(sys.argv[5])

if (len(sys.argv) > 6):
	writethreadscount = int(sys.argv[6])

if (len(sys.argv) > 7):
	datasize = int(sys.argv[7])

string_val = "x" * datasize

mc_server1 = memcache.Client([server], debug=0)

mc_server1.set("den", "xxx_data")
print mc_server1.get("den")

# precreate initial items
currentItem = []
for i in range(writethreadscount):
	currentItem.append(0)
	do_mc_set(i, 1)	

start_time = time.time()

# Create threads
threads = []
for j in range(writethreadscount):
	name = "Thread-SET-" + str(j)
	mythread = mySetThread(j, name)
	mythread.start()
	threads.append(mythread)

for j in range(readthreadscount):
	name = "Thread-GET-" + str(j)
	mythread = myGetThread(j, name)
	mythread.start()
	threads.append(mythread)

# Wait for all threads to complete
for t in threads:
    t.join()
    
print "Exiting Main Thread"

print("MC --- %s seconds ---" % (time.time() - start_time))
