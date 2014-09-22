#!/usr/bin/python
#
# simple script to send many set commands to memcached server (prints every 10th key to see progress)
# and does not check for errors
#
# you will need redis library:
# sudo yum install python-pip
# sudo pip-python install python-memcached

# usage instructions for the script:
# python mcload.py <servername> <num of iterations> <datasize>
# example:
# python mcload.py "den-server:11212" 100000 99

# 1) first param (den-server in my example) is memcached server box with port
# 2) second param (100000) is number of set commands to do
# 3) third param (99) is size of data to send in bytes. can be valuable if you want to send large data. if 0 will send iteration number (i=0,1.. till number of set commands). 


import sys
import memcache

server = 'localhost:11212'
iterations = 100
datasize = 100
 
if (len(sys.argv) > 1):
	server = str(sys.argv[1])

if (len(sys.argv) > 2):
	iterations = int(sys.argv[2])

if (len(sys.argv) > 3):
	datasize = int(sys.argv[3])

print ("connecting to server: %s" % server)

mc_server = memcache.Client([server], debug=0)

if (datasize > 0):
	string_val = "x" * datasize
	print ("using date value with size: %d" % datasize)
else:
	print 'using number as data value'

for i in range(iterations): 
	key = 'load_key_' + str(i)

	data = string_val if (datasize > 0) else str(i)

	mc_server.set(key, data)
	if (i % 10 == 0): 
		print key 

print 'done'