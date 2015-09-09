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

is_section_re = re.compile(ur'^\s*\[(.*)\]\s*$')
is_dsn_re = re.compile(ur'^(;)?\s*dsn(<[\w_-]+>)?\s*=\s*(.*)$')
dsn_re = re.compile(ur'^\"mysql://(?:(?:(.*):)?(.*)@)?(.*)/(.*)\"$')

currentsection = ""

perconfsetcreds = dict()

for line in lines:
    if is_section_re.match(line):
        sections.append(line)
        currentsection = line
        passes[currentsection] = []
    else:
        if currentsection not in ignoresections:
            is_dsn = is_dsn_re.match(line)
            if is_dsn:
                confset = is_dsn.group(2)
                dsn = dsn_re.match(is_dsn.group(3))
                if dsn:
                    #print line
                    u = dsn.group(1)
                    p = dsn.group(2)
                    if u:
                        cred = u + ":" + p
                    else:
                        cred = p

                    if confset:
                        if confset not in perconfsetcreds:
                            perconfsetcreds[confset] = []

                        cspasses = perconfsetcreds[confset]
                        if cred not in cspasses:
                            perconfsetcreds[confset].append(cred)
                    else:
                        cred_ph = ""
                        if cred not in passesuniq:
                            cred_ph = "common_credentials" + str(passesuniq_index)
                            passesuniq[cred] = cred_ph
                            passesuniq_index += 1
                        else:
                            cred_ph = passesuniq[cred]

                        curpasses = passes[currentsection]

                        if len(curpasses) > 0:
                            if cred_ph not in curpasses:
                                diffpassinsec.append(currentsection)

                        passes[currentsection].append(cred_ph)
                else:
                    raise ValueError("ERROR: error for line " + line)


for perconfsetcreds_i in perconfsetcreds:
    if len(perconfsetcreds[perconfsetcreds_i]) > 1:
        print perconfsetcreds_i
        for creds_i in perconfsetcreds[perconfsetcreds_i]:
            print(creds_i)
        print ""



#for perconfsetcreds_i in perconfsetcreds:
#    print perconfsetcreds_i
#    for creds_i in perconfsetcreds[perconfsetcreds_i]:
#        print(creds_i)
#
#    print ""

#
#for diffpassinsec_i in dif
# fpassinsec:
#    print(diffpassinsec_i)
#
## if (len(diffpassinsec) > 0):
##    raise ValueError('ERROR: Above resousces have incorrect credentials')
#
#print "[common_credentials]"
#for passesuniq_i in passesuniq:
#    print(passesuniq[passesuniq_i] + "=" + passesuniq_i)
#
#print("")
#for section in sections:
#    secpas = passes[section]
#    if len(secpas) > 0:
#        print(section)
#        print("credentials=" + secpas[0])
#        print("")
#        # for pswd in secpas:
#        #    print("credentails=" + pswd)
#
#print("DONE")
#