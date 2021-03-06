"""AuthenticationApp Forms
Created by Naman Patwari on 10/4/2016.
"""
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import MyUser, Student, Professor, Engineer

#Import TinyMCE.
from tinymce.widgets import TinyMCE

#Import bleach to stop XSS attacks.
import bleach
from django.conf import settings

#Import USER_TYPES.
from .models import USER_TYPES


class LoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    """A form to creating new users. Includes all the required
    fields, plus a repeated password."""
    email = forms.CharField(label='Email', widget=forms.EmailInput, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True)

    firstname = forms.CharField(label="First name", widget=forms.TextInput, required=False)
    lastname = forms.CharField(label="Last name", widget=forms.TextInput, required=False)

    # Add user_type to the registration form. Drop-down selection.
    user_type = forms.ChoiceField(choices=USER_TYPES, required=True)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        #raise forms.ValidationError(email)
        # Check if email exists before
        try:
            exists = MyUser.objects.get(email=email)
            raise forms.ValidationError("This email has already been taken")
        except MyUser.DoesNotExist:
            return email
        except:
            raise forms.ValidationError("There was an error, please contact us later")


class UpdateForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'first_name', 'last_name')

    def clean_password(self):
        return self.initial["password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Check is email has changed
        if email == self.initial["email"]:
            return email
        # Check if email exists before
        try:
            exists = MyUser.objects.get(email=email)
            raise forms.ValidationError("This email has already been taken")
        except MyUser.DoesNotExist:
            return email
        except:
            raise forms.ValidationError("There was an error, please contact us later")

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        # Check is email has changed
        if first_name is None or first_name == "" or first_name == '':
            email = self.cleaned_data.get("email")
            return email[:email.find("@")]
        return first_name


# Add Meta to update the profiles.
class StudentUpdateForm(forms.ModelForm):

    #Make the about field use the tinyMCE editor.
    about = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Student
        exclude = ['user']

        def clean_skills(self):
            skills = self.cleaned_data.get("skills")
            if skills == self.initial["skills"]:
                return skills
            try:
                return skills
            except:
                raise forms.ValidationError("There was an error, please contact us later")

        def clean_experience(self):
            experience = self.cleaned_data.get("experience")
            if experience == self.initial["experience"]:
                return experience
            try:
                return experience
            except:
                raise forms.ValidationError("There was an error, please contact us later")
        
        #Add method to defend against XSS attacks for the WYSIWYG editor.
        def clean_about(self):
            about = self.cleaned_data.get('about', '')
            cleaned_text = bleach.clean(about, settings.BLEACH_VALID_TAGS, settings.BLEACH_VALID_ATTRS, settings.BLEACH_VALID_STYLES)
            return cleaned_text #sanitize html

class ProfessorUpdateForm(forms.ModelForm):

    #Make the about field use the tinyMCE editor.
    about = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Professor
        exclude = ['user']

    #Add method to defend against XSS attacks for the WYSIWYG editor.
    def clean_about(self):
        about = self.cleaned_data.get('about', '')
        cleaned_text = bleach.clean(about, settings.BLEACH_VALID_TAGS, settings.BLEACH_VALID_ATTRS, settings.BLEACH_VALID_STYLES)
        return cleaned_text #sanitize html


class EngineerUpdateForm(forms.ModelForm):

    #Make the about field use the tinyMCE editor.
    about = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Engineer
        exclude = ['user']

    #Add method to defend against XSS attacks for the WYSIWYG editor.
    def clean_about(self):
        about = self.cleaned_data.get('about', '')
        cleaned_text = bleach.clean(about, settings.BLEACH_VALID_TAGS, settings.BLEACH_VALID_ATTRS, settings.BLEACH_VALID_STYLES)
        return cleaned_text #sanitize html

"""Admin Forms"""


class AdminUserCreationForm(forms.ModelForm):
    """A form for Admin to creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(AdminUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for Admin for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        # fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin')
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]