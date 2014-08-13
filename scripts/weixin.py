#!usr/bin/python
# coding=utf-8


import urllib2
import urllib
import time
import random
import base64
import hashlib

PARTNER = '2088111407760111'
SECRET = 'yrko6rh1y4nif8gamoan6nm7vcmsxenq'
BASE_URL = 'https://mapi.alipay.com/gateway.do?'
CB_URL = 'http://log.changeju.com/_.gif'
URL = 'https://mapi.alipay.com/gateway.do?_input_charset=gbk'

TOKEN = '28HlLLeVP6yglSXWV2qQHnAoHNGTDDzU7LBOGQ1Lf17UcJGzg0ePZcwk8ogfK-TPLJGjGO8PRz7uBvEoLiZGWA'

# 小区经理助手
APP_ID = 'wx5933773b6d17a75a'
APP_SECRET = 'f520a22c63b92d2f85ca7ebcf263336f'

# APP_ID = 'wx5933773b6d17a75a'
# APP_SECRET = 'f520a22c63b92d2f85ca7ebcf263336f'

# 畅e居
# APP_ID = 'wx0764cdaa1dfedb53'
# APP_SECRET = '1a447f555c5fea6eb50c497be21cb6f8'

data = {
    'event': '''<xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[FromUser]]></FromUserName>
    <CreateTime>123456789</CreateTime>
    <MsgType><![CDATA[event]]></MsgType>
    <Event><![CDATA[subscribe]]></Event>
    </xml>''',
    'qr': '''<xml><ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[FromUser]]></FromUserName>
    <CreateTime>123456789</CreateTime>
    <MsgType><![CDATA[event]]></MsgType>
    <Event><![CDATA[subscribe]]></Event>
    <EventKey><![CDATA[qrscene_123123]]></EventKey>
    <Ticket><![CDATA[TICKET]]></Ticket>
    </xml>''',
    'bind': '''<xml>
        <ToUserName><![CDATA[gh_a42c6faf3254]]></ToUserName>
        <FromUserName><![CDATA[oJ4a-t4R9oKbA1d4z8FpcZyNce2Y]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[CLICK]]></Event>
        <EventKey><![CDATA[ACTION_BIND]]></EventKey>
    </xml>''',
    'bind1': '''<xml>
        <ToUserName><![CDATA[gh_a42c6faf3254]]></ToUserName>
        <FromUserName><![CDATA[oJ4a-t5t-hZOgREARa6P9JzGNQ44]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[CLICK]]></Event>
        <EventKey><![CDATA[ACTION_BIND]]></EventKey>
    </xml>''',
    'bind2': '''<xml>
        <ToUserName><![CDATA[gh_a42c6faf3254]]></ToUserName>
        <FromUserName><![CDATA[oJ4a-t_x1dqkbCuUc57vty35P1OU]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[CLICK]]></Event>
        <EventKey><![CDATA[ACTION_BIND]]></EventKey>
    </xml>''',
    'verify': '''<xml>
        <ToUserName><![CDATA[gh_a42c6faf3254]]></ToUserName>
        <FromUserName><![CDATA[oJ4a-t_x1dqkbCuUc57vty35P1OU]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[CLICK]]></Event>
        <EventKey><![CDATA[ACTION_VERIFY]]></EventKey>
    </xml>''',
    'manage': '''<xml>
        <ToUserName><![CDATA[gh_a42c6faf3254]]></ToUserName>
        <FromUserName><![CDATA[oJ4a-t4R9oKbA1d4z8FpcZyNce2Y]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[CLICK]]></Event>
        <EventKey><![CDATA[ACTION_MANAGE]]></EventKey>
    </xml>''',
    'query': '''<?xml version="1.0" encoding="UTF-8"?>
        <xml><ToUserName><![CDATA[gh_a42c6faf3254]]></ToUserName>
        <FromUserName><![CDATA[oJ4a-t4R9oKbA1d4z8FpcZyNce2Y]]></FromUserName>
        <CreateTime>1400833886</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[no]]></Content>
        <MsgId>6016535727699418611</MsgId>
    </xml>''',
    'text': '''
    <xml>
    <ToUserName><![CDATA[gh_a42c6faf3254]]></ToUserName>
    <FromUserName><![CDATA[oJ4a-t4R9oKbA1d4z8FpcZyNce2Y]]></FromUserName> 
    <CreateTime>1400833886</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[1号院]]></Content>
    <MsgId>6016535727699418613</MsgId>
    </xml>''',
}


def post(phone, url='https://account.xiaomi.com/pass/sendPhoneTicket'):
    req = urllib2.Request(url)
    data = urllib.urlencode({'phone': phone})
    proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8087'})
    opener = urllib2.build_opener(proxy)
    resp = opener.open(req, data)
    return resp.read()


def postXML(type):
    xml_string = data[type]

    url = 'http://localhost:8080/admin-web/api/weixin/gateway'
    # url = 'http://manager.changeju.com/api/weixin/gateway'
    ts = str(int(time.time() * 1000))  # timestamp
    nonce = str(random.randrange(1464484386, 9999999999))  # nonce
    arr = [TOKEN, ts, nonce]
    arr = sorted(arr)
    sign = hashlib.sha1(''.join(arr)).hexdigest()  # signature
    url = ''.join(
        [url, '?timestamp=', ts, '&nonce=', nonce, '&signature=', sign])
    dt = (xml_string)

    req = urllib2.Request(url, dt)
    req.add_header('Content-Type', 'application/xml')
    req.add_header('ams-method', 'POST')

    r = urllib2.urlopen(req)
    print r.read()


def getAccessToken():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        APP_ID, APP_SECRET)
    r = urllib2.urlopen(url)
    # {"access_token":"GDae-OHjJn6Zxfv4dxCiYxOJwP-9ea-pszpegrBldJQZvIyDhJPY9Ym0RuGZg1JGiQzg8VgNh539CEZsK5RTdw","expires_in":7200}
    print r.read()


def postMenu():
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % TOKEN
    json = '''{
    "button": [{
        "name": "业务管理",
        "sub_button": [{
                "type": "click",
                "name": "房源审核",
                "key": "ACTION_VERIFY"
            }, {
                "type": "click",
                "name": "房源管理",
                "key": "ACTION_MANAGE"
            }, {
                "type": "click",
                "name": "收款说明",
                "key": "ACTION_HELP_PAY"
            }, {
                "type": "click",
                "name": "使用说明",
                "key": "ACTION_HELP"
            }]
        }, {
            "type": "click",
            "name": "账号绑定",
            "key": "ACTION_BIND"
        }]
    }'''

    data = (json)

    req = urllib2.Request(url, data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('ams-method', 'POST')

    r = urllib2.urlopen(req)
    print r.read()

# def postMessage():
#     url = 'http://localhost:8080/admin-web/api/weixin/gateway?'
#     pass

if __name__ == '__main__':
    # postMessage()
    # getAccessToken()
    # postMenu()

    # postXML('bind1')