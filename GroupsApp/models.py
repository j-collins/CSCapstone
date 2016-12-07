"""GroupsApp Models

Created by Naman Patwari on 10/10/2016.
"""
from django.db import models
from AuthenticationApp.models import MyUser, Student
from ProjectsApp.models import Project
from UniversitiesApp.models import University
from CompaniesApp.models import Company
from CommentsApp.models import Comment

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    members = models.ManyToManyField(MyUser)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name