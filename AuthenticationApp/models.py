"""AuthenticationApp Models

Created by Naman Patwari on 10/4/2016.
"""

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.core.validators import RegexValidator

#Used for drop-down list of user_types.
USER_TYPES = (
    ("STUDENT", "Student"),
    ("PROFESSOR", "Professor"),
    ("ENGINEER", "Engineer"),
)

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email=None, password=None, first_name=None, last_name=None, user_type=None):
        if not email:
            raise ValueError('Users must have an email address')

        #We can safetly create the user
        #Only the email field is required
        user = self.model(email=email,user_type=user_type)
        user.set_password(password)

        user.first_name = first_name
        user.last_name = last_name

        #If first_name is not present, set it as email's username by default
        if first_name is None or first_name == "" or first_name == '':                                
            user.first_name = email[:email.find("@")]

        if user_type == 'STUDENT':
            user.is_student = True
        if user_type == 'ENGINEER':
            user.is_professor = True
        if user_type == 'PROFESSOR':
            is_engineer = True


        user.save(using=self._db)
        return user


    def create_superuser(self, email=None, password=None, first_name=None, last_name=None):
        user = self.create_user(email, password=password, first_name=first_name, last_name=last_name)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(
    	max_length=120,
    	null=True,
    	blank=True,
    	)    

    last_name = models.CharField(
    	max_length=120,
    	null=True,
    	blank=True,
    	)

    is_active = models.BooleanField(default=True,)
    is_admin = models.BooleanField(default=False,)

    #Added line to define user_type with choices for student, professor, and engineer.
    user_type = models.CharField(max_length=9, choices = USER_TYPES, default="STUDENT")


    # #New fields added
    is_student = models.BooleanField(default=False,)
    is_professor = models.BooleanField(default=False,)
    is_engineer = models.BooleanField(default=False,)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):        
        return "%s %s" %(self.first_name, self.last_name)

    def get_short_name(self):        
        return self.first_name

    def __str__(self):              #Python 3
        return self.email

    def __unicode__(self):           # Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):        
        return True

    #Define getter for user_type.
    def get_user_type(self):
        return self.user_type

    @property
    def is_staff(self):
        return self.is_admin
    
#     def new_user_reciever(sender, instance, created, *args, **kwargs):
#     	if created:   
     
# Going to use signals to send emails
# post_save.connect(new_user_reciever, sender=MyUser)
             
class Student(models.Model):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        primary_key=True)
    skills = models.CharField(max_length=120, null=True, blank=True)
    experience =  models.CharField(max_length=120, null=True, blank=True)

    def get_full_name(self):
        return "%s %s" %(self.user.first_name, self.user.last_name)

    def get_short_name(self):        
        return self.user.first_name

    def __str__(self):              #Python 3
        return self.user.email

    def __unicode__(self):           # Python 2
        return self.user.email


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):        
        return True
    def get_experience(self):
        return self.experience
    def get_skills(self):
        return self.skills
    @property
    def is_staff(self):
        return False

class Professor(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)

    title = models.CharField(max_length=120, null=True, blank=True)

    #University model already exists, so have a field that points to the Univeristy database table. Use ForeignKey.
    university = models.ForeignKey('UniversitiesApp.University', null=True, on_delete=models.CASCADE)

    #http://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True) # validators should be a list

    def get_full_name(self):
        return "%s %s" %(self.user.first_name, self.user.last_name)

    def get_short_name(self):
        return self.user.first_name

    def __str__(self):              #Python 3
        return self.user.email

    def __unicode__(self):           # Python 2
        return self.user.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return False

class Engineer(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)

    title = models.CharField(max_length=120, null=True, blank=True)

    #Use ForeignKey.
    alma_mater = models.ForeignKey('UniversitiesApp.University', null=True, on_delete=models.CASCADE)
    company = models.ForeignKey('CompaniesApp.Company', null=True, on_delete=models.CASCADE)

    #http://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True) # validators should be a list

    def get_full_name(self):
        return "%s %s" %(self.user.first_name, self.user.last_name)

    def get_short_name(self):
        return self.user.first_name

    def __str__(self):              #Python 3
        return self.user.email

    def __unicode__(self):           # Python 2
        return self.user.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return False