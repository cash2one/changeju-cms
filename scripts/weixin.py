#!usr/bin/python
# coding=utf-8


import urllib2
import urllib
import time
import random
import base64
import hashlib

import json

PARTNER = '2088111407760111'
SECRET = 'yrko6rh1y4nif8gamoan6nm7vcmsxenq'
BASE_URL = 'https://mapi.alipay.com/gateway.do?'
CB_URL = 'http://log.changeju.com/_.gif'
URL = 'https://mapi.alipay.com/gateway.do?_input_charset=gbk'

TOKEN = '28HlLLeVP6yglSXWV2qQHnAoHNGTDDzU7LBOGQ1Lf17UcJGzg0ePZcwk8ogfK-TPLJGjGO8PRz7uBvEoLiZGWA'

# 小区经理助手
# APP_ID = 'wx5933773b6d17a75a'
# APP_SECRET = 'f520a22c63b92d2f85ca7ebcf263336f'

# 测试账号
APP_ID = 'wx60d4c4a2eb413c26'
APP_SECRET = '04be60b30db22acefc524e908b264de7'

# 测试账号2
APP_ID = 'wx359b54263ab9dca2'
APP_SECRET = 'cb6f31c61fa644783cfab1ae736e5786'

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

testMenu = u'''
{
    "button": [{
        "type": "click",
        "key": "HELP",
        "name": "微店"
    }, {
        "name": "唯珍基地",
        "sub_button": [{
            "type": "click",
            "name": "刘斌堡中心基地",
            "key": "基地"
        }, {
            "type": "click",
            "key": "GOOD",
            "name": "七星河大米基地"
        }, {
            "type": "click",
            "key": "HELP",
            "name": "井儿沟冬产基地"
        }, {
            "type": "click",
            "key": "HELP",
            "name": "大古山养殖基地"
        }, {
            "type": "click",
            "name": "沈家营示范基地",
            "key": "沈家营"
        }]
    }, {
        "name": "关于我们",
        "sub_button": [{
            "type": "click",
            "key": "HELP",
            "name": "唯珍首页"
        }]
    }]
}
'''



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


def getAccessToken(aid=APP_ID, asecret=APP_SECRET):
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        aid, asecret)
    r = urllib2.urlopen(url)
    # q8XmGI4U0Z_59GnsyPs5zE6L1vwkrGH8pliVfz99pFJKxausnQy-jzxdxV7Z9JVboJnAD7hmRSEjQ-4WijZYhA
    # {"access_token":"GDae-OHjJn6Zxfv4dxCiYxOJwP-9ea-pszpegrBldJQZvIyDhJPY9Ym0RuGZg1JGiQzg8VgNh539CEZsK5RTdw","expires_in":7200}
    jstr = r.read()
    jobj = json.loads(jstr)
    print jobj['access_token']
    return jobj['access_token']

def postMenu(token):
    global testMenu
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % token
    jsonstr = u'''{
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

    # data = (testMenu)
    data = (json.dumps(json.loads(testMenu), ensure_ascii=False).encode('utf-8'))

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
    # token = 'TPC0mCeLMJ0CgzIslFIgKvHUSWYxDrFM43Cur9usEboTSt0SEnB0bJGxPPUAVhS0YwkxP3UNCKumaDdZTCGB5Q'
    # token = '8OvyxJGMSuD5R3DEVUcUJVEsT_WIZ3voa1-J0T8-bGrvi7Si69hvCmr6GfV3Ukq6CT_RIEUSw26YTPamYjpYvA'
    # token = 'NqAVFD6EhN6N8U975tE0eD62nUDSb17cdbIniFHFQFOhceHbiBkFvS5D1TRVYS1S0hWxzUlJdrcFY8OvWo3Tyw'
    # token = getAccessToken(aid=APP_ID, asecret=APP_SECRET)
    cmd = "curl -X POST -H Content-Type:application/json -H Cache-Control:no-cache https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s"
    
    import subprocess, shlex

    access_token = 'NqAVFD6EhN6N8U975tE0eD62nUDSb17cdbIniFHFQFOhceHbiBkFvS5D1TRVYS1S0hWxzUlJdrcFY8OvWo3Tyw'
    proc = subprocess.Popen(shlex.split(cmd % (access_token, 'oFZijt11OjA4i3Fq1jSjf1agboxw')), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.stdout.read()
    
    print output

    # {
    #     "total": 2,
    #     "count": 2,
    #     "data": {
    #         "openid": ["oFZijt71j9NzhSqQzVf1_Im3Ucn0", "oFZijt11OjA4i3Fq1jSjf1agboxw"]
    #     },
    #     "next_openid": "oFZijt11OjA4i3Fq1jSjf1agboxw"
    # }
    # postMenu(token)

    # postXML('bind1')
