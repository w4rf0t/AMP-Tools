#!/bin/bash

cd ~
export GOPATH=~/go
export PATH=$GOPATH/bin:$(which go)/bin:$PATH

go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/lc/subjs@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/tomnomnom/httprobe@latest
go install github.com/bp0lr/gauplus@latest
go install github.com/0xsha/GoLinkFinder@latest
mkdir .gf
go install github.com/tomnomnom/qsreplace@latest
go install github.com/tomnomnom/gf@latest
git clone https://github.com/1ndianl33t/Gf-Patterns
mv Gf-Patterns/*.json ~/.gf
rm -rf Gf-Patterns
pip3 install pytenable
