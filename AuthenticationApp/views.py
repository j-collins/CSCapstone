"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


from .forms import LoginForm, RegisterForm, UpdateForm, StudentUpdateForm, ProfessorUpdateForm, EngineerUpdateForm
from .models import MyUser, Student, Professor, Engineer

# Auth Views

def auth_login(request):
	form = LoginForm(request.POST or None)
	next_url = request.GET.get('next')
	if next_url is None:
		next_url = "/"
	if form.is_valid():
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = authenticate(email=email, password=password)
		if user is not None:
			messages.success(request, 'Success! Welcome, '+(user.first_name or ""))
			login(request, user)
			return HttpResponseRedirect(next_url)
		else:
			messages.warning(request, 'Invalid username or password.')
			
	context = {
		"form": form,
		"student_form": None,
		"professor_form" : None,
		"engineer_form" : None,
		"page_name" : "Update",
		"button_value" : "Update",
		"links" : ["logout"],
	}
	return render(request, 'auth_form.html', context)

def auth_logout(request):
	logout(request)
	messages.success(request, 'Success, you are now logged out')
	return render(request, 'index.html')

def auth_register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data) #added brackets - shubhika
		print(form.cleaned_data['user_type']) #added brackets - shubhika

		#Creating a new user, adding user_type.
		new_user = MyUser.objects.create_user(email=form.cleaned_data['email'], 
			password=form.cleaned_data["password2"], 
			first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'],
			user_type=form.cleaned_data['user_type'])

		#Saves user to database.
		new_user.save()	

		#Get user_type from the form data. Form is an object with all the data provided by the user.
		user_type = form.cleaned_data['user_type']
		if user_type == 'STUDENT':
			#Make a new student object.
			profile = Student(user = new_user)
		elif user_type == 'PROFESSOR':
			profile = Professor(user = new_user)
		elif user_type == 'ENGINEER':
			profile = Engineer(user = new_user)
		#Save the profile.
		profile.save()

		login(request, new_user);
		messages.success(request, 'Success! Your account was created.')
		return render(request, 'index.html')

	context = {
		"form": form,
		"page_name" : "Register",
		"button_value" : "Register",
		"links" : ["login"],
	}
	return render(request, 'auth_form.html', context)

@login_required
def update_profile(request):
	form = UpdateForm(request.POST or None, instance=request.user)

	if form.is_valid():
		form.save()
		messages.success(request, 'Success, your profile was saved!')

	#Query the database to get the current user. Good ole Google.
	user = MyUser.objects.get(email=request.user)

	#Get user type.
	user_type = user.get_user_type()

	#Initialize form variables.
	student_form = None
	professor_form = None
	engineer_form = None

	#Get a user_type specific form to display for the user.
	if user_type == "STUDENT":
		student_form = StudentUpdateForm(request.POST or None, instance=request.user)
		if student_form.is_valid():
			student_form.save()
	elif user_type == "PROFESSOR":
		professor_form = ProfessorUpdateForm(request.POST or None, instance=request.user)
		if professor_form.is_valid():
			professor_form.save()
	elif user_type == "ENGINEER":
		engineer_form = EngineerUpdateForm(request.POST or None, instance=request.user)
		if engineer_form.is_valid():
			engineer_form.save()

	#Provide the form data to the auth_form.html template. See provided code above.
	context = {
		"form": form,
		"student_form": student_form,
		"professor_form" : professor_form,
		"engineer_form" : engineer_form,
		"page_name" : "Update",
		"button_value" : "Update",
		"links" : ["logout"],
	}
	return render(request, 'auth_form.html', context)
