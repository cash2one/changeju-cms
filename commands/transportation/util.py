# encoding=utf-8

import os
import urllib2
from settings import *
from random import random

def save(title, data):
    '''
    '''
    fp = open(os.path.join(BASE_PATH, title), 'w')
    fp.write(data)

def dump_net_error(url, name):
    fp = None
    try:
        fp = open(os.path.join(BASE_PATH, 'error.json'), 'a')
        fp.writelines(url + '|' + name + '\n')
    finally:
        if fp:
            fp.close()

def cacheoronline(url, fname, times=1, force=False):
    path = os.path.join(BASE_PATH, fname)
    fp = None
    content = ''
    try:
        fp = open(path)
        content = fp.read()
    except:
        Proxy_Or_Not = random() * 10 > 7

        try:
            if Proxy_Or_Not:
                content = urllib2.urlopen(url).read()
            else:
                proxy_handler = urllib2.ProxyHandler({"http" : 'http://127.0.0.1:8087'})
                opener = urllib2.build_opener(proxy_handler)
                content = opener.open(url).read()
            save(fname, content)
            print fname, ' loaded'
        except Exception,e:
            print e
            dump_net_error(url, fname)
            if times < 3:
                print 'retry ' + fname
                cacheoronline(url, fname, times+1)
    finally:
        if fp:
            fp.close()
    return content