#coding=utf-8

from django.db import models

class Identification(models.Model):
	'''
	'''
	url = models.CharField(max_length=200, verbose_name='图片地址')
	mobile = models.CharField(max_length=20, verbose_name='手机号码')
	mobile_confirm = models.CharField(max_length=20, verbose_name='确认手机号码')