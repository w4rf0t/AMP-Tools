#!/bin/bash

sudo apt install golang-go -y

git clone https://github.com/blechschmidt/massdns.git
cd massdns
make
make install
rm -rf ../massdns
sudo apt install python3-censys


cd ~
export GOROOT=/usr/lib/go
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH

go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/lc/subjs@latest
go install github.com/tomnomnom/waybackurls@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/tomnomnom/httprobe@latest
mkdir .gf
go install github.com/tomnomnom/qsreplace@latest
git clone https://github.com/tomnomnom/gf
git clone https://github.com/1ndianl33t/Gf-Patterns
mv gf/examples/* .gf
mv Gf-Patterns/*.json ~/.gf
rm -rf gf
rm -rf Gf-Patterns

