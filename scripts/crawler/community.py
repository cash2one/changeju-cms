#!/usr/bin/python
#coding=utf-8
#encoding:utf-8

import urllib2
from multiprocessing.dummy import Pool as ThreadPool
import time, re, datetime
from bs4 import BeautifulSoup

CONNECTION = 10

UA = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
REFERER = 'http://beijing.homelink.com.cn/'

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from connect import ConnectFactory
connectify = ConnectFactory()

import MySQLdb
from DBUtils.PooledDB import PooledDB

db_pool = PooledDB(MySQLdb, 5, host='127.0.0.1', user='root', passwd='root', db='test', charset='utf8', port=3306)
# db_pool = PooledDB(MySQLdb, CONNECTION, host='10.0.100.1', user='remote', passwd='remote', db='cj_cms', charset='utf8', port=3306)

import redis
r = redis.StrictRedis(host='10.0.100.1', port=6379, db=0)

BASE_URL = 'http://bj.lianjia.com/xiaoqu/pg%s/'

TODAY = datetime.datetime.now().strftime('%Y-%m-%d')

def insert_db(data):
    '''
    (title, link, area, zone, subway, other, bd_year, price)
    '''
    SQL = '''INSERT INTO comm (title, link, area, zone, subway_desc, subway_line, subway_station, remarks, bd_year, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE count = count + 1'''
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
    (pg, url) = tup

    print 'page %s fetching' % pg

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
            r.set('hl_comm_fail_%s' % pg, pg)
            return None

    try:
        print 'page %s extracting' % pg

        container = soup.find(id='house-lst')

        lists = container.findAll('li') #, {'class': 'public indetail'}

        data = []

        for item in lists:

            title, link, area, zone, subway_desc, subway_line, subway_station, other, bd_year, price = ('', '', '', '', '', '', '', '', 1900, 0)

            head_box = item.find('h2')
            link_dom = head_box.find('a')

            if link_dom:
                title = link_dom.get_text() # 标题/小区名
                link = link_dom['href'] # 链接

            area_dom = item.find('a', {'class': 'ad'})
            if area_dom:
                area = area_dom.get_text() # 区域

            # 商圈
            zone_dom = area_dom.next_sibling
            if zone_dom:
                zone = zone_dom.get_text()

            subway_dom = item.find('span', {'class': 'fang-subway-ex'})
            if subway_dom:
                subway_desc = subway_dom.get_text() # 地铁描述

                # 近地铁5号线天通苑南站
                pt = re.compile(ur'.*近(.+线)(.+站)')
                match = pt.match(subway_desc)
                if match:
                    subway_line = match.group(1)
                    subway_station = match.group(2)

            other = ''
            other_box = item.find('div', {'class': 'con'})
            if other_box:
                other = other_box.get_text()            

            pt = re.compile(r'.*(\d{4}).*')
            match = pt.match(other)
            if match:
                bd_year = match.group(1)

            price_box = item.find('span', {'class': 'num'})
            if price_box:
                price = price_box.get_text() # 价格
                if not price.isnumeric():
                    price = 0

            # data.append((title, link, area, subway, other, bd_year, bd_year, price))
            insert_db((title, link, area, zone, subway_desc, subway_line, subway_station, other, bd_year, price))

        r.sadd('community_success', pg)

    except Exception, e:
        print e
        # r.set('hl_page_fail_%s' % pg, pg)
        r.sadd('community_fail', pg)

def run():
    for page in xrange(400):
        get_page((page + 1, BASE_URL % (page + 1)))

if __name__ == '__main__':
    run()

