#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hollay
# @Date:   2014-07-24 12:46:01
# @Last Modified by:   hollay
# @Last Modified time: 2014-07-24 12:52:24

from django.contrib import admin

from ds.models import Homelink_House
from ds.models import Ziroom_House

from ds.admin.homelink import ZiroomHouseAdmin

admin.site.register(Ziroom_House)
admin.site.register(Homelink_House, ZiroomHouseAdmin)
