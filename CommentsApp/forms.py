from django import forms

#Import TinyMCE.
from tinymce.widgets import TinyMCE

from . import models

#Import bleach to stop XSS attacks.
import bleach
from django.conf import settings

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

    #Add method to defend against XSS attacks for the WYSIWYG editor.
    def clean_comment(self):
        comment = self.cleaned_data.get('comment', '')
        cleaned_text = bleach.clean(comment, settings.BLEACH_VALID_TAGS, settings.BLEACH_VALID_ATTRS, settings.BLEACH_VALID_STYLES)
        return cleaned_text #sanitize html