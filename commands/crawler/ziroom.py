#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-07-20 16:13:45
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-07-21 00:34:23

import urllib2
import urllib
import re
import datetime
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

PREIX = 'http://www.ziroom.com'
CONNECTION = 5

UA = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
REFERER = 'http://www.ziroom.com/z/nl/sub/'

from connect import ConnectFactory
connectify = ConnectFactory()
import MySQLdb
from DBUtils.PooledDB import PooledDB

db_pool = PooledDB(MySQLdb, CONNECTION, host='10.0.100.1',
                   user='remote', passwd='remote', db='cj_cms', charset='utf8', port=3306)

import redis
r = redis.StrictRedis(host='10.0.100.1', port=6379, db=0)

TODAY = datetime.datetime.now().strftime('%Y-%m-%d')


def get_url_id(url):
    # 'http://www.ziroom.com/z/vr/41998.html'
    pt = re.compile('/([^/]+)\.html')
    m = pt.search(url)
    return m.group(1)


def fetch_page(url):
    opener = connectify.get_opener(use_proxy=False)
    request = connectify.build_request(url)
    response = opener.open(request)
    soup = BeautifulSoup(response.read())
    return soup


def extract_page(soup):
    items = []
    hl = soup.find(id='houseList')
    iteml = hl.findAll('li')
    for item in iteml:
        tt = item.find('h3').find('a', href=re.compile('http://*'))

        b = item.find('b', class_='t_pagemapbtn')

        t = item.find('p', class_='condition')

        p = item.find('div', class_='priceDetail').find('span', class_='en')

        d = item.find('p', class_='detail')

        c = item.find('p', class_='comments')

        url = tt['href']
        title = tt.get_text().strip()
        lng = b['data-lng']
        lat = b['data-lat']
        comm = b['data-title']
        addr = b['data-addr']
        price = p.get_text()
        desc = d.get_text().strip()
        tags = t and t.get_text().strip() or ''
        comments = c.get_text().strip()

        items.append(
            (get_url_id(url), url, title, lng, lat, comm, addr, price, desc, tags, comments))

    return items


def insert_rows(rows):
    SQL = '''INSERT INTO ds_ziroom_house (url_id, url, title, lng, lat, community, address, price, 
        description, tags, comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        ON DUPLICATE KEY UPDATE count=count+1, last_update=NOW()'''

    try:
        conn = db_pool.connection()
        cur = conn.cursor()

        cur.executemany(SQL, rows)
        conn.commit()

        cur.close()
        conn.close()
    except Exception, e:
        print e


def next_page(soup, url):
    pg = soup.find(id='page')
    lks = pg.findAll('a')
    if not lks:
        return None
    else:
        n = lks.pop()['href']
        if url == n or url.endswith(n):
            return None
        else:
            if n.startswith('?'):
                return url + n
            else:
                return n


def one(url):
    if r.exists('zr_succ_%s' % url):
        return

    soup = fetch_page(url)
    rows = extract_page(soup)
    insert_rows(rows)

    r.set('zr_succ_%s' % url, 1)

    np = next_page(soup, url)
    if(np):
        one(np)


def run():
    with open('/usr/local/etc/cms/urls_area.txt', 'r') as fp:
        lines = fp.readlines()
        urls = [line.strip() for line in lines]

        thread_pool = ThreadPool(CONNECTION)
        results = thread_pool.map(one, urls)
        thread_pool.close()
        thread_pool.join()

    keys = r.keys('zr_succ_*')
    for k in keys:
        r.delete(k)
    print 'clean complete'


def prepare():
    lines = []
    base = 'http://www.ziroom.com/z/nl/'
    soup = fetch_page(base)
    dl = soup.find('div', class_='selection_box').find('dl')
    links = dl.findAll('a', class_='')

    for link in links:
        sp = fetch_page(link['href'])
        p = sp.find('p', class_='t_areaboxcontent')
        lks = p.findAll('a', class_='')
        for lk in lks:
            lines.append('%s%s\n' % (PREIX, lk['href']))
        print link

    with open('urls_area.txt', 'w') as fp:
        fp.writelines(lines)

if __name__ == '__main__':
    run()
    # prepare()
