from django.db import models
from random import choices
from string import ascii_letters
from django.conf import settings
from django.contrib.auth.models import User
from datetime import date,datetime


class Album(models.Model):
    name_album = models.CharField(max_length=30)
    date_update = models.DateTimeField(default=datetime.now())
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status_delete = models.BooleanField(default=False)

class Link(models.Model):
    original_link=models.URLField()
    shortened_link=models.URLField(blank=True,null=True)
    number_random = models.CharField(max_length=20) 
    create_by= models.ForeignKey(User, on_delete=models.CASCADE)
    date_now = models.DateTimeField(default=datetime.now())
    date_update = models.DateTimeField(default=datetime.now())
    check_date = models.BooleanField(default=False)
    ex_date = models.DateTimeField()
    name_album = models.IntegerField()
    key = models.CharField(max_length=20) 
    code = models.ImageField(blank=True,upload_to='code')
    status_delete = models.BooleanField(default=False)
    name_qr = models.CharField(max_length=20) 
    # code = models.ImageField('images/')

    def __str__(self):
        return self.key

class count(models.Model):
    CountShort = models.CharField(max_length =40)
    DateURL = models.DateTimeField(default=datetime.now())
    Link_by= models.ForeignKey(Link,  related_name='Link', on_delete=models.CASCADE)
    Countqr = models.BooleanField(default=False)

    def __str__(self):
        return self.CountShort


class OfficeUser(models.Model):
    email = models.EmailField(max_length = 200)

    def __str__(self):
        return self.email

class Story(models.Model):
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    namepath = models.CharField(max_length=20)
    data = models.CharField(max_length=20)
    date = models.DateTimeField()
    short_url_by = models.ForeignKey(Link,  related_name='Link_Story', on_delete=models.CASCADE)

class test(models.Model):
    name = models.CharField(max_length=20)
    code = models.ImageField('images/')

    def __str__(self):
        return self.name

class log(models.Model):
    log_error_api_api_path = models.CharField(max_length=50)
    log_error_api_api_error = models.CharField(max_length=50)
    log_error_api_client_device = models.CharField(max_length=50)
    log_error_api_client_data = models.CharField(max_length=50)
    log_error_api_method = models.CharField(max_length=50)
    log_error_api_datenow = models.DateTimeField()

    def __str__(self):
        return self.log_error_api_api_path

# class Username(models.Model):
#     password = models.CharField(max_length=50)
#     last_login = models.DateTimeField(default=datetime.now())
#     email = models.EmailField(blank=True)
#     username = models.CharField( max_length=150, blank=True)
#     is_staff = models.BooleanField(default=False)
    # is_superuser = 

