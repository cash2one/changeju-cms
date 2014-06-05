# coding=utf-8
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=80)
    area = models.CharField(max_length=15, blank=True)
    legal_person = models.CharField(max_length=55, blank=True)
    qualification_number = models.CharField(max_length=25, blank=True)
    qualification_level = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=80, blank=True)
    area = models.CharField(max_length=45, blank=True)
    property_company_name = models.CharField(max_length=45, blank=True)
    qualification_number = models.CharField(max_length=25, blank=True)
    qualification_level = models.CharField(max_length=10, blank=True)
    property_usage = models.CharField(max_length=10, blank=True)
    property_level = models.CharField(max_length=10, blank=True)
    head = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    finish_date = models.CharField(max_length=10, blank=True)

    company = models.ForeignKey(Company, verbose_name=r'关联的物业公司')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
