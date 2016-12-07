from django.conf.urls import url

from . import views

urlpatterns = [

	url(r'^comments$', views.getComments, name='Comments'),
	#url(r'^commentform$', views.getCommentForm, name='CommentForm'),
	url(r'^addcomment$', views.addComment, name='AddComment'),
    url(r'^comments/remove$', views.removeComment, name="RemoveComment"),
	url(r'^group/addcomments$', views.addComment, name='GroupComment'),
]
