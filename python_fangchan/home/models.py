

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Anjuke(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    img_urls = models.CharField(max_length=255, blank=True, null=True)
    typ = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    chengshi = models.ForeignKey('Csfl', models.DO_NOTHING, blank=True, null=True)
    addr = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'anjuke'

class AnjukeBj(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    img_urls = models.CharField(max_length=255, blank=True, null=True)
    typ = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    chengshi = models.ForeignKey('Csfl', models.DO_NOTHING, blank=True, null=True)
    addr = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'anjuke_bj'

class AnjukeSh(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    img_urls = models.CharField(max_length=255, blank=True, null=True)
    typ = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    chengshi = models.ForeignKey('Csfl', models.DO_NOTHING, blank=True, null=True)
    addr = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'anjuke_sh'

class AnjukeTj(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    img_urls = models.CharField(max_length=255, blank=True, null=True)
    typ = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    chengshi = models.ForeignKey('Csfl', models.DO_NOTHING, blank=True, null=True)
    addr = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'anjuke_tj'

class Csfl(models.Model):
    chengshi_id = models.IntegerField(blank=True, null=True)
    cs_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'csfl'

