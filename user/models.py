# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name="名")
    last_name = models.CharField(max_length=150, verbose_name="姓")
    full_name = models.CharField(max_length=16, verbose_name="全名")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.full_name = self.last_name + self.first_name
        super(User, self).save(*args, **kwargs)
