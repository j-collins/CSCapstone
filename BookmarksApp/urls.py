"""
BookmarksApp URL Configuration
"""
from django.conf.urls import url

from . import views

#Defining urls to associate with the bookmark views.
urlpatterns = [
    url(r'^bookmark/create$', views.createBookmark, name='createBookmark'),
    url(r'^bookmark/remove$', views.removeBookmark, name='removeBookmark'),
    url(r'^bookmark/all$', views.getBookmarks, name='getBookmarks'),

]