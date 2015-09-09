#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-08-27 17:38:17
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-08-27 17:59:01


微信用户
WechatUser

WechatGroup

WechatProfile

微信公众账号
WechatAccount
	appid, appsecret, access_token
微信返回码
WechatCode

微信媒体文件
WechatMedia
	::upload
	::download

WechatMediaImage
WechatMediaVoice
WechatMediaVideo
WechatMediaThumb

微信消息
WechatMessage
	文本
	图片
	语音
	视频
	地理位置
	链接信息

	事件推送
		关注/取消关注
		扫描带参数二维码
		用户已关注时的事件推送
		上报地理位置事件
		自定义菜单事件
		点击菜单跳转链接时的事件推送

	接收语音识别结果

WechatResponse
	文本消息
	图片消息
	语音消息
	视频消息
	音乐消息
	图文消息

客服消息
WechatCustomResponse
群发消息
WechatMassResponse