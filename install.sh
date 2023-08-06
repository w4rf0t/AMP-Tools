#!/bin/bash

cd ~
pip3 install -r requirements.txt

go install github.com/lc/subjs@latest
go install github.com/tomnomnom/httprobe@latest
go install github.com/0xsha/GoLinkFinder@latest
mkdir .gf
go install github.com/tomnomnom/qsreplace@latest
go install github.com/tomnomnom/gf@latest
go install github.com/0xsha/GoLinkFinder@latest
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/bp0lr/gauplus@latest
git clone https://github.com/1ndianl33t/Gf-Patterns
git clone https://github.com/tomnomnom/gf.git
mv gf/examples/*.json ~/.gf
mv Gf-Patterns/*.json ~/.gf
rm -rf gf
rm -rf Gf-Patterns

if [[ -f ~/.zshrc ]]; then
    # Thêm các dòng vào tệp .zshrc
    echo 'export PATH=~/.local/bin:$PATH' >> ~/.zshrc
    echo 'export GOPATH=...' >> ~/.zshrc
    source ~/.zshrc
    echo "Cập nhật và source ~/.zshrc thành công!"
fi

if [[ -f ~/.bashrc ]]; then
    # Thêm các dòng vào tệp .bashrc
    echo 'export PATH=~/.local/bin:$PATH' >> ~/.bashrc
    echo 'export GOPATH=...' >> ~/.bashrc
    source ~/.bashrc
    echo "Cập nhật và source ~/.bashrc thành công!"
fi

