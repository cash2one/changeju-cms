#coding=utf-8

from django.contrib import admin

from manual.models import Identification
from manual.admin.identification import IdentificationAdmin

admin.site.register(Identification, IdentificationAdmin)