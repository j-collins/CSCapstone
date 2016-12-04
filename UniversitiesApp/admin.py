"""
UniversitiesApp Admin

Created by Jacob Dunbar on 11/5/2016.
"""
from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.University)

#Make sure the admin acccount can edit and see courses.
admin.site.register(models.Course)
