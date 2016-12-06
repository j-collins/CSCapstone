"""
UniversitiesApp Forms

Created by Jacob Dunbar on 11/5/2016.
"""
from django import forms

from .models import Course

from AuthenticationApp.models import Student

class UniversityForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    photo = forms.ImageField(label='Photo')
    description = forms.CharField(label='Description', max_length=300)
    website = forms.CharField(label='Website', max_length = 300)

class CourseForm(forms.Form):
	tag = forms.CharField(label='Tag', max_length=10)
	name = forms.CharField(label='Name', max_length=50)
	description = forms.CharField(label='Description', max_length=300)

class CourseUpdateForm(forms.ModelForm):

	#Get every student in the database.
	student_list = Student.objects.all()

	#Make a multiple choice field (box with student names), only show students.
	#Code adapted from online tutorials.
	members = forms.ModelMultipleChoiceField(label='Members', queryset=student_list)

	#Adds list of students on course update page. 
	class Meta: 
		model = Course
		exclude = ['university']
