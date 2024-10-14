from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class User(AbstractBaseUser, PermissionsMixin):
    telegram_id = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_login = None
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

class Phone(models.Model):
     code = models.PositiveSmallIntegerField()
     phone = models.PositiveSmallIntegerField(blank=True)

class City(models.Model):
    city = models.CharField(max_length=255, unique=True)