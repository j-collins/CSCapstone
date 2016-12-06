"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render
from . import forms

from . import models
from . import forms
from GroupsApp.models import Group

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
        flag = False
        if request.user.id == in_project.engineer_id:
            flag = True
        group = False
        groups_list = Group.objects.all()
        for in_group in groups_list:
            if in_group.members.filter(email__exact=request.user.email).exists():
                group = True
        context = {
            'project' : in_project,
            'userIsMember': flag,
            'in_group' : group,
        }
        return render(request, 'project.html', context)
    return render(request, 'autherror.html')

def getProjectForm(request):
	user_type = request.user.get_user_type()
	print(user_type)
	if user_type == 'ENGINEER':
		if request.user.is_authenticated():
			return render(request, 'projectform.html')
	# render error page if user is not logged in
	return render(request, 'autherror.html')

def getAddGroup(request):
    if request.user.is_authenticated():
            return render(request, 'addgroupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getAddGroupSuccess(request):
    if request.user.is_authenticated():
            if request.method == 'POST':
                form = forms.AddGroupForm(request.POST)
                print(form)
                if form.is_valid():
                    if Group.objects.filter(name__exact=form.cleaned_data['group']).exists():
                        if models.Project.objects.filter(name__exact=form.cleaned_data['project']).exists() is not True:
                            return render(request, 'autherror.html', {'error': 'project doesnt exists'})
                        project = models.Project.objects.get(name__exact=form.cleaned_data['project'])
                        in_group = Group.objects.get(name__exact=form.cleaned_data['group'])
                        #check if user is a group member
                        if in_group.members.filter(myuser_id__exact=request.user.id):
                            if in_group.project_id == None:
                                in_group.project_id = project.id
                                print(in_group.project_id)
                                in_group.save()
                                print(in_group.project_id)
                                context = {
                                    'project': project,
                                }
                                return render(request, 'project.html', context)
                            return render(request, 'addgroupform.html', {'error': 'Group has a project!! Only one project per group'})
                        return render(request,'addgroupform.html', {'error' : 'You are not a member of this group!!!'} )
                    return render(request, 'addgroupform.html', {'error' : 'Group does not exisits!!!'})
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def update_project(request):
	in_name = request.GET.get('name', 'None')
	form = forms.Update_Form(request.POST or None, instance=request.user)
	if form.is_valid():
		form.save()
		messages.success(request, 'Success, your profile was saved!')
	user = models.Project.objects.get(name=in_name)
	context = {
		"form": form,
		"page_name" : "Update",
		"button_value" : "Update",
		"links" : ["logout"],
	}
	return render(request, 'authform.html', context)

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
                    engineer = models.Engineer.objects.filter(user_id__exact=request.user.id)
                    company_id = engineer.company_id
                    new_project = models.Project(name=form.cleaned_data['name'], description=form.cleaned_data['description'], programming_language=form.cleaned_data['programming_language'], years_of_experience=form.cleaned_data['years_of_experience'], speciality=form.cleaned_data['speciality'], engineer_id= request.user.id, company_id=company_id)
                    new_project.save()
                    context = {
                        'name' : form.cleaned_data['name'],
                    }
                    return render(request, 'projectformsuccess.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')
