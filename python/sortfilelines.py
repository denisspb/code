#!/usr/bin/env python
# Model load


import os
import sys

inFileName = 'ap1.txt'
outFileName = '_ap1.txt'

if (len(sys.argv) > 1):
    inFileName = str(sys.argv[1])

if (len(sys.argv) > 2):
    outFileName = str(sys.argv[2])

with open(inFileName) as f:
    lines = f.read().splitlines()

getList = []

for item in lines:
    stip = item[4:]
    if (stip[:3] == "get"):
        getList.append(stip[5:])

# lines = [(item[8:]) for item in lines]

getList.sort()


fSorted = open(outFileName, 'w')

for item in getList:
  fSorted.write("%s\n" % item)