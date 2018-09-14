from django.db import models
import datetime
from django.utils import timezone

class Coinbar(models.Model):

    m_symbol = models.CharField(max_length=40,default='none',unique=True)#bitstampbtc
    m_name = models.CharField(max_length=30,default='none') #bitstamp
    m_coin = models.CharField(max_length=10,default='none') #btc
    m_price = models.FloatField(default=0,null=True)
    m_24hprice = models.FloatField(default=0,null=True)
    m_24hvol = models.FloatField(default=0,null=True)
    m_24hchange = models.CharField(max_length=25,null=True)
    m_24hchangepercent = models.CharField(max_length=10,null=True)
    m_updatetime =  models.CharField(max_length=25,null=True)#2 hours ago or just now
    m_website = models.CharField(max_length=60,null=True)
    m_area = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.m_symbol

class Modelupdatetime(models.Model):
    m_coinexchanges = models.DateTimeField()
    m_coinbar = models.DateTimeField()

class Exchanges(models.Model):
    m_name = models.CharField(max_length=30,default='none') #bitstamp
    m_website = models.CharField(max_length=20,null=True)
    m_area = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.m_symbol
# Create your models here.
