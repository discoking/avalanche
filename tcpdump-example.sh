#command to get VLAN IDs with tcpdump
tcpdump -n -i eth0 -e | grep vlan | awk '{print $11}';
