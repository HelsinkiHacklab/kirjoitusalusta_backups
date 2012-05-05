#!/bin/bash -x
wget -E --no-check-certificate -q -O /dev/stdout http://kirjoitusalusta.fi/ep/pad/export/hacklab/latest?format=html | sed -r -e "s%\"https?://kirjoitusalusta.fi/([^\"]+)\"%\"http://kirjoitusalusta.fi/ep/pad/export/\1/latest?format=html\"%g"  >hacklab/latest\?format\=html.html
wget -nH --cut-dirs=3 -E -k -r -np --force-html --no-check-certificate --base=http://kirjoitusalusta.fi --input-file hacklab/latest\?format\=html.html

# rename the dumped files
for file in $( find . -name '*.html' | grep 'latest' )
do
    mv -f "$file" `echo "$file" | sed -r -e "s%/latest.*\.html%.html%g"`
    rmdir `echo "$file" | sed -r -e "s%/latest.*\.html%/%g"`
done

# and rewrite the links in hacklab.html to point to the renamed files
sed -i -r -e "s%http://kirjoitusalusta.fi/ep/pad/export/([^/]+)/latest\?format=html%\1.html%g" hacklab.html

# Autocommit
git add hacklab*.html
git commit -m 'dumped with script'
