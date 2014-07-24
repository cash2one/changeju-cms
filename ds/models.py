# coding=utf-8
from django.db import models


class Ziroom_House(models.Model):
    url_id = models.IntegerField(unique=True)
    url = models.CharField(max_length=50)
    title = models.CharField(max_length=100, null=True)
    lng = models.FloatField(default=0)
    lat = models.FloatField(default=0)
    community = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=100, null=True)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=200, null=True)
    tags = models.CharField(max_length=50, null=True)
    comments = models.CharField(max_length=200, null=True)
    last_update = models.DateField(auto_now=True, auto_now_add=True)
    count = models.IntegerField(default=1)


class Homelink_House(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=50)
    homelink_id = models.CharField(max_length=45)
    rent = models.IntegerField()
    house_type = models.CharField(max_length=10)
    building_year = models.CharField(max_length=10)
    pub_date = models.DateField(auto_now=True)
    off_date = models.DateField(auto_now=True)
    area = models.IntegerField()
    community_name = models.CharField(max_length=45)
    last_update = models.DateField(auto_now=True, auto_now_add=True)
    status = models.IntegerField(default=0)

# class Company(models.Model):
#     name = models.CharField(max_length=80, verbose_name='公司名称')
#     area = models.CharField(max_length=15, blank=True, verbose_name='区县')
#     legal_person = models.CharField(max_length=55, blank=True, verbose_name='企业法人')
#     qualification_number = models.CharField(max_length=25, blank=True, verbose_name='物业资质号')
#     qualification_level = models.CharField(max_length=20, blank=True, verbose_name='物业资质等级')

#     def __unicode__(self):
#         return self.name

#     def __str__(self):
#         return self.name
