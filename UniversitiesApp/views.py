"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from AuthenticationApp.models import MyUser


def getUniversities(request):
    if request.user.is_authenticated():
        universities_list = models.University.objects.all()
        context = {
            'universities' : universities_list,
        }
        return render(request, 'universities.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        is_member = in_university.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'userIsMember': is_member,
        }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityForm(request):
    if request.user.is_authenticated():
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

#Add a function to update the course information.
def manage(request):
    if request.user.is_authenticated():

        #Get the univeristy from the url.
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)

        #Get the course from the url.
        course_tag = request.GET.get('course', 'None')
        course_object = models.Course.objects.get(tag__exact=course_tag)

        #Make a course form and provide the current course object so the form is pre-filled.
        form = forms.CourseUpdateForm(request.POST or None, instance=course_object)
        if form.is_valid():
            #Get the updated course from the form, but don't commit.
            #https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
            updated_course_object = form.save(commit=False)

            #Remove all of the current course members.
            updated_course_object.members.clear()

            #For each of the students in the form, add them to the course.
            for email in form.cleaned_data['members']:
                student_object = MyUser.objects.get(email__exact=email)
                updated_course_object.members.add(student_object)

            #Save the course updates to the database.
            updated_course_object.save()

            #Go back to the main course view.
            #See if the user is a professor by using a getter.
            user_type = request.user.get_user_type()

            if user_type == 'PROFESSOR' :
                is_professor = True
            else:
                is_professor = False

            context = {
                'university' : in_university,
                'course' : course_object,
                'userIsProfessor' : is_professor, 
            }
            return render(request, 'course.html', context)

        #If the form data was not valid, continue to show the form.
        context = {
            'university' : in_university,
            'form': form,
            'course': course_object,
        }
        return render(request, 'manageform.html', context)

    #If the user is not authenticated, show an error.
    return render(request, 'autherror.html')

def getUniversityFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.UniversityForm(request.POST, request.FILES)
            if form.is_valid():
                if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'universityform.html', {'error' : 'Error: That university name already exists!'})
                new_university = models.University(name=form.cleaned_data['name'], 
                                             photo=request.FILES['photo'],  
                                             description=form.cleaned_data['description'],
                                             website=form.cleaned_data['website'])
                new_university.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'universityformsuccess.html', context)
            else:
                return render(request, 'universityform.html', {'error' : 'Error: Photo upload failed!'})
        else:
            form = forms.UniversityForm()
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.add(request.user)
        in_university.save();
        request.user.university_set.add(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': True,
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')
    
def unjoinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.remove(request.user)
        in_university.save();
        request.user.university_set.remove(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': False,
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')
    
def getCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        is_member = in_course.members.filter(email__exact=request.user.email)

        #See if the user is a professor by using a getter.
        user_type = request.user.get_user_type()

        if user_type == 'PROFESSOR' :
            is_professor = True
        else:
            is_professor = False

        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse' : is_member,
            'userIsProfessor' : is_professor, 
        }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

def courseForm(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		context = {
			'university': in_university,
		}
		return render(request, 'courseform.html', context)
    # render error page if user is not logged in
	return render(request, 'autherror.html')

def addCourse(request):
    #See if the user is a professor before adding the course.
    user_type = request.user.get_user_type()
    if (user_type == 'PROFESSOR'):
        if request.user.is_authenticated():
            if request.method == 'POST':
                form = forms.CourseForm(request.POST)
                if form.is_valid():
                    print("Form is valid!")
                    in_university_name = request.GET.get('name', 'None')
                    in_university = models.University.objects.get(name__exact=in_university_name)
                    if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
                        return render(request, 'courseform.html', {'error' : 'Error: That course tag already exists at this university!'})
                    new_course = models.Course(tag=form.cleaned_data['tag'],
                                               name=form.cleaned_data['name'],
                                               description=form.cleaned_data['description'],
                                               university=in_university)
                    new_course.save()
                    in_university.course_set.add(new_course)
                    is_member = in_university.members.filter(email__exact=request.user.email)
                    context = {
                        'university' : in_university,
                        'userIsMember': is_member,
                    }
                    return render(request, 'university.html', context)
                else:
                    return render(request, 'courseform.html', {'error' : 'Undefined Error!'})
            else:
                form = forms.CourseForm()
                return render(request, 'courseform.html')
            # render error page if user is not logged in
        return render(request, 'autherror.html')
    #If the user is not a professor, show an error screen.
    return render(request, 'professorerror.html')

def removeCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.delete()
		is_member = in_university.members.filter(email__exact=request.user.email)
		context = {
			'university' : in_university,
			'userIsMember' : is_member,
		}
		return render(request, 'university.html', context)
	# render error page if user is not logged in
	return render(request, 'autherror.html')

def joinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.members.add(request.user)
		in_course.save();
		request.user.course_set.add(in_course)
		request.user.save()
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse': True,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def unjoinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.members.remove(request.user)
		in_course.save();
		request.user.course_set.remove(in_course)
		request.user.save()
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse': False,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')
