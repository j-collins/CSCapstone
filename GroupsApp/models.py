"""GroupsApp Models

Created by Naman Patwari on 10/10/2016.
"""
from django.db import models
from AuthenticationApp.models import MyUser, Student
from ProjectsApp.models import Project

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    members = models.ManyToManyField(Student)    
    project = models.OneToOneField(        
	Project,
        on_delete=models.CASCADE,
        primary_key=True)
    
    def __str__(self):
        return self.name