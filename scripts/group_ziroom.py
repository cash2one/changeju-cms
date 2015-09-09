#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-09-03 23:15:57
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-09-08 22:35:46

from geohash.geohash import *

import re
import MySQLdb
from DBUtils.PooledDB import PooledDB

# db_pool = PooledDB(MySQLdb, 5, host='10.0.100.1', user='remote',
#                    passwd='remote', db='cj_cms', charset='utf8', port=3306)
db_pool = PooledDB(MySQLdb, 5, host='127.0.0.1', user='root',
                   passwd='root', db='cj_cms', charset='utf8', port=3306)

import redis
r = redis.StrictRedis(host='10.0.100.1', port=6379, db=0)

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# update ziroom set lng = '116.258370335', lat='39.8419378522' where community = '东铁营定向安置房';
# update ziroom set lng = '116.47722644938', lat='39.876637622155' where community = '沁园';
# update ziroom set lng = '116.25253967014', lat='39.971880659564' where community = '京泉馨苑东里';
# update ziroom set lng = '116.521694891', lat='39.9589531664' where community = '远洋新悦一期';



def gen_geohash():
    conn = db_pool.connection()
    cur = conn.cursor()

    SQL = 'SELECT * FROM ziroom'
    UPDATE = '''UPDATE ziroom SET geohash5 = '%s' WHERE id = %s'''

    cur.execute(SQL)

    records = cur.fetchall()
    count = 0
    for record in records:
        pk = int(record[0])
        lat = float(record[5])
        lng = float(record[4])
        try:
            h = encode(lat, lng, 5)
        except:
            continue

        cur.execute(UPDATE % (h, pk))

        count = (count + 1) % 50
        if count == 0:
            print 'commit'
            conn.commit()

    conn.commit()


def gen_title():
    conn = db_pool.connection()
    cur = conn.cursor()

    SQL = 'SELECT * FROM ziroom'
    UPDATE = '''UPDATE ziroom SET house_title = '%s' WHERE id = %s'''

    cur.execute(SQL)

    records = cur.fetchall()
    count = 0
    for record in records:
        pk = int(record[0])
        title = record[3]
        house_title = title[:title.find('-')]

        cur.execute(UPDATE % (house_title, pk))
        count = (count + 1) % 50
        if count == 0:
            print 'commit'
            conn.commit()

    conn.commit()

def extract_subway():
    SQL = '''SELECT * FROM ziroom WHERE tags like '%地铁周边%' '''
    UPDATE = '''UPDATE ziroom SET subway_line = '%s', subway_station = '%s', subway_walk = %s where id = %s'''
    pt = re.compile(ur'.*距(.*线)(.*)步行(\d+)分钟.*')

    conn = db_pool.connection()
    cur = conn.cursor()

    cur.execute(SQL)

    records = cur.fetchall()

    count = 0
    for record in records:
        pk = int(record[0])
        addr = record[9]

        match = pt.match(addr)
        if match:
            line = match.group(1)
            station = match.group(2)
            time = match.group(3)

            cur.execute(UPDATE % (line, station, time, pk))

            count = (count + 1) % 100
            if count == 50:
                conn.commit()
                print 'commit'
        else:
            print pk, addr

    conn.commit()
    # if match:
    #     print match.group(1)
    #     print match.group(2)
    #     print match.group(3)
    # else:
    #     print 'no'


def gen_coord(geohash):
    print decode(geohash, delta=True)

def test():
    SQL = ''' SELECT * FROM ziroom WHERE subway_station IS NULL'''
    conn = db_pool.connection()
    cur = conn.cursor()
    cur.execute(SQL)
    records = cur.fetchall()
    
    # cur.execute('''SELECT COUNT(*) FROM `cj_db`.`community`''')

    # record = cur.fetchone()
    # print record

def run():
    test()
    # extract_subway()
    # gen_title()
    # gen_geohash()
    # gen_coord('wx4g3x')

if __name__ == '__main__':
    run()
