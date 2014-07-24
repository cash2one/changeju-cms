#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hollay
# @Date:   2014-06-23 14:41:34
# @Last Modified by:   hollay
# @Last Modified time: 2014-06-30 16:34:50

from geohash.geohash import *

import MySQLdb
from DBUtils.PooledDB import PooledDB

db_pool = PooledDB(MySQLdb, 5, host='127.0.0.1', user='root',
                   passwd='root', db='cj_db', charset='utf8', port=3306)

import redis
r = redis.StrictRedis(host='10.0.100.1', port=6379, db=0)


def update_geohash():
    conn = db_pool.connection()
    cur = conn.cursor()

    SQL = 'SELECT comm_id, longtitude, latitude FROM community_geo'
    UPDATE = '''UPDATE community_geo SET geohash = '%s' WHERE comm_id = %s'''

    cur.execute(SQL)
    results = cur.fetchall()

    for line in results:
        h = encode(float(line[2]), float(line[1]), 6)
        cur.execute(UPDATE % (h, line[0]))

    conn.commit()


def update_geocunt():
    SQL = '''select community_geo.comm_id, community_geo.geohash, community_geo.longtitude, community_geo.latitude, community_geo.name, tmp.count from (select comm_id as id, count(*) as count from long_rent group by comm_id) as tmp JOIN community_geo where community_geo.comm_id = tmp.id;'''
    INSERT = '''INSERT INTO geo_community_count (comm_id, geohash, longtitude, latitude, comm_name, count) VALUES (%s, %s, %s, %s, %s, %s)'''
    conn = db_pool.connection()
    cur = conn.cursor()

    cur.execute(SQL)

    results = cur.fetchall()

    cur.executemany(INSERT, results)
    conn.commit()


def update_community():
    KEY_COMM = 'GEO_COMM_%s'
    SQL = '''SELECT comm_id, name, longtitude, latitude, geohash FROM community_geo'''
    conn = db_pool.connection()
    cur = conn.cursor()

    cur.execute(SQL)
    results = cur.fetchall()
    for result in results:
        r.hmset(KEY_COMM % result[0], {
            'comm_id': result[0],
            'comm_name': result[1],
            'longtitude': result[2],
            'latitude': result[3],
            'geohash': result[4]
        })
    print 'finish'


def update_count():
    KEY = 'GEO_COUNT_%s'
    KEY_GEO = 'GEO_HASH_%s'
    SQL = '''SELECT comm_id, count FROM geo_community_count'''
    conn = db_pool.connection()
    cur = conn.cursor()

    cur.execute(SQL)

    results = cur.fetchall()
    for result in results:
        r.set(KEY % result[0], result[1])
        r.expire(KEY % result[0], 30000)  # expire in 100 Min

        r.sadd(KEY_GEO % result[0], result[1])  # Add community to geohash map
    print 'finish'


def clean():
    GLOBAL_KEY = 'GEO_'
    keys = r.keys()
    print len(keys)
    for k in keys:
        r.delete(k)


def run():
    update_community()
    update_count()
    clean()

if __name__ == '__main__':
    run()
