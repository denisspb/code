#!/usr/bin/env python
# Memcached TCollector
# find all instances running locally, and dump stats to STDOUT in Open TSDB format
# Additional logging for slab specific info such as key age

import logging
import os
import re
import socket
import time
from optparse import OptionParser

def main(options, instance):
	# Connect to a single instance of memcached and get the stats
	timestamp = time.mktime(time.localtime())
	hostname = instance[0]
	port = instance[1]

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
	logging.debug("Connecting to %s:%s" % ( hostname, port ))
	s.settimeout(5)
	s.connect((hostname, port))
	s.send("stats items\n")

	stats = ''
	while True:
		buf = s.recv(32768)
		logging.debug(buf)
		if not buf: break
		stats += buf
		if "END\r\n" in stats: break
	s.close()

	for line in stats.splitlines():
		if line != "END":
			fields = line.split(':')
			slab = fields[1]
			line = re.sub(r':\d+:',r'.',line)
			tokens = line.split(' ')
			tokens.append(slab)
			if len(tokens) == 4 and tokens[1] != 'version':
				print "%s.%s %d %s slab=%s port=%d" % ( 'mc', tokens[1], int(timestamp), tokens[2], tokens[3], port)

def discover_instances():
	# create a list of all host,port combinations running locally
	host = socket.gethostname()
	instances = []
	for x in os.popen('ps h -eo pid:1,command | grep memcached'):
		tokens = x.split(' ',2)
		if tokens[1] == '/box/bin/memcached' or tokens[1] == '/usr/bin/memcached' or tokens[1] == 'memcached' :
			match = re.findall("-p (\d+)",tokens[2])
			if len(match):
				instances.append( (host, int(match[0])) )
	return instances

if __name__ == '__main__':
	parser = OptionParser(usage="usage: %prog [options]")
	parser.add_option("--log", dest="log", help="Set the logging level", default='INFO')
	(options, args) = parser.parse_args()

	logging.basicConfig(level=getattr( logging, options.log.upper()),
		datefmt='%Y-%m-%d %H:%M:%S',
                format='%(asctime)s %(levelname)s: %(message)s')

	instances = discover_instances()
	logging.debug(instances)

	for i in instances:
		main(options, i)

