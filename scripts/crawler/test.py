#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2015-09-08 01:07:00
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2015-09-08 01:12:48

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re

s = u'近地铁1号线玉泉路站'
r = re.compile(ur'.*近(.+线)(.+站)')
m = r.match(s)
if m:
	print m.group(1), m.group(2)
