#!/usr/bin/python
#
# python redisperftest2.py 

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
        do_redis_set(self.threadID, writeiterations, )

class myGetThread (threading.Thread):
    def __init__(self, threadId, name):
        threading.Thread.__init__(self)
        self.threadID = threadId
        self.name = name        

    def run(self):
        do_redis_get(self.threadID, readiterations)

def do_redis_set(threadId, iterations):
    rserver = []
    for i in range(num_servers):
        rserver.append(redis.Redis(server, redisport + i))

    keyPrefix = "test_key_" + str(threadId) + "_"

    for i in range(iterations): 
        id = currentItem[threadId]
        key = keyPrefix + str(id)

        data = string_val if (datasize > 0) else str(i)

        serverId = abs(hash(key)) % (num_servers)
        rserver[serverId].set(key, data)

        currentItem[threadId] = id + 1

def do_redis_get(threadId, iterations):
    rserver = []
    for i in range(num_servers):
        rserver.append(redis.Redis(server, redisport + i))

    for i in range(iterations): 
        backetId = random.randrange(0, writethreadscount)
        maxId = currentItem[backetId]
        id = random.randrange(0, maxId)
        keyPrefix = "test_key_" + str(backetId) + "_"
        key = keyPrefix + str(id)

        serverId = abs(hash(key)) % (num_servers)
        rserver[serverId].get(key)


server = 'localhost'
num_servers = 1
writeiterations = 1000
readiterations =  1500
datasize = 383
writethreadscount = 3
readthreadscount = 3
redisport = 6379
 
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

redis1 = redis.Redis(server, redisport)

redis1.set("den", "xxx_data_redis!!!!" + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
print redis1.get("den")

# precreate initial items
currentItem = []
for i in range(writethreadscount):
    currentItem.append(0)
    do_redis_set(i, 1)  


for i in range(0, 1000):
    print("iteration: %d" % i)
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
    
    print("iteration %s seconds" % (time.time() - start_time))
    print(" ")

print "Exiting Main Thread"