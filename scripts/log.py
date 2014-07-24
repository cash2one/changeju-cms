#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hollay
# @Date:   2014-07-02 14:20:13
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-07-02 14:29:12

def run():
	fp = open('/tmp/1.log', 'r')
	nfp = open('/tmp/2.log', 'w')
	lines = fp.readlines()

	spiders = ['Baiduspider/2.0', 'DNSPod-Monitor/1.0', 'Googlebot', 'Sogou web spider/4.0', '360Spider', 'bingbot/2.0']
	
	for line in lines:
		p = False
		for spider in spiders:
			if line.find(spider) > 0:
				p = True
				break
		if p:
			continue

		nfp.write(line)

	fp.close()
	nfp.close()

if __name__ == '__main__':
	run()