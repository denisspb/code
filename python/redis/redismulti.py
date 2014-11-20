#!/usr/bin/python
#
# simple script that send many set commands to server in several threads
#
# usage instructions for the script:
# python redismulti.py <servername> <num of iterations> <datasize> <numberOfThreads>
# example:
# python redismulti.py localhost 100 99 1
# python redismulti.py den-sever 100000 99 101
# 1) first param (den-server in my example) is redis server box
# 2) second param (100000) is number of set commands to do
# 3) third param (99) is size of data to send in bytes. can be valuable if you want to send large data. if 0 will send iteration number (i=0,1.. till number of set commands).
# 4) forth param (101) is number of parallel threads


import sys
import threading
import redis

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name        
    def run(self):
        print "Starting " + self.name
        do_redis(self.name)

def do_redis(threadName):
	print ("%s connecting to server: %s" % (threadName, server))

	rserver = redis.Redis(server) 

	keyPrefix = "load_key_" + threadName + "_"

	for i in range(iterations): 
		key = keyPrefix + str(i)

		data = string_val if (datasize > 0) else str(i)

		rserver.set(key, data)
		if (i % 10 == 0): 
			print("%s: %s" % (threadName, key))

	print("%s done." % threadName)


server = 'localhost'
iterations = 100
datasize = 100
threadscount = 2
 
if (len(sys.argv) > 1):
	server = str(sys.argv[1])

if (len(sys.argv) > 2):
	iterations = int(sys.argv[2])

if (len(sys.argv) > 3):
	datasize = int(sys.argv[3])

if (len(sys.argv) > 4):
	threadscount = int(sys.argv[4])


if (datasize > 0):
	string_val = "x" * datasize
	print ("using date value with size: %d" % datasize)
else:
	print 'using number as data value'

# Create threads
threads = []
for j in range(threadscount):
	name = "Thread-" + str(j)
	mythread = myThread(j, name)
	mythread.start()
	threads.append(mythread)

# Wait for all threads to complete
for t in threads:
    t.join()
    
print "Exiting Main Thread"	
