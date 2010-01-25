from django import forms
#from django.conf import settings

from django.contrib.auth.models import User

#import re

class RegisterForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', max_length = 30, label = 'Username', 
                                error_message = 'The username must contain only letters, numbers and underscores.')
    email = forms.EmailField(label = 'Email Address')
    
    def clean_username(self):
        '''
        We need to check that username is unique.
        '''
        username = self.cleaned_data['username']
        try:
            User.objects.get(username = username)
        except User.DoesNotExist:
            #This is good, means that we can use this username:
            return username

        #Otherwise, username exists. We can't use it.
        raise forms.ValidationError(
                "Username already exists! Please choose another one."
              )

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length = 30, label = 'First Name')
    last_name = forms.CharField(max_length = 30, label = 'Last Name')
    #Maybe make email unique.
    email = forms.EmailField(label = 'Email Address')
    
