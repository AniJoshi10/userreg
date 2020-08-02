from django_mongoengine import forms
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django import forms as f
from .models import *

class SignupForm(forms.DocumentForm):

	# Birth date widget and Password confirmation fields.
	YEARS= [x for x in range(1940,2010)]
	birth_date= f.DateField(label='What is your birth date?', widget=f.SelectDateWidget(years=YEARS))
	password = f.CharField(widget = f.PasswordInput, validators=[validate_password])
	confirm_password = f.CharField(widget = f.PasswordInput, validators=[validate_password])
	
	class Meta:
		document = User
		exclude = ('passwd', 'last_sign_in')

class LoginForm(forms.DocumentForm):
	
	password = f.CharField(label='Password', widget = f.PasswordInput)
	
	class Meta:
		document = User
		fields = ('phoneno',)

class PasswordForm(forms.DocumentForm):

	# Password fileds for old and new passwords with confirmation field for new password.
	old_password = f.CharField(label='Old Password', widget = f.PasswordInput)
	new_password = f.CharField(label='New Password', widget = f.PasswordInput, validators=[validate_password])
	confirm_new_password = f.CharField(label='Confirm New Password', widget = f.PasswordInput)
	
	class Meta:
		document = User
		fields = ()