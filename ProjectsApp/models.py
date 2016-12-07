"""ProjectsApp Models

Created by Harris Christiansen on 10/02/16.
"""
from django.db import models
from CompaniesApp.models import Company
from AuthenticationApp.models import MyUser, Engineer
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000, default='')
    created_at = models.DateTimeField('date created', default='2000-10-10')
    updated_at = models.DateTimeField('date updated', default='2000-10-10')
    company =models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, null=True)
    programming_language = models.CharField(max_length=1000, default='')
    years_of_experience = models.IntegerField( default=0)
    speciality = models.CharField(max_length=1000, default='')

    # TODO Task 3.5: Add field for company relationship
    # TODO Task 3.5: Add fields for project qualifications (minimum required: programming language, years of experience, speciality)

    def __str__(self):
        return self.name
    def get_description(self):
        return self.description
    def get_created_at(self):
        return self.created_at
    def get_updated_at(self):
        return self.updated_at
    def get_programming_language(self):
        return self.programming_language
    def get_years_of_experience(self):
        return self.years_of_experience
    def get_speciality(self):
        return self.speciality
    def get_company(self):
        return self.company

