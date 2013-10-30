#!/usr/bin/python
from __future__ import with_statement
import re, urllib2
from bs4 import BeautifulSoup

# Some configurable things
DEFAULT_ENTRY_URL = 'http://kirjoitusalusta.fi/hacklab'
ETHERPAD_BASE = 'http://kirjoitusalusta.fi/'
# How to extract the pad name from the pad url
PAD_NAME_RE = re.compile('^%s(?P<padname>[^/]+).*$' % ETHERPAD_BASE)
# How to form the HTML export URL, takes single %s where the pad name goes
PAD_EXPORT_URL_FORMAT = 'http://kirjoitusalusta.fi/ep/pad/export/%s/latest?format=html'
# By default recurse to any and all urls under this same etherpad instance
PAD_RECURSE_HREF_RE = re.compile('^%s' % ETHERPAD_BASE)
# Again takes single %s which is the pad name
PAD_EXPORT_FILENAME = '%s.html'

# pad url and export url example (as a reminder)
# http://kirjoitusalusta.fi/hacklab
# http://kirjoitusalusta.fi/ep/pad/export/hacklab/latest?format=html

class jobmanager:
    def __init__(self, entry_url):
        self.job_queue = [entry_url, ]
        self.seen_urls = { entry_url: True }
        self.fetcher = fetcher(ETHERPAD_BASE, self)

    def add_to_queue(self, url):
        """Add given URL to job queue unless it has previously been added there already"""
        if self.seen_urls.has_key(url):
            return False
        self.job_queue.append(url)
        self.seen_urls[url] = True
        return True

    def run(self):
        while(len(self.job_queue) > 0):
            url = self.job_queue.pop(0)
            self.fetcher.fetch(url)

class fetcher:
    """This will take a pad URL (under ETHERPAD_BASE) and dump it as HTML, then follow any links to same etherpad server and dump those as well"""
    def __init__(self, base, queuemanager):
        self.base = base
        # This is just a reference so we can push jobs to the queue
        self.queuemanager = queuemanager

    def fetch(self, pad_url):
        """This will fetch a single HTML export of a pad, add any other pads found in it to the job queue and rewrite links to local files"""
        m = PAD_NAME_RE.search(pad_url)
        if not m:
            return False
        pad_name = m.group('padname')
        htmlfile = PAD_EXPORT_FILENAME % pad_name
        export_url = PAD_EXPORT_URL_FORMAT % pad_name
        print "Fetching %s" % export_url
        try:
            fp = urllib2.urlopen(export_url)
        except urllib2.URLError,e:
            print "Failed to fetchs %s: %s" % (export_url, e)
            return False
        soup = BeautifulSoup(fp)
        
        recurse_links = = soup.find_all('a', href=PAD_RECURSE_HREF_RE)
        for tag in recurse_links:
            # Doublecheck the url is sane pad
            new_pad_url = tag['href']
            m2 = PAD_NAME_RE.search(new_pad_url)
            if not m2:
                continue
            new_pad_name = m2.group('padname')
            new_htmlfile = PAD_EXPORT_FILENAME % new_pad_name
            # Add to processing list
            self.queuemanager.add_to_queue(new_pad_url)
            # Rewrite the link to point to the local file to be (since doing it afterwards, while slightly safer, is just too much work for now)
            tag['href'] = './%s' % new_htmlfile

        # Dump the soup to a file
        with open(htmlfile, 'w') as f:
            f.write(soup.prettify())

if __name__ == '__main__':
    # TODO: allow specifying entry URL via command line ?
    jm = jobmanager(DEFAULT_ENTRY_URL)
    jm.run()

