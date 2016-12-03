"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from AuthenticationApp.models import Student
from django.shortcuts import get_object_or_404
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
        context = {
            'group' : in_group,
            'userIsMember': is_member,
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
                            if new_user.is_student:                             #NEED TO CHECK IF REQUEST.USER IS A MEMBER OF THE GROUP
                                in_name = request.GET.get('name')               #need to check if the user to be added is already a member or not
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
                    return render(request, 'adduserform.html', {'error' : 'User is not a Student! Only Students can be added to a Group!!!'})
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
    