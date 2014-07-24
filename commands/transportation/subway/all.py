#encoding=utf-8
#
import urllib2
import json
from settings import *
import os
import chardet

from util import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getAllLines():
    '''获取所有线路
    '''

    lines_path = LINES_PREFIX % 'lines.json'

    content = cacheoronline(ALL_LINES, lines_path)

    detail = json.loads(content)['Response']['Main']
    lines = int(detail['@Rows'])
    data = detail['Item']
    print 'There are %d lines' % lines

    for line in data:
        try:
            # print line['XianLuMingCheng'], chardet.detect(line['XianLuMingCheng'].encode('UTF-8'))        
            cur.execute('INSERT INTO subway (sub_name, external_id, external_key) VALUES ("%s", "%s", "%s")' % (line['XianLuMingCheng'], line['XianLuBianMa'].encode('utf-8'), line['XianLuBianHao'].encode('utf-8')))
            con.commit()
        except Exception,se:
            print se
            con.rollback()

        getLineDetail(line['XianLuMingCheng'])

def getLineDetail(line):
    '''获取线路详情
    '''
    url = LINE_DETAIL + line
    fname = LINES_PREFIX % line + '.json'
    content = cacheoronline(url, fname)

    ## parse


def test():
    cur.execute('SELECT * FROM area')

    data = cur.fetchall()
    print data

def getAllStations():
    stations_path = STATIONS_PREFIX % 'stations.json'
    content = cacheoronline(ALL_STATIONS, stations_path)
