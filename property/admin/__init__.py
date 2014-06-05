# coding=utf-8

from django.contrib import admin

from property.models import Company
from property.models import Project

from property.admin.company import CompanyAdmin
from property.admin.project import ProjectAdmin

admin.site.register(Company, CompanyAdmin)
admin.site.register(Project, ProjectAdmin)
