"""GroupsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms

from . import models

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
        model = models.Project
        fields = ('name', 'description', 'years_of_experience', 'programming_language', 'speciality')

    def clean_name(self):
        return self.initial["name"]

    def clean_description(self):
        des = self.cleaned_data.get("description")
        # Check is email has changed
        if des == self.initial["description"]:
            return des
        # Check if email exists before
        try:
            des = self.cleaned_data("description")
            return des
        except:
            raise forms.ValidationError("There was an error, please contact us later")

    def clean_years_of_experience(self):
        years_of_experience = self.intial["years_of_experience"]
        if years_of_experience == self.cleaned_data.get("years_of_experience"):
            years_of_experience = self.cleaned_data.get("years_of_experience")
        return years_of_experience

    def clean_programming_language(self):
        programming_language = self.intial["programming_language"]
        if programming_language == self.cleaned_data.get("programming_language"):
            programming_language = self.cleaned_data.get("programming_language")
        return programming_language

    def clean_speciality(self):
        speciality = self.intial["speciality"]
        if speciality == self.cleaned_data.get("speciality"):
            speciality = self.cleaned_data.get("speciality")
        return speciality
