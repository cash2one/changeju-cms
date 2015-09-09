#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hollay
# @Date:   2014-06-18 01:21:35
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2015-09-07 23:53:09

import MySQLdb
from DBUtils.PooledDB import PooledDB

# db_pool = PooledDB(MySQLdb, 5, host='127.0.0.1', user='root', passwd='root', db='cj_cms', charset='utf8', port=3306)
db_pool = PooledDB(MySQLdb, 1, host='10.0.100.1', user='remote',
                   passwd='remote', db='cj_cms', charset='utf8', port=3306)


def run():
    conn = db_pool.connection()
    cur = conn.cursor()

    SQL = '''select title, url, homelink_id, rent, house_type, building_year, pub_date, off_date, area, community_name from ds_homelink_hourly where homelink_id not in (select homelink_id from ds_homelink_house where pub_date >= '2014-06-17');'''

    cur.execute(SQL)

    results = cur.fetchall()

    print len(results)

    # for result in results:
    #     print result

    # return

    NSQL = SQL = '''INSERT INTO ds_homelink_house (title, url, homelink_id, rent, house_type, building_year, pub_date, off_date, area, community_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE off_date=CURDATE()-1, last_update=NOW()'''

    try:
        cur.executemany(NSQL, results)
        conn.commit()

        cur.close()
        conn.close()
    except Exception, e:
        print e

if __name__ == '__main__':
    run()
