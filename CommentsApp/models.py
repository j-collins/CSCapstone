from __future__ import unicode_literals

from django.db import models

from AuthenticationApp.models import MyUser

# Create your models here.

class Comment(models.Model):
    time = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    group_name = models.CharField(max_length=30, default='')