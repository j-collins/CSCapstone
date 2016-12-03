"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render

from . import models

def getProjects(request):
	projects_list = models.Project.objects.all()
	return render(request, 'projects.html', {
        'projects': projects_list,
    })

def getProject(request):
	return render(request, 'project.html')

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
                if form.is_valid():
                    if models.Project.objects.filter(name__exact=form.cleaned_data['name']).exists():
                        return render(request, 'project.html', {'error' : 'Error: That Project name already exists!'})
                    new_project = models.Project(name=form.cleaned_data['name'])
                    new_project.save()
                    context = {
                        'name' : form.cleaned_data['name'],
                    }
                    return render(request, 'projectformsuccess.html', context)
            else:
                form = forms.ProjectForm()
            return render(request, 'projectform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')
