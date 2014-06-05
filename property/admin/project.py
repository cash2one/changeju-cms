# coding=utf-8

from django.contrib import admin

class ProjectAdmin(admin.ModelAdmin):
	list_filter = ('area', 'qualification_level', 'property_usage', )
	list_display = ('name', 'property_company_name', 'area', 'property_usage', 'address', 'phone', 'qualification_number', 'qualification_level',)
	search_fields = ('name', 'property_company_name',)
	list_per_page = 20
