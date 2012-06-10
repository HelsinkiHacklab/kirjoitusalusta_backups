#!/bin/bash -x
WGET='wget -nH --cut-dirs=3 -E -k -r -np --force-html --no-check-certificate --base=http://kirjoitusalusta.fi --domains=kirjoitusalusta.fi'
# Make sure you have most recent version locally
git pull
# Dump the motherpad and follow links in it
mkdir hacklab
wget -E --no-check-certificate -q -O /dev/stdout http://kirjoitusalusta.fi/ep/pad/export/hacklab/latest?format=html | sed -r -e "s%\"https?://kirjoitusalusta.fi/([^\"]+)\"%\"http://kirjoitusalusta.fi/ep/pad/export/\1/latest?format=html\"%g"  >hacklab/latest\?format\=html.html
$WGET --input-file hacklab/latest\?format\=html.html

# Find links in child pads, dump them to single file and run wget again
echo >urllist.html
for file in $( find . -name '*.html' | grep -v urllist\.html )
do
    grep "kirjoitusalusta.fi" "$file" | sed -r -e "s%\"https?://kirjoitusalusta.fi/([^\"]+)\"%\"http://kirjoitusalusta.fi/ep/pad/export/\1/latest?format=html\"%g" >>urllist.html
done

$WGET --input-file urllist.html
rm urllist.html

# rename the dumped files
for file in $( find . -name '*.html' | grep 'latest' )
do
    mv -f "$file" `echo "$file" | sed -r -e "s%/latest.*\.html%.html%g"`
    rmdir `echo "$file" | sed -r -e "s%/latest.*\.html%/%g"`
done

# and rewrite the links in hacklab.html to point to the renamed files
sed -i -r -e "s%http://kirjoitusalusta.fi/ep/pad/export/([^/]+)/latest\?format=html%\1.html%g" hacklab.html

# and rewrite links in the other files too
for file in $( find . -name '*.html')
do
    sed -i -r -e "s%\"https?://kirjoitusalusta.fi/([^\"]+)\"%\"\1.html\"%g" "$file"
done

# Remove possibly generated .N.html files
rm *.1.html *.2.html *.3.html

# Autocommit
git add hacklab*.html "4x4-RBG-LED-Board--I2C-.html"
git commit -m 'dumped with script'
git push

