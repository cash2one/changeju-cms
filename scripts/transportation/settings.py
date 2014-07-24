#encoding=utf-8

KEY = r'aeb3dab5-6099-4f03-b7a3-0e6c221eb77f'
ZONE = r'%e5%8c%97%e4%ba%ac' # 北京
BASE = r'http://www.twototwo.cn/'
ALL_CITIES = r'http://www.twototwo.cn/metro/Service.aspx?format=json&action=QueryAllMetroLine&key=aeb3dab5-6099-4f03-b7a3-0e6c221eb77f&zone=%e5%8c%97%e4%ba%ac&more=1&pageIndex=1&pageSize=30'
ALL_LINES = r'http://www.twototwo.cn/metro/Service.aspx?format=json&action=QueryAllMetroLine&key=%s&zone=%s&more=1&pageIndex=1&pageSize=20' % (KEY, ZONE)
ALL_STATIONS = r'http://www.twototwo.cn/metro/Service.aspx?format=json&action=QueryAllMetroStation&key=aeb3dab5-6099-4f03-b7a3-0e6c221eb77f&zone=%E5%8C%97%E4%BA%AC&more=1&pageIndex=1&pageSize=300'

LINE_DETAIL = r'http://www.twototwo.cn/metro/Service.aspx?format=json&action=QueryMetroByLine&key=aeb3dab5-6099-4f03-b7a3-0e6c221eb77f&zone=%e5%8c%97%e4%ba%ac&line='
BASE_PATH = r'c:/data/cj/'
LINES_PREFIX = r'lines/%s'
STATIONS_PREFIX = r'stations/%s'


BUSLINE_PREFIX = r'bus/lines/%s'
BUSSTOP_PREFIX = r'bus/stops/%s'
ALL_BUS_CITY = r'http://www.twototwo.cn/bus/Service.aspx?format=json&action=QueryAllBusZone&key=aeb3dab5-6099-4f03-b7a3-0e6c221eb77f'
ALL_BUS_LINES = r'http://www.twototwo.cn/bus/Service.aspx?format=json&action=QueryAllBusLine&key=aeb3dab5-6099-4f03-b7a3-0e6c221eb77f&zone=%E5%8C%97%E4%BA%AC&more=1&pageIndex=1&pageSize=2000'
BUS_LINE_DETAIL = r'http://www.twototwo.cn/bus/Service.aspx?format=json&action=QueryBusByLine&key=aeb3dab5-6099-4f03-b7a3-0e6c221eb77f&zone=%E5%8C%97%E4%BA%AC&line='

ALL_BUS_STATIONS = r'http://www.twototwo.cn/bus/Service.aspx?format=json&action=QueryAllBusStation&key=aeb3dab5-6099-4f03-b7a3-0e6c221eb77f&zone=%E5%8C%97%E4%BA%AC&more=1&pageSize=40&pageIndex='

import MySQLdb as mdb
con = None
con = mdb.connect('127.0.0.1', 'cj', 'cj', 'cj', charset='utf8' );

#所有的查询，都在连接con的一个模块cursor上面运行的
cur = con.cursor()

#执行一个查询
# cur.execute("SELECT VERSION()")

#取得上个查询的结果，是单个结果
# data = cur.fetchone()
