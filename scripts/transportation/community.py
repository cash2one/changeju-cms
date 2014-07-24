# coding=utf-8
import os
from settings import con, cur
import json
import urllib2

BMAP_KEY = '84439343100cd6738dc68d84e3ceb000'
BMAP_GEO_URI = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&city=北京&ak=%s'

#http://api.map.baidu.com/geocoder/v2/?address=金隅万科二期&output=json&ak=84439343100cd6738dc68d84e3ceb000

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def dump_net_error(url, name):
    fp = None
    try:
        fp = open('e:/data/error.json', 'a')
        fp.writelines(name + '|' + url)
    finally:
        if fp:
            fp.close()

logfp = open(os.path.join('e:/data/', 'geo_not_found.log'), 'a')
# historyfp = None
fp = open('e:/data/data.log', 'w')
# geo_history = {}

def dump_place_error(place):
    logfp.writelines(place + '\n')

# def loadHistory():
#     global geo_history
#     history = open('c:/data/tmp/geo_history.log', 'r')
#     for line in history.readlines():
#         geo_history[line.strip()] = 1
#     history.close()

def parseComm():
    rfp = None
    try:
        rfp = open(os.path.join('e:/data/', 'all_comms.txt'))
        lines = rfp.readlines()
        count = 0
        print len(lines)
        for line in lines:
            count += 1
            # if count < 1025:
            #     continue
            values = line.split()
            # print 'len:', len(values), values[0]
            getGeo(values[0])
            print count
    except Exception, e:
        print 'parseComm exception', e, sys.exc_info()
    finally:
        if rfp:
            rfp.close()
empty = 0

def getGeo(place):
    global empty
    # global geo_history
    # try:
    #     if geo_history[place]:
    #         return
    # except Exception,e:
    #     print 3, e
    url = BMAP_GEO_URI % (place, BMAP_KEY)
    # {
    #     "status": 0,
    #     "result": {
    #         "location": {
    #             "lng": 121.21870795657,
    #             "lat": 31.055669676971
    #         },
    #         "precise": 0,
    #         "confidence": 50,
    #         "level": ""
    #     }
    # }
    try:
        resp = urllib2.urlopen(url)
        data = json.loads(resp.read())
    except:
        dump_place_error(url)
        return
    if 'result' in data and 'location' in data['result']:
        saveGeo(place, data['result'])
    else:
        empty += 1
        dump_place_error(place)

cache = []
total = 0
c = 0
import string
def saveGeo(name, data):
    global c
    global cache
    global total
    
    l = [name, str(data['location']['lng']), str(data['location']['lat']), str(data['precise']), str(data['confidence']), data['level'], '\n']
    fp.writelines(string.join(l, ' '))
    c += 1
    if c >= 50:
        fp.flush()
        c = 0

    ged_sql = '''INSERT INTO geo(name,longtitude, latitude, precise, confidence, level) VALUES (%s,%s,%s,%s,%s,%s)'''
    cache.append((name, str(data['location']['lng']), str(data['location']['lat']), int(data['precise']), int(data['confidence']), data['level']));
    if len(cache) >= 100:
        try:
            cur.executemany(ged_sql, cache)
            con.commit()
            total += len(cache)
            print total, ' records appended'
            cache = []
        except Exception,e:
            print 'saveGeo exception', e


def flushCache():
    global cache
    global total
    if len(cache) > 0:
        ged_sql = '''INSERT INTO geo(name, longtitude, latitude, precise, confidence, level) VALUES (%s,%s,%s,%s,%s,%s)'''
        cur.executemany(ged_sql, cache)
        con.commit()
        total += len(cache)
        print total, ' records appended in flush'

def clear():
    if con:
        try:
            con.commit()
            con.close()
        except Exception,e:
            print 'clear Exception', e

    if logfp:
        logfp.close()

    if fp:
        fp.close()

def test():
    s = '''INSERT INTO geo(name, longtitude, latitude, precise, confidence, level) VALUES (%s,%s,%s,%s,%s,%s)'''
    tmp = []
    tmp.append(('Hello', '100', '200', 20, 1, r'中文'))
    tmp.append(('Hello', '100', '200', 20, 1, r'中文'))
    tmp.append(('Hello', '100', '200', 20, 1, r'中文'))
    cur.executemany(s, tmp)
    con.commit()

def main():
    # global historyfp
    # test()
    # loadHistory()
    # historyfp = open('c:/data/tmp/geo_history.log', 'a')
    # getGeo(r'龙锦苑东三区')
    parseComm()
    flushCache()
    # test()
    # print 'empty count: ', empty
    clear()

if __name__ == '__main__':
    main()
# p = '\u5730\u4ea7\u5c0f\u533a'
# fp = None
# try:
#     fp = open('c:/data/comm_info.json')
#     content = fp.read()
#     # print content
#     data = json.loads(content)
#     for key in data:
#         print key
# except:
#     pass
# finally:
#     if fp:
#         fp.close()
# dump_net_error('a', 'b')
# dump_net_error('c', 'd')
# import urllib2
# proxy_handler = urllib2.ProxyHandler({
#     'http' : 'http://127.0.0.1:8087'
# })
# opener = urllib2.build_opener(proxy_handler)
# out = opener.open('http://www.baidu.com/')
# print out.read()