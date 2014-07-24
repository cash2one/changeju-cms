#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hollay
# @Date:   2014-07-24 12:46:01
# @Last Modified by:   hollay
# @Last Modified time: 2014-07-24 13:37:22

from django.contrib import admin

from ds.models import Homelink_House
from ds.models import Ziroom_House

from ds.admin.homelink import ZiroomHouseAdmin
from ds.admin.homelink import HomelinkHouseAdmin

admin.site.register(Ziroom_House, ZiroomHouseAdmin)
admin.site.register(Homelink_House, HomelinkHouseAdmin)
