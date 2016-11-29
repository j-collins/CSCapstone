"""AuthenticationApp Admin

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import MyUser, Student, Professor, Engineer
from .forms import AdminUserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = AdminUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    #Add user_type.

    list_display = ('email', 'first_name', 'last_name', 'is_admin', 'user_type')
    list_filter = ('is_admin', 'is_active', 'user_type')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        #('Permissions', {'fields': ('is_admin', 'is_active')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'user_type')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            #'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    #ordering = ('email','first_name')
    ordering = ('email','first_name')
    filter_horizontal = ()

# Now register the new UserAdmin...

#Add student/professor/engineer...
#Allows site admin to edit profiles.
admin.site.register(MyUser, UserAdmin)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Engineer)
admin.site.unregister(Group)
