from django.db import models
# Create your models here.

#管理员表
class admin(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=100)
    add_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(auto_now=True)

#网站基本信息表
class config(models.Model):
    title = models.CharField(max_length=200, null=True)
    logo = models.ImageField(upload_to='static', null=True)
    description = models.CharField(max_length=200, null=True)
    keywords = models.CharField(max_length=100, null=True)
    about_us = models.TextField(null=True)
    connect_us = models.CharField(max_length=200, null=True)
#留言表
class message(models.Model):
    my_name=models.CharField(max_length=100)
    content=models.TextField()
    add_time=models.DateTimeField(auto_now=True)

#文章分类表
class article_cat(models.Model):
    cat_name=models.CharField(max_length=100)
    add_time=models.DateTimeField(auto_now=True)
    update_time=models.DateTimeField(auto_now=True)
    status=models.IntegerField(default=1)

#文章表
class article(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField()
    count=models.IntegerField()
    desc=models.CharField(max_length=200)
    content=models.TextField()
    sort=models.IntegerField()
    add_time=models.DateTimeField(auto_now=True)
    update_time=models.DateTimeField(auto_now=True)
    cat=models.ForeignKey('article_cat',to_field='id',on_delete=models.CASCADE)