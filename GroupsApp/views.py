"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render, redirect
from . import models
from . import forms
from AuthenticationApp.models import Student
from ProjectsApp.models import Project
from CompaniesApp.models import Company
from django.shortcuts import get_object_or_404
from GroupsApp.models import Group

def getGroups(request):
    #if request.user in Student.objects.all():
        if request.user.is_authenticated():
            groups_list = models.Group.objects.all()
            context = {
            'groups' : groups_list,
            }
            return render(request, 'groups.html', context)
        return render(request, 'autherror.html')

def getGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        print(in_name)
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact = request.user.email)

        print(is_member)
        project1 = None
        project2 = None
        project3 = None
        in_project = None
        company = None
        project_assigned = False
        company_assigned = False
        print("herererer")
        if in_group.project_id != None:
            print ("hererere+proj")
            project_assigned = True
            project_id = in_group.project_id
            in_project = models.Project.objects.get(id__exact=project_id)
            company_id = in_project.company_id
            if company_id != None:
                company = models.Company.objects.get(id__exact=company_id)
                company_assigned = True
        elif is_member.exists():
            print("here")
            member_list = in_group.members.all()
            years_of_experience = 0
            number_of_members = 0
            #declare a string array.
            for member in member_list:
                user_id = member.id
                student = models.Student.objects.get(user_id__exact=user_id)
                years_of_experience = years_of_experience + student.experience
                number_of_members += 1
            avg_exp = years_of_experience/number_of_members
            print(avg_exp)
            list_project = models.Project.objects.all()
            count = 0
            for project in list_project:
                project_experience = project.years_of_experience
                if project_experience <= avg_exp and count < 3:
                    print("here")
                    count += 1
                    if count == 1:
                        project1 = project
                    if count == 2:
                        project2 = project
                    if count == 3:
                        project3 = project

        context = {
            'group' : in_group,
            'userIsMember': is_member,
            'Project1': project1,
            'Project2': project2,
            'Project3': project3,
            'Project': in_project,
            'Company': company,
            'IsCompany': company_assigned,
            'IsProject': project_assigned,
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    user_type = request.user.get_user_type()
    print(user_type)
    if user_type == 'STUDENT':
        if request.user.is_authenticated():
            return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
            if request.method == 'POST':
                form = forms.GroupForm(request.POST)
                if form.is_valid():
                    if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                        return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!'})
                    new_group = models.Group(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
                    new_group.save()
                    context1 = {
                        'name' : form.cleaned_data['name'],
                    }
                    print(new_group)
                    new_group.members.add(request.user)
                    new_group.save()
                    request.user.group_set.add(new_group)
                    request.user.save()
                    context = {
                        'group': new_group,
                        'userIsMember': True,
                    }
                    return render(request, 'groupformsuccess.html', context1)
            else:
                form = forms.GroupForm()
            return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')
def addStudent(request):
    if request.user.is_authenticated():
            return render(request, 'adduserform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getAddUserSuccess(request):
    if request.user.is_authenticated():
            if request.method == 'POST':
                form = forms.AddUserForm(request.POST)
                if form.is_valid():

                    if models.MyUser.objects.filter(email__exact=form.cleaned_data['email']).exists():

                        if models.Group.objects.filter(name__exact=form.cleaned_data['group']).exists():
                            new_user = models.MyUser.objects.get(email__exact=form.cleaned_data['email'])
                            print(new_user)
                            in_group = models.Group.objects.get(name__exact=form.cleaned_data['group'])
                            if new_user.is_student:
                                print ("hererere")
                                if in_group.members.filter(email__exact=new_user.email).exists() != True:
                                    in_name = request.GET.get('name')
                                    print(in_name)
                                    in_group.members.add(request.user)
                                    in_group.save()
                                    new_user.group_set.add(in_group)
                                    new_user.save()
                                    context = {
                                        'group': in_group,
                                        'userIsMember': True,
                                    }
                                    return render(request, 'addformsuccess.html', context)
                                return render(request, 'adduserform.html', {'error': 'User already a member!!!'})
                            return render(request, 'adduserform.html', {'error' : 'User is not a Student! Only Students can be added to a Group!!!'})
                        return render(request, 'adduserform.html',{'error': 'Group doesnt exists!!!'})
                    return render(request, 'adduserform.html',{'error': 'User is doesnt exists!!!'})
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_student = request.user.is_student
        in_group.members.remove(request.user)
        in_group.save()
        request.user.group_set.remove(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': False,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')

def removeGroup(request):
    if request.user.is_authenticated():
        #Get the group object from the url.
        group_name = request.GET.get('name', 'None')
        group_object = models.Group.objects.get(name__exact=group_name)

        #Delete the group.
        group_object.delete()

        #Redirect to the group list.
        return redirect('/group/all')
    # render error page if user is not logged in
    return render(request, 'autherror.html')
    