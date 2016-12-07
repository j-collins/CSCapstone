"""
BookmarksApp Views

"""

from django.shortcuts import render

from . import models


# Create your views here.

#Wrote getBookmarks function.
def getBookmarks(request):
    if request.user.is_authenticated():


        user_object = models.MyUser.objects.get(email__exact=request.user.email)

        bookmarks_list = models.Bookmark.objects.filter(user=user_object)
        print(bookmarks_list)

        context = {
            'bookmarksList' : bookmarks_list
        }
        return render(request, 'bookmarksList.html', context)
    return render(request, 'autherror.html')


#Wrote createBookmark function.
def createBookmark(request):
    #If user is logged in...
    if request.user.is_authenticated():
        #Get project name from URL.
        project_name = request.GET.get('name', 'None')

        #Get project object with given project_name.
        project_object = models.Project.objects.get(name__exact=project_name)
        
        #Get user object with given current logged in user email.
        user_object = models.MyUser.objects.get(email__exact=request.user.email)

        #Create a new bookmark with provided user_object and project_object.
        new_bookmark = models.Bookmark(user=user_object, project=project_object)

        #Save the bookmark in the database.
        new_bookmark.save()

        #The user has bookmarked the project.
        user_has_bookmarked = True

        #Context updated to include project_object and variable for if user has bookmarked
        #the project.
        context = {
            'project' : project_object,
            'userHasBookmarked' : user_has_bookmarked,
        }
        #Render using project.htlm file from ProjectsApp.
        return render(request, 'project.html', context)
    return render(request, 'autherror.html')
    
    
def removeBookmark(request):
    #Code follows logic and comments from above createBookmark function.
    if request.user.is_authenticated():

        project_name = request.GET.get('name', 'None')
        
        project_object = models.Project.objects.get(name__exact=project_name)
        
        user_object = models.MyUser.objects.get(email__exact=request.user.email)

        #Get the bookmark_object using the user_object an project_object.
        bookmark_object = models.Bookmark.objects.get(user=user_object, project=project_object)

        #Delete bookmark from database.
        bookmark_object.delete()

        #User has unbookmarked the project.
        user_has_bookmarked = False

        context = {
            'project' : project_object,
            'userHasBookmarked': user_has_bookmarked,
        }
        return render(request, 'project.html', context)
    return render(request, 'autherror.html')
  





