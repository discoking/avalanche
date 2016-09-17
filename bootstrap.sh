#!/bin/bash

sudo apt-get -y install vlan tcpdump
sudo modprobe 8021q
echo 8021q >> /etc/modules
git clone https://github.com/SpiderLabs/Responder.git
