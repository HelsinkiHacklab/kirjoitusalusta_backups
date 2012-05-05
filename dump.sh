#!/bin/bash -ex
wget --no-check-certificate -q -O /dev/stdout http://kirjoitusalusta.fi/ep/pad/export/hacklab/latest?format=html | sed -r -e "s%\"https?://kirjoitusalusta.fi/([^\"]+)\"%\"http://kirjoitusalusta.fi/ep/pad/export/\1/latest?format=html\"%g"  >hacklab/latest\?format\=html.html
wget -nH --cut-dirs=3 -E -k -r -np --force-html --no-check-certificate --base=http://kirjoitusalusta.fi --input-file hacklab/latest\?format\=html.html

