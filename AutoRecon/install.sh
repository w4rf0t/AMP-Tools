#!/bin/bash

cd ~
git clone https://github.com/shmilylty/OneForAll.git; cd OneForAll; pip3 install -r requirements.txt; 
git clone https://github.com/guelfoweb/knock.git; cd knock; pip3 install -r requirements.txt; 
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/tomnomnom/waybackurls@latest
$ GO111MODULE=on go get -u -v github.com/lc/subjs@latest
go install github.com/tomnomnom/qsreplace@latest
go get -u github.com/tomnomnom/gf
echo 'source $GOPATH/src/github.com/tomnomnom/gf/gf-completion.bash' >> ~/.bashrc
cp -r $GOPATH/src/github.com/tomnomnom/gf/examples ~/.gf
pip3 install -r requirements.txt
