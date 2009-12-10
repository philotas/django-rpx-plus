from django import forms
#from django.conf import settings

from django.contrib.auth.models import User

#import re

class RegisterForm(forms.Form):
    username = forms.CharField(max_length = 30, label = 'Username')
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

