#!/usr/bin/python
#coding=utf-8

import urllib2

from proxy import ProxyFactory

UA = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'

class ConnectFactory():

    UA = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'

    def __init__(self):
        self.proxy_factory = ProxyFactory()

    def get_opener(self, use_proxy=True):
        if use_proxy:
            proxy = self.proxy_factory.random()
            proxy_handler = urllib2.ProxyHandler({'http': proxy})
            opener = urllib2.build_opener(proxy_handler)
        else:
            opener = urllib2.build_opener()

        return opener

    def build_request(self, url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        req.add_header('Referer', '')
        return req

if __name__ == '__main__':
    cf = ConnectFactory()
    for i in range(10):
        opener = cf.get_opener(use_proxy=True)

        req = urllib2.Request('http://www.baidu.com/')
        req.add_header('User-Agent', UA)
        req.add_header('Referer', '')
        resp = opener.open(req)
        print resp.code