"""GroupsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms

from .models import Project

class ProjectForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=300)
    #created_at = forms.DateTimeField('date created')
    #updated_at = forms.DateTimeField('date updated')
    programming_language = forms.CharField(max_length=1000)
    years_of_experience = forms.CharField(max_length=1000)
    speciality = forms.CharField(max_length=1000)

class AddGroupForm(forms.Form):
    group = forms.CharField(max_length=1000)
    project = forms.CharField(max_length=1000)

class Update_Form(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('description', 'years_of_experience', 'programming_language', 'speciality')

    def clean_description(self):
            des = self.cleaned_data["description"]
            return des

    def clean_years_of_experience(self):
            years_of_experience = self.cleaned_data["years_of_experience"]
            return years_of_experience

    def clean_programming_language(self):
            programming_language = self.cleaned_data["programming_language"]
            return programming_language

    def clean_speciality(self):
        speciality = self.cleaned_data["speciality"]
        return speciality
