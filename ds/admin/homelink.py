#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hollay
# @Date:   2014-07-24 12:47:17
# @Last Modified by:   hollay
# @Last Modified time: 2014-07-24 13:40:42
from django.contrib import admin


class HomelinkHouseAdmin(admin.ModelAdmin):
    list_filter = ('house_type', )
    list_display = ('community_name', 'house_type',
                    'area', 'rent', 'building_year', 'url', 'title')
    search_fields = ('community_name', 'house_type',)
    list_per_page = 20


class ZiroomHouseAdmin(admin.ModelAdmin):
    list_display = ('community', 'price', 'description',
                    'tags', 'title', 'url', 'comments', 'last_update')
    search_fields = ('community', 'description', 'tags', 'title',)
    list_per_page = 20
