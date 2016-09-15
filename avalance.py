#!/usr/bin/env python
#This script will discover the vlans on an 802.1Q trunk and print them
#Soon it will add interfaces, and do DHCP discovery and only works on Linux
#needs tcpdump installed

import StringIO
import sys
import shlex
import subprocess
cmd = "/usr/sbin/tcpdump -n -i eth0 -e"
args = shlex.split(cmd)
tcpdump = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print "Press CTRL-C to stop tcpdump"
output = StringIO.StringIO()
running = True
vlans = set()
while running:
    try:
        data = tcpdump.stdout.readline()
        if len(data):
	    packet = data.split()
	    if packet[5] == "802.1Q":
	#	print vlans
		vlanTag = packet[10].rstrip(',')
		vlanTag = int(vlanTag) 
		if vlanTag not in vlans:
			vlans.add(vlanTag)
			print "added VLAN " + str(vlanTag) 
        else:
            running = False
    except KeyboardInterrupt:
        tcpdump.kill()
        data = tcpdump.stdout.readline()
        running = False
