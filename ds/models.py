#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hollay
# @Date:   2014-07-24 12:47:17
# @Last Modified by:   hollay
# @Last Modified time: 2014-07-24 15:02:18

from django.db import models


class Ziroom_House(models.Model):
    url_id = models.IntegerField(unique=True)
    url = models.CharField(max_length=50, verbose_name=u'网址')
    title = models.CharField(max_length=100, null=True, verbose_name=u'标题')
    lng = models.FloatField(default=0, verbose_name=u'经度')
    lat = models.FloatField(default=0, verbose_name=u'纬度')
    community = models.CharField(max_length=30, null=True, verbose_name=u'小区名称')
    address = models.CharField(max_length=100, null=True, verbose_name=u'小区地址')
    price = models.IntegerField(default=0, verbose_name=u'价格')
    description = models.CharField(max_length=200, null=True, verbose_name=u'描述')
    tags = models.CharField(max_length=50, null=True, verbose_name=u'标签')
    comments = models.CharField(max_length=200, null=True, verbose_name=u'评价')
    last_update = models.DateField(auto_now=True, auto_now_add=True, verbose_name=u'最后更新时间')
    count = models.IntegerField(default=1)

    class Meta:
        verbose_name = u'自如友家房源信息'
        verbose_name_plural = u'自如友家房源信息'

class Homelink_House(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'标题')
    url = models.CharField(max_length=50)
    homelink_id = models.CharField(max_length=45)
    rent = models.IntegerField(verbose_name=u'租金')
    house_type = models.CharField(max_length=10, verbose_name=u'房型')
    building_year = models.CharField(max_length=10, verbose_name=u'建筑年代')
    pub_date = models.DateField(auto_now=True, verbose_name=u'发布日期')
    off_date = models.DateField(auto_now=True, verbose_name=u'下架日期')
    area = models.IntegerField(verbose_name=u'房屋面积')
    community_name = models.CharField(max_length=45, verbose_name=u'小区名称')
    last_update = models.DateField(auto_now=True, auto_now_add=True, verbose_name=u'最后更新')
    status = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'链家房源信息'
        verbose_name_plural = u'链家房源信息'
