from django import forms
from  django.contrib.auth.models import User
# from log.models import userdb
from django.forms import TextInput, EmailInput

from home.models import members


# class loginform(forms.ModelForm):
#     password=forms.CharField(widget=forms.PasswordInput())
#     class Meta():
#         model=User
#         fields=('username','password')
        
#         # help_texts = {
#         #     'username': None,
        
#         # }
# class signupform(forms.ModelForm):
#     password=forms.CharField(widget=forms.PasswordInput())
#     email=forms.EmailField()
#     Phone= forms.IntegerField()
#     # widget=forms.ValidationError
#     Block=forms.CharField()
#     room=forms.IntegerField()
#     flat_type=forms

#     class Meta():
#         model=members,User
#         fields=('first_name','block','flat','flat_type')