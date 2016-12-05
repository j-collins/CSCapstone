"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render
from . import forms

from . import models
from . import forms

from BookmarksApp.models import Bookmark

def getProjects(request):
	projects_list = models.Project.objects.all()
	return render(request, 'projects.html', {
        'projects': projects_list,
    })

def getProject(request):
    if request.user.is_authenticated():

        in_name = request.GET.get('name', 'None')

        print(in_name)

        in_project = models.Project.objects.get(name__exact=in_name)

        #Get the user_object by searching for the exact email.
        user_object = models.MyUser.objects.get(email__exact=request.user.email)

        try:
            #Get the bookmark_object using the user_object and in_project object.
            bookmark_object = Bookmark.objects.get(user=user_object, project=in_project)
        except Bookmark.DoesNotExist:
            bookmark_object = None

        #If an object was returned...
        if bookmark_object != None:
            #User has bookmarked the project.
            user_has_bookmarked = True
        else:
            #User has not bookmarked the project.
            user_has_bookmarked = False

        context = {
            'project' : in_project,
            'userHasBookmarked' : user_has_bookmarked,
        }
        #Render project page with updated button. 
        return render(request, 'project.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')
    
def getProjectForm(request):
	user_type = request.user.get_user_type()
	print(user_type)
	if user_type == 'ENGINEER':
		if request.user.is_authenticated():
			return render(request, 'projectform.html')
	# render error page if user is not logged in
	return render(request, 'autherror.html')

def getProjectFormSuccess(request):
    if request.user.is_authenticated():
            if request.method == 'POST':
                form = forms.ProjectForm(request.POST)
                print(form.is_valid())
                print(form)
                if form.is_valid():
                    print('heremm!!')
                    if models.Project.objects.filter(name__exact=form.cleaned_data['name']).exists():
                        return render(request, 'projectform.html', {'error' : 'Error: That Project name already exists!'})
                    new_project = models.Project(name=form.cleaned_data['name'])
                    new_project.save()
                    context = {
                        'name' : form.cleaned_data['name'],
                    }
                    return render(request, 'projectformsuccess.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')
