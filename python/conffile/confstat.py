#!/usr/bin/env python

import os
import sys

inFileName = 'db.conf'

if (len(sys.argv) > 1):
    inFileName = str(sys.argv[1])

with open(inFileName) as f:
    lines = f.read().splitlines()

sections = []
sectionkeys = set()

for line in lines:
    if (len(line) > 0):
        if (line[0] == "["):
            sections.append(line)
        else:
            if (line[0] != ";"):
                k = line.split('=')
                sectionkeys.add(k[0])

for section in sections:
    print(section)

#for sectionkey in sectionkeys:
#    print(sectionkey)

