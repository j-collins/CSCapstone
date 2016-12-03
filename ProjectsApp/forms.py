"""GroupsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms

class ProjectForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=300)
    #created_at = forms.DateTimeField('date created')
    #updated_at = forms.DateTimeField('date updated')
    programming_language = forms.CharField(max_length=1000)
    years_of_experience = forms.CharField(max_length=1000)
    speciality = forms.CharField(max_length=1000)