#!/usr/bin/env python

# get credentials from conf file
import sys
import re

inFileName = 'dbdu.conf'

if len(sys.argv) > 1:
    inFileName = str(sys.argv[1])

with open(inFileName) as f:
    lines = f.read().splitlines()

sections = []
passes = dict()

passesuniq = dict()
passesuniq_index = 0

diffpassinsec = []

ignoresections = ["[.common]", "[sharded_application]"]

ignoreconfsec = ["<qe-pod4101>","<devvm>","<pod4201>","<staging>","<feature01>","<test>", "<chaos>", "<min-db>", "<endpoint-test>", "<endpoint-test-automation>", "<endpoint-test-mmorearty>"]

is_section_re = re.compile(ur'^\s*\[(.*)\]\s*$')
is_dsn_re = re.compile(ur'^(;)?\s*dsn(<[\w_-]+>)?\s*=\s*(.*)$')
dsn_re = re.compile(ur'^\"mysql://(?:(?:(.*):)?(.*)@)?(.*)/(.*)\"$')

currentsection = ""

perconfsetcreds = dict()

noconfsetlines = []

dnsinsec = dict()

for line in lines:
    if is_section_re.match(line):
        sections.append(line)
        currentsection = line
        dnsinsec[currentsection] = []
    else:
        if currentsection not in ignoresections:
            is_dsn = is_dsn_re.match(line)
            if is_dsn:
                confset = is_dsn.group(2)
                if confset:
                    if (confset not in ignoreconfsec):
                        dsn = dsn_re.match(is_dsn.group(3))
                        if dsn:
                            #print line
                            server = dsn.group(3)
                            schema = dsn.group(4)
                            dnsstr = server + "/" + schema
                            if dnsstr not in dnsinsec[currentsection]:
                                dnsinsec[currentsection].append(dnsstr)

                        else:
                            raise ValueError("ERROR: error for line " + line)
                else:
                    noconfsetlines.append(line)

for sec_i in dnsinsec:
    if len(dnsinsec[sec_i]) > 1:
        print sec_i
        for dns_i in dnsinsec[sec_i]:
            print(dns_i)
        print ""


