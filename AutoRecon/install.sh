#!/bin/bash

cd ~
mkdir tool; cd tool
git clone https://github.com/shmilylty/OneForAll.git; cd OneForAll; pip3 install -r requirements.txt; 
cd ~/tool
git clone https://github.com/guelfoweb/knock.git; cd knock; pip3 install -r requirements.txt; 
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
pip3 install -r requirements.txt
