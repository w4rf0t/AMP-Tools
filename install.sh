#!/bin/bash

sudo apt install golang-go -y

git clone https://github.com/blechschmidt/massdns.git
cd massdns
make
make install
rm -rf ../massdns
go get github.com/michenriksen/gitrob
cd ~
export GOROOT=/usr/local/go
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH

go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/lc/subjs@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/tomnomnom/httprobe@latest
go install github.com/bp0lr/gauplus@latest
mkdir .gf
go install github.com/tomnomnom/qsreplace@latest
go install github.com/tomnomnom/gf@latest
git clone https://github.com/1ndianl33t/Gf-Patterns
mv Gf-Patterns/*.json ~/.gf
rm -rf Gf-Patterns

pip3 install pytenable
