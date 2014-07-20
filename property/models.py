# coding=utf-8
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=80, verbose_name='公司名称')
    area = models.CharField(max_length=15, blank=True, verbose_name='区县')
    legal_person = models.CharField(max_length=55, blank=True, verbose_name='企业法人')
    qualification_number = models.CharField(max_length=25, blank=True, verbose_name='物业资质号')
    qualification_level = models.CharField(max_length=20, blank=True, verbose_name='物业资质等级')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=80, verbose_name='项目名称')
    address = models.CharField(max_length=80, blank=True, verbose_name='项目地址')
    area = models.CharField(max_length=45, blank=True, verbose_name='区县')
    property_company_name = models.CharField(max_length=45, blank=True, verbose_name='物业公司')
    qualification_number = models.CharField(max_length=25, blank=True, verbose_name='物业资质号')
    qualification_level = models.CharField(max_length=10, blank=True, verbose_name='物业资质等级')
    property_usage = models.CharField(max_length=10, blank=True, verbose_name='物业用途')
    property_level = models.CharField(max_length=10, blank=True, verbose_name='物业等级')
    head = models.CharField(max_length=10, blank=True, verbose_name='负责人')
    phone = models.CharField(max_length=30, blank=True, verbose_name='联系电话')
    finish_date = models.CharField(max_length=10, blank=True, verbose_name='项目完成时间')

    company = models.ForeignKey(Company, verbose_name=r'关联的物业公司')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
