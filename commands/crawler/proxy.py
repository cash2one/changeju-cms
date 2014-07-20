#!/usr/bin/python
#coding=utf-8

import ConfigParser
import random

from datetime import datetime

from bs4 import BeautifulSoup

import urllib2

UA = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
REFERER = 'http://cross.imethodz.com/'

class ProxyFactory():
    proxy_str = ''
    config = None

    def __init__(self, init='proxy.ini'):
        self.ini = init
        self.reload()

    def reload(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.ini)

        self.proxy_str = self.config.get('cn-proxy', 'list')

        self.proxies = self.proxy_str.split('|')

    def update_proxy(self):
        url = 'http://cn-proxy.com/'
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        req.add_header('Referer', REFERER)
        response = urllib2.urlopen(req)
        soup = BeautifulSoup(response.read())
        tbl = soup.findAll('table', {'class':'sortable'})
        lines = tbl[0].findAll('tr')
        count = len(lines)
        print count
        proxies = []
        for idx in xrange(2, count):
            cols = lines[idx].findAll('td')
            col_count = len(cols)
            proxies.append('%s:%s' % (cols[0].get_text(), cols[1].get_text()))

        self.config.set('cn-proxy', 'list', '|'.join(proxies))
        self.config.write(open(self.ini, 'w'))
        print 'proxy updated... Reloading proxies'
        self.reload()

    def random(self):
        return random.choice(self.proxies)

    def delete(self, proxy):
        if proxy in factory.proxies:
            factory.proxies.remove(proxy)

    def save(self):
        self.config.set('cn-proxy', 'list', '|'.join(self.proxies))
        self.config.write(open(self.ini, 'w'))

    def empty(self):
        return len(self.proxies) > 0

    def size(self):
        return len(self.proxies)

    def test(self, proxy=None, url='http://www.baidu.com/'):
        if not proxy:
            proxy = self.random()
        proxy_handler = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(proxy_handler)

        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        req.add_header('Referer', REFERER)
        start = datetime.now()
        try:
            response = opener.open(req)
            lasts = (datetime.now() - start).microseconds
            print '%s response: %s' % (proxy, lasts)
        except:
            self.delete(proxy)
            print 'proxy %s deleted' % proxy

    def test_all(self, url=None):
        for p in self.proxies:
            print p
            self.test(p, url=url)
            self.save()

if __name__ == '__main__':
    import socket
    socket.setdefaulttimeout(3)
    factory = ProxyFactory()
    factory.update_proxy()
    factory.test_all('http://www.ziroom.com/z/nl/')
    print factory.size()