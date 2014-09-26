#!/usr/bin/env python
# Model load
#
# python modelload.py <sizesfile> <countfile>
# <sizefile> is result of echo "stats slabs" | nc localhost 11211 | grep chunk_size 
# <countfile>  echo "stats items" | nc localhost 11211 | grep number

import os
import sys
import threading
import redis

def parseSizeLine( line, dic ):
	#STAT XY:chunk_size Z
	fields = line.split(':')
	slab = fields[0].split(' ')[1]
	size = fields[1].split(' ')[1]
	dic[slab] = size
	return

def loadSizes( fileName ):
	dic = {}
	ins = open(fileName, "r" )	
	for line in ins:
		parseSizeLine( line, dic )
	ins.close()
	return dic

def parseCountLine( line, dic ):
	#STAT items:XY:number Z
	fields = line.split(':')
	slab = fields[1]
	count = fields[2].split(' ')[1]
	dic[slab] = count
	return

def loadCount( fileName ):
	dic = {}
	ins = open(fileName, "r" )	
	for line in ins:
		parseCountLine( line, dic )
	ins.close()
	return dic

def debugPrint( dic1, dic2 ):
	print("Sizes:")
	for k,v in dic1.items():
	    print(k + " " + v)

	print("Count:")
	for k,v in dicCount.items():
	    print(k + " " + v)   

def fillRedis( r_server, slab, count, size ):
	string_val = "x" * (int(size) - 5) # -4 is to compensate key lenght (mc report full item size including key)
	for x in range(1, int(count)):
		r_server.set(slab + "-" + str(x), string_val)

sizesFile = 'sizefile.txt'
countFile = 'countfile.txt'
server = 'localhost'

if (len(sys.argv) > 1):
	sizesFile = str(sys.argv[1])

if (len(sys.argv) > 2):
	countFile = int(sys.argv[2])

if (len(sys.argv) > 3):
	server = str(sys.argv[3])

dicSizes = loadSizes(sizesFile)
dicCount = loadCount(countFile)

print ("connecting to server: %s" % server)
r_server = redis.Redis(server) 

for slab,count in dicCount.items():
	size = dicSizes.get(slab, -1)
	if size == -1:
		raise Exception("No size found for " + slab)
		
	print(slab + ":" + count + "size:" + size)
	fillRedis(r_server, slab, count, size)