#!/usr/bin/python
import re, urllib2
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup

# Some configurable things
DEFAULT_ENTRY_URL = "http://kirjoitusalusta.fi/hacklab"
ETHERPAD_BASE = "http://kirjoitusalusta.fi/"
PAD_NAME_RE = re.compile('^%s(?P<padname>[^/]+).*$' % ETHERPAD_BASE)
PAD_EXPORT_FORMAT = 'http://kirjoitusalusta.fi/ep/pad/export/%s/latest?format=html'


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

# http://kirjoitusalusta.fi/hacklab
# http://kirjoitusalusta.fi/ep/pad/export/hacklab/latest?format=html

    def fetch(self, pad_url):
        """This will fetch a single HTML export of a pad, add any other pads found in it to the job queue and rewrite links to local files"""
        m = PAD_NAME_RE.search(pad_url)
        if not m:
            return False
        export_url = PAD_EXPORT_FORMAT % m.group('padname')
        print "Fetching %s" % export_url
        try:
            fp = urllib2.urlopen(export_url)
        except urllib2.URLError,e:
            print "Failed to fetchs %s: %s" % (export_url, e)
            return False
        soup = BeautifulSoup(fp)
        print soup


if __name__ == '__main__':
    # TODO: allow specifying entry URL via command line ?
    jm = jobmanager(DEFAULT_ENTRY_URL)
    jm.run()

