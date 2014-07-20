#!/usr/bin/python
#coding=utf-8

import urllib2
from multiprocessing.dummy import Pool as ThreadPool
import time, re, datetime
from bs4 import BeautifulSoup

import logging
logger = logging.getLogger()
logfile = '/tmp/homelink.log'
hdlr = logging.FileHandler(logfile)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

CONNECTION = 10

# from proxy import ProxyFactory
from connect import ConnectFactory

UA = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
REFERER = 'http://beijing.homelink.com.cn/'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# proxy_factory = ProxyFactory()
connectify = ConnectFactory()

import MySQLdb
from DBUtils.PooledDB import PooledDB

# db_pool = PooledDB(MySQLdb, 5, host='127.0.0.1', user='root', passwd='root', db='cj_cms', charset='utf8', port=3306)
db_pool = PooledDB(MySQLdb, CONNECTION, host='10.0.100.1', user='remote', passwd='remote', db='cj_cms', charset='utf8', port=3306)

import redis
r = redis.StrictRedis(host='10.0.100.1', port=6379, db=0)

BASE_URL = 'http://beijing.homelink.com.cn/zufang/cto0/'

TODAY = datetime.datetime.now().strftime('%Y-%m-%d')
LAST_MONTH = '2014-00-00'

# 租金、面积、户型、建筑年代、小区名称、发布时间

def get_count(url):
    opener = connectify.get_opener(use_proxy=False)
    request = connectify.build_request(url)
    response = opener.open(request)
    soup = BeautifulSoup(response.read())
    ps = soup.findAll('div', {'class': 'public condition'})
    if len(ps) > 0:
        span = ps[0].findAll('span')
        return int(span[0].get_text())
    else:
        exit(1)

def gen_list(count):
    url = BASE_URL + 'pg%s'
    urls = []
    for i in xrange(1, count + 1):
        urls.append((i, url % i))
    return urls

def insert_db(data):
    '''
    (title, url, homelink_id, rent, house_type, building_year, pub_date, off_date, area, community_name, status)
    '''
    SQL = 'INSERT INTO datasource_homelink_house (title, url, homelink_id, rent, house_type, building_year, pub_date, off_date, area, community_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    try:
        conn = db_pool.connection()
        cur = conn.cursor()
        
        cur.executemany(SQL, data)
        conn.commit()

        cur.close()
        conn.close()
        return True
    except Exception, e:
        print 'insert error: %s' % e
        return False

def update_db(row):
    '''
    INSERT INTO datasource_homelink_house (title, url, homelink_id, rent, house_type, building_year, pub_date, off_date, area, community_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    SQL = '''INSERT INTO datasource_homelink_house (title, url, homelink_id, rent, house_type, building_year, pub_date, off_date, area, community_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE off_date=CURDATE(), last_update=NOW()'''

    try:
        conn = db_pool.connection()
        cur = conn.cursor()
        
        cur.execute(SQL, row)
        conn.commit()

        cur.close()
        conn.close()
        return True
    except Exception, e:
        print 'insert error: %s' % e
        return False


def get_page(tup, retry=0):
    (pg, url) = tup

    if r.exists('hl_%s' % pg):
        print '%s skipped' % pg
        return

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
            r.set('hl_fail_%s' % pg, pg)
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
            elif date_text == u'1个月前发布':
                date = LAST_MONTH
            else:
                dpt = re.compile(r'.*(\d{2}-\d{2}).*')
                dmatch = dpt.match(date_text)
                if dmatch:
                    date = '2014-%s' % dmatch.group(1)

            price_box = item.find('div', {'class': 'price'})

            price = price_box.find('b').get_text()

            # data.append((title, link, hid, price, htype, bd_year, date, TODAY, area, comm))
            ret = update_db((title, link, hid, price, htype, bd_year, date, TODAY, area, comm))

        r.set('hl_%s' % pg, pg)
        # ret = insert_db(data)
        # if ret:
        #     print '%s success' % pg
        #     r.set('hl_%s' % pg, pg)
        # else:
        #     print '%s insert error' % pg
        #     r.set('hl_fail_%s' % pg, pg)

    except Exception, e:
        r.set('hl_fail_%s' % pg, pg)

def run():
    count = get_count(BASE_URL)
    pages = (count + 11) / 12

    urls = gen_list(pages)

    thread_pool = ThreadPool(CONNECTION)
    results = thread_pool.map(get_page, urls)
    thread_pool.close()
    thread_pool.join()

if __name__ == '__main__':
    # data = [('丰台 新村三里 1居室 49平米', '/zufang/BJFT87758946.shtml', 'BJFT87758946', 3200, '1室1厅', '2003', '2014-06-16', '2014-06-16', 44, '十里堡南区')]
    # insert_db(data)
    run()
    # update_db(('default', '1234', 'BJFT87762547', 500, 'bcd', '11', '2014-01-01', '2014-02-02', 100, 'China'))
    # get_page((1, 'http://beijing.homelink.com.cn/zufang/cto0/pg2/'))
