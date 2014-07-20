#!/usr/bin/python
#coding=utf-8

import urllib2
from multiprocessing.dummy import Pool as ThreadPool
import time, re, datetime
from bs4 import BeautifulSoup

CONNECTION = 10

UA = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
REFERER = 'http://beijing.homelink.com.cn/'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# from proxy import ProxyFactory
# proxy_factory = ProxyFactory()
from connect import ConnectFactory
connectify = ConnectFactory()

import MySQLdb
from DBUtils.PooledDB import PooledDB

# db_pool = PooledDB(MySQLdb, 5, host='127.0.0.1', user='root', passwd='root', db='cj_cms', charset='utf8', port=3306)
db_pool = PooledDB(MySQLdb, CONNECTION, host='10.0.100.1', user='remote', passwd='remote', db='cj_cms', charset='utf8', port=3306)

import redis
r = redis.StrictRedis(host='10.0.100.1', port=6379, db=0)

BASE_URL = 'http://beijing.homelink.com.cn/zufang/cto0/pg%s'

TODAY = datetime.datetime.now().strftime('%Y-%m-%d')

FINISH = False # Global

def insert_db(data):
    '''
    (title, url, homelink_id, rent, house_type, building_year, pub_date, off_date, area, community_name, status)
    '''
    SQL = '''INSERT INTO ds_homelink_hourly (title, url, homelink_id, rent, house_type, building_year, pub_date, off_date, area, community_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE count = count + 1'''
    try:
        conn = db_pool.connection()
        cur = conn.cursor()
        
        cur.execute(SQL, data)
        conn.commit()

        cur.close()
        conn.close()
        return True
    except Exception, e:
        print 'insert error: %s' % e
        return False

def get_page(tup, retry=0):
    global FINISH
    (pg, url) = tup

    opener = connectify.get_opener(use_proxy=False)
    request = connectify.build_request(url)

    try:
        response = opener.open(request)
        soup = BeautifulSoup(response.read())
    except Exception, e:
        print e
        if retry < 2:
            print '%s retry' % pg
            return get_page(tup, retry+1)
        else:
            print '%s failed' % pg
            r.set('hl_hour_fail_%s' % pg, pg)
            return None

    try:
        container = soup.find(id='listData')
        lists = container.findAll('div', {'class': 'public indetail'})

        data = []

        for item in lists:
            head_box = item.find('h3')
            link = head_box.find('a')
            title = link.get_text()

            link = link['href']

            pt1 = re.compile(r'.*\/([^\/\.]+)\..*')
            match1 = pt1.match(link)
            hid = ''
            if match1:
                hid = match1.group(1)

            content_box = item.find('div', {'class': 'content'})
            comm_box = content_box.find('li', {'class': 'one'})
            comm = comm_box.get_text()
            
            type_box = content_box.find('li', {'class': 'two'})
            htype = type_box.get_text()

            area_box = content_box.find('li', {'class': 'three'}).find('span')
            area = area_box.get_text()

            text_box = content_box.find('p', {'class': 'clearfix'})
            text = text_box.get_text()

            bd_year = '1900'
            pt = re.compile(r'.*(\d{4}).*')
            match = pt.match(text)
            if match:
                bd_year = match.group(1)

            date_box = content_box.find('ol').find('font')

            date_text = date_box.get_text()
            date = '1900-00-00'
            if date_text == u'今天发布':
                date = TODAY
            else:
                FINISH = True
                print 'today finished, break'
                break

            price_box = item.find('div', {'class': 'price'})

            price = price_box.find('b').get_text()

            data.append((title, link, hid, price, htype, bd_year, date, TODAY, area, comm))
            insert_db((title, link, hid, price, htype, bd_year, date, TODAY, area, comm))

        # ret = insert_db(data)
        # if ret:
        #     print '%s success' % pg
        #     r.set('hl_hour_%s' % pg, pg)
        # else:
        #     print '%s insert error' % pg
        #     r.set('hl_hour_fail_%s' % pg, pg)

    except Exception, e:
        r.set('hl_hour_fail_%s' % pg, pg)

def run():
    page = 1
    while not FINISH:
        get_page((page, BASE_URL % page))
        page += 1

if __name__ == '__main__':
    run()

