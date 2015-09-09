#!/usr/bin/env python

# get credentials from conf file
import os
import sys
import re

inFileName = 'db.conf'

if (len(sys.argv) > 1):
    inFileName = str(sys.argv[1])

with open(inFileName) as f:
    lines = f.read().splitlines()

sections = []
passes = dict()

passesuniq = dict()
passesuniq_index = 0

diffpassinsec = []

is_section_re = re.compile(ur'^\s*\[(.*)\]\s*$')
is_dsn_re = re.compile(ur'^(;)?\s*dsn(<[\w_-]+>)?\s*=\s*(.*)$')
dsn_re = re.compile(ur'^\"mysql:\/\/(?:(?:(.*):)?(.*)@)?(.*)\/(.*)\"$')

currentsection = ""

for line in lines:
    if (is_section_re.match(line)):
        sections.append(line)
        currentsection = line
        passes[currentsection] = []
    else:
        is_dsn = is_dsn_re.match(line)
        if (is_dsn):
            dsn = dsn_re.match(is_dsn.group(3))
            if (dsn):
                cred = dsn.group(1) + ":" + dsn.group(2)
                cred_ph = ""
                if (not cred in passesuniq):
                    cred_ph = "common_credentials" + str(passesuniq_index)
                    passesuniq[cred] = cred_ph
                    passesuniq_index += 1
                else:
                    cred_ph = passesuniq[cred]

                curpasses = passes[currentsection]
                if (len(curpasses) > 0):
                    if (not cred_ph in curpasses):
                        diffpassinsec.append(currentsection)

                passes[currentsection].append(cred_ph)
            else:
                raise ValueError("ERROR: error for line " + line)

for diffpassinsec_i in diffpassinsec:
    print(diffpassinsec_i)

#if (len(diffpassinsec) > 0):
#    raise ValueError('ERROR: Above resousces have incorrect credentials')

print "[common_credentials]"
for passesuniq_i in passesuniq:
    print(passesuniq[passesuniq_i] + "=" +passesuniq_i)

print("")
for section in sections:
    secpas = passes[section]
    if (len(secpas) > 0):
        print(section)
        print("credentials=" + secpas[0])
        print("")
        #for pswd in secpas:
        #    print("credentails=" + pswd)

print("DONE")


