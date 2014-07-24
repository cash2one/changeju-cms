#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hollay
# @Date:   2014-07-08 10:37:59
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-07-08 12:07:44

import json
import MySQLdb
from DBUtils.PooledDB import PooledDB
from multiprocessing.dummy import Pool as ThreadPool

db_pool = PooledDB(MySQLdb, 6, host='10.0.100.1', user='remote',
                   passwd='remote', db='cj_db', charset='utf8', port=3306)

import urllib2

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

URI = '''http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=sEuGA0B3pDZMCVD2pwj6XOFs&callback=&city=%s'''


def get_area_geo(line):
    city = line[1]
    name = line[2]
    idx = line[0]

    url = URI % (name, city)

    resp = urllib2.urlopen(url)
    try:
        obj = json.load(resp)
        loc = obj['result']['location']
        lat = loc['lat']
        lng = loc['lng']

        UPDATE = '''UPDATE `cj_db`.`loc_area` SET longtitude = %s, latitude = %s WHERE area_id = %s'''

        conn = db_pool.connection()
        cur = conn.cursor()

        cur.execute(UPDATE % (lng, lat, idx))
        conn.commit()

        conn.close()

    except Exception,e:
        print name, city, obj

def get_station_geo(line):
    cityMap = ['', '北京市', '上海市']
    city = cityMap[line[2]]
    name = line[1] + '-地铁站'
    idx = line[0]

    lng = line[3]
    if lng is not None:
        return

    # URI = '''http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=sEuGA0B3pDZMCVD2pwj6XOFs&callback='''

    url = URI % (name, city)
    obj = {}

    try:
        resp = urllib2.urlopen(url)
        obj = json.load(resp)
        loc = obj['result']['location']
        lat = loc['lat']
        lng = loc['lng']

        UPDATE = '''UPDATE `cj_db`.`subway_station` SET longtitude = %s, latitude = %s WHERE id = %s'''

        conn = db_pool.connection()
        cur = conn.cursor()

        cur.execute(UPDATE % (lng, lat, idx))
        conn.commit()

        conn.close()
        print name
    except Exception,e:
        print e
        print name, city, obj
        print url

def run():
    # SQL = '''SELECT * FROM `cj_db`.`loc_area`'''
    SQL = '''SELECT * FROM `cj_db`.`subway_station`'''
    conn = db_pool.connection()
    cur = conn.cursor()

    cur.execute(SQL)

    results = cur.fetchall()

    conn.close()

    thread_pool = ThreadPool(5)
    # results = thread_pool.map(get_area_geo, results)
    results = thread_pool.map(get_station_geo, results)
    thread_pool.close()
    thread_pool.join()

    # get_station_geo(results[11])
    # for result in results:
    #     get_station_geo(result)
    #     break

if __name__ == '__main__':
    run()
    # html = urllib2.urlopen(URI % ('西二旗地铁站', '北京')).read()
    # print html
