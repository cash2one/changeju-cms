# coding=utf-8

from django.contrib import admin

class CompanyAdmin(admin.ModelAdmin):
	list_filter = ('area', 'qualification_level',)
	list_display = ('name', 'area', 'legal_person', 'qualification_number', 'qualification_level',)
	search_fields = ('name',)
	list_per_page = 20
