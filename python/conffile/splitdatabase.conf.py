#!/usr/bin/env python

import sys
import re


inFileName = 'dbdu.conf'

if len(sys.argv) > 1:
    inFileName = str(sys.argv[1])

with open(inFileName) as f:
    lines = f.read().splitlines()

currentsection = ""
credentialscommonkey = "[common]"
phyapplicationkey = "[application]"

logicalfile_data = {}
physicalfile_data = {}
physicalfile_slavesdata = {}
credentialsfile_data = {credentialscommonkey: {}}

logicalfile_sections = {"[.common]", "[sharded_application]", "[migrations]"}
nonpersonal_confsets = {"<qe-pod4101>", "<devvm>", "<pod4201>", "<staging>", "<feature01>", "<test>", "<chaos>",
                        "<min-db>", "<endpoint-test>", "<endpoint-test-automation>", "<endpoint-test-mmorearty>"}

is_section_re = re.compile(ur'^\s*\[(.*)\]\s*$')
is_dsn_re = re.compile(ur'^(;)?\s*dsn(<[\w_-]+>)?\s*=\s*(.*)$')
dsn_re = re.compile(ur'^\"mysql://(?:(?:(.*):)?(.*)@)?(.*)/(.*)\"$')
is_ro_slave_list_re = re.compile(ur'^\s*ro_slave_list_')

for line in lines:
    if is_section_re.match(line):
        currentsection = line
        if currentsection in logicalfile_sections:
            logicalfile_data[currentsection] = []
        else:
            physicalfile_data[currentsection] = set()
            physicalfile_slavesdata[currentsection] = set()
            credentialsfile_data[currentsection] = {}

    else:
        if currentsection in logicalfile_sections:
            logicalfile_data[currentsection].append(line)
        else:
            is_dsn = is_dsn_re.match(line)

            if is_dsn:
                dsn = dsn_re.match(is_dsn.group(3))
                if dsn:
                    server = dsn.group(3)
                    schema = dsn.group(4)
                    serverline = "mysql://username:password@" + server + "/" + schema

                    username = dsn.group(1)
                    passwordOrusername = dsn.group(2)
                    if username:
                        credentialsline = username + ":" + passwordOrusername
                    else:
                        credentialsline = passwordOrusername
                else:
                    raise ValueError("ERROR: dsn line expected, error for line " + line)

                confset = is_dsn.group(2)

                if confset:
                    # if dsn has confset from non-personal group
                    #   keep this confset and create credenetials with such confset
                    # if not - strip confset from dsn and create credentials with such confset in common section
                    if confset in nonpersonal_confsets:
                        # per section credentials
                        credentialslinekey = "credentials" + confset + " = "
                        credentialsfile_data[currentsection][credentialslinekey] = credentialsline

                        serverline = "dsn" + confset + " = " + serverline
                    else:
                        # personal confset
                        # for personal confset we do assumption that only one password is used everywhere
                        credentialslinekey = "credentials" + confset + " = "

                        if credentialslinekey not in credentialsfile_data[credentialscommonkey]:
                            credentialsfile_data[credentialscommonkey][credentialslinekey] = credentialsline
                        else:
                            existingcredentialsline = credentialsfile_data[credentialscommonkey][credentialslinekey]

                            if existingcredentialsline != credentialsline:
                                raise ValueError("ERROR: credentails conflict " + line)

                        # strip confset from personal dns as all are the same
                        serverline = "dsn = " + serverline
                        # else:
                        # live file
                        # TODO

                physicalfile_data[currentsection].add(serverline)
            else:
                is_ro_slave_list = is_ro_slave_list_re.match(line)
                if is_ro_slave_list:
                    physicalfile_slavesdata[currentsection].add(line)


# save to files
# logicalfile
savefile = open('database_logical.conf', 'w')
for section in logicalfile_data:
    savefile.write(section + '\n')
    for ln in logicalfile_data[section]:
        savefile.write(ln + '\n')
    savefile.write("" + '\n')

savefile.close()


# physicalfile
# store [application] first
savefile = open('database_physical.conf', 'w')

savefile.write(phyapplicationkey + '\n')
lns = sorted(physicalfile_data[phyapplicationkey])
for ln in lns:
    savefile.write(ln + '\n')

if len(physicalfile_slavesdata[phyapplicationkey]) > 0:
    savefile.write("" + '\n')
    lns = sorted(physicalfile_slavesdata[phyapplicationkey])
    for ln in lns:
        savefile.write(ln + '\n')

savefile.write("" + '\n')

srtd = sorted(physicalfile_data)
for section in srtd:
    if section != phyapplicationkey:
        if len(physicalfile_data[section]) > 0:
            savefile.write(section + '\n')
            lns = sorted(physicalfile_data[section])
            for ln in lns:
                savefile.write(ln + '\n')

            if len(physicalfile_slavesdata[section]) > 0:
                savefile.write("" + '\n')
                lns = sorted(physicalfile_slavesdata[section])
                for ln in lns:
                    savefile.write(ln + '\n')

            savefile.write("" + '\n')
        else:
            print "WARNING: empty physical section:" + section

savefile.close()

# credentialsfile
# store [common] first
savefile = open('database_credentials.conf', 'w')
savefile.write(credentialscommonkey + '\n')
srtd = sorted(credentialsfile_data[credentialscommonkey])
for credentialskey in srtd:
    credentialsvalue = str(credentialsfile_data[credentialscommonkey][credentialskey])
    savefile.write(credentialskey + credentialsvalue + '\n')
savefile.write("" + '\n')


srtd = sorted(credentialsfile_data)
for section in srtd:
    if section != credentialscommonkey:
        if len(credentialsfile_data[section]) > 0:
            savefile.write(section + '\n')
            srtdCreds = sorted(credentialsfile_data[section])
            for credentialskey in srtdCreds:
                credentialsvalue = str(credentialsfile_data[section][credentialskey])
                savefile.write(credentialskey + credentialsvalue + '\n')
            savefile.write("" + '\n')
        else:
            print "WARNING: empty credential section:" + section

savefile.close()
