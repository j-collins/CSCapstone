"""
BookmarksApp Models

"""

from __future__ import unicode_literals

from django.db import models
from ProjectsApp.models import Project
from AuthenticationApp.models import MyUser


#Create Bookmark model. 
class Bookmark(models.Model):

    #Create user_id and project_id.
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    project =  models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    #Create getters for user_id and project_id.
    def get_user(self):
        return self.user
    def get_project(self):
        return self.project
 

