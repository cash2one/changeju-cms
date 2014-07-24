#encoding=utf-8

from util import *

from subway.all import *
from bus.all import *

def main():

    # test()
    # getAllLines()
    # getAllStations()
    # getAllBusLines()
    # getAllBusStop()
    test()
    clear()

def clear():
    if con:
        con.close()

def step1():
    fp = None
    nfp = None
    try:
        fp.open('c:/data/tmp/comm_info.txt')
        nfp.open('c:/data/tmp/step1.txt')
        lines = fp.readlines()
        for line in lines:
            
    except:
        pass
    finally:
        if fp:
            fp.close()
        if nfp:
            nfp.close()

def test():
    # SECRET = r'84439343100cd6738dc68d84e3ceb000'

    # url = 'http://api.map.baidu.com/geocoder?address=%s&output=json&key=%s&city=北京' % (r'龙锦苑东三区', SECRET)
    # html = urllib2.urlopen(url)
    # print html.read()
    print '，'

if __name__ == '__main__':
    main()