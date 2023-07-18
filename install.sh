#!/bin/bash

cd ~
go install github.com/lc/subjs@latest
go install github.com/tomnomnom/httprobe@latest
go install github.com/0xsha/GoLinkFinder@latest
mkdir .gf
go install github.com/tomnomnom/qsreplace@latest
go install github.com/tomnomnom/gf@latest
go install github.com/0xsha/GoLinkFinder@latest
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
git clone https://github.com/1ndianl33t/Gf-Patterns
git clone https://github.com/tomnomnom/gf.git
mv gf/examples/*.json ~/.gf
mv Gf-Patterns/*.json ~/.gf
rm -rf gf
rm -rf Gf-Patterns
pip3 install pytenable
pip3 install python-Levenshtein
pip3 install aiohttp
pip3 install asyncio
pip3 install termcolor
pip3 install openpyxl
