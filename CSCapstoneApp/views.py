"""CSCapstone Views

Created by Harris Christiansen on 9/18/16.
"""
from django.shortcuts import render
from AuthenticationApp.models import MyUser

def getIndex(request):
	try:
		user_object = MyUser.objects.get(email=request.user)
	except:
		user_object = None
	context = {
		'user' : user_object,
	}
	return render(request, 'index.html', context)

def getTable(request):
	return render(request, 'table.html')

def getForm(request):
	return render(request, 'form.html')