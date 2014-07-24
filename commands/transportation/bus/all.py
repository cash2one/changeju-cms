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

def getBusLineDetail(line):
    path = BUSLINE_PREFIX % line + '.json'
    content = cacheoronline(BUS_LINE_DETAIL + line, path)

def getAllBusStop(page=1):
    # ALL_BUS_STATIONS
    path = BUSSTOP_PREFIX % ('all_' + str(page) + '.json')
    url = ALL_BUS_STATIONS + str(page)
    content = cacheoronline(url, path)
    data = json.loads(content)
    pageInfo = data['Response']['Page']
    if page < int(pageInfo['TotalPage']):
        getAllBusStop(page+1)

def getAllBusLines():
    content = cacheoronline(ALL_BUS_LINES, 'bus/lines/all.json')
    import json
    data = json.loads(content)['Response']['Main']
    num = int(data['@Rows'])
    items = data['Item']
    for item in items:
        getBusLineDetail(item['XianLuMingCheng'])
