from django import forms

#Import TinyMCE.
from tinymce.widgets import TinyMCE

from . import models

#class CommentForm(forms.Form):
#    comment = forms.CharField(label='Text', max_length=500)

class CommentForm(forms.ModelForm):

    #Make the comment field use the tinyMCE editor.
    comment = forms.CharField(widget=TinyMCE())

    #Have Django automatically make the form based on the comment model.
    class Meta:
        model = models.Comment

        #Exclude time so that a user can't update it.
        exclude = ['time', 'user']
