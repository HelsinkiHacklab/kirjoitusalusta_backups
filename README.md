# Backups of our pads from kirjoitusalusta.fi

It seems the future of this great service is not 100% certain, so we dumped backups here.

A small script to automate the dumping is included. Needs Beautiful Soup, version 4 of course preferred but we do  very simple things so version 3 should manage.

     sudo apt-get install python-bs4

Then just run 

    ./dump.py

It will make sure your checkout is up-to date and dumps all the stuff then commits it and will attempt to push the changed back as well
