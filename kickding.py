#!/usr/bin/python2
from bs4 import BeautifulSoup as bs

import urllib
import json
import subprocess
import time
from random import randint

# the URL for the project to watch. 
site = 'http://www.kickstarter.com/projects/peterseid/romo-the-smartphone-robot-for-everyone/'
# the sound to play, once for each unit sold
pingsound = './ping.wav'
# a command-line sound player (on mac, use afplay)
player = 'aplay'
refresh = 40 # in seconds
mults = [0, 0, 1, 1, 1, 1, 1, 1, 1] # how many units sold at each backer tier

class Kick:
    ''' A quickly hacked-together script to watch a kickstarter project, and
    play a sound every time one more 'unit' is backed. Inspired by Netscape's
    cannon shots timed to Navigator downloads, as retold by jwz.'''
    def __init__(self, page):
        self.page = page
        self.backers = self.get_backers()
    
    def soup(self):
        while True:
            try:
                ret = bs(urllib.urlopen(self.page).read())
                break
            except Exception as e:
                # pause and try again
                print e
                time.sleep(2)
        return ret

    def get_data(self):
        data = self.soup().find_all('script', limit=2)[1]
        return json.loads(data[data.find('{') : data.rfind('}')])

    def get_backers(self):
        backs = self.soup().find('ul', id='what-you-get').find_all('li')
        f = lambda t: int(t.strip().split()[0])
        return [f(li.find('span', 'num-backers').contents[0]) for li in backs]

    def delta(self):
        prev = self.backers
        # only take note of increases in backers. If there's a decrease, it'll
        # just go quiet until we pass the high point again.
        # this becomes especially relevant when load-balancing is bouncing you
        # between two servers that are not exactly in sync.
        self.backers = [max(b, n, 0) for (b, n) in zip(self.backers,
                                                       self.get_backers())]
        return [max(c-p, 0) for c, p in zip(self.backers, prev)]

def ping():
    # change this up if you want a more complicated reaction. Other stuff has
    # been designed around this call taking one second, though.
    print 'ping!'
    subprocess.call([player, pingsound])

if __name__ == '__main__':
    foo = Kick(site)
    # starting number of backers
    print foo.backers
    while True:
        sales = foo.delta()
        print time.asctime(), sales
        # figure out how many units were sold in this delta
        count = sum([a*c for (a, c) in zip(sales, mults)])
        if count > refresh:
            # hell yeah, more than one a second! ping until they're all
            # accounted for.
            # Note: the original sound clip was one second long.
            for i in range(count):
                ping()
        elif count > 0:
            for i in range(count):
                ping()
                # dither the timing a bit so that it's not too regular
                time.sleep(max(refresh / float(count) + randint(-5, 5), 0))
        else:
            time.sleep(refresh)
