from django.db import models
from django_mongoengine import Document, EmbeddedDocument
from django_mongoengine import fields
from datetime import datetime
from django.urls import reverse
# Create your models here.

class User(Document):

	name = fields.StringField(verbose_name="Full Name", blank=True, max_length=50, unique=False)
	email = fields.EmailField(verbose_name="Email", blank=True, unique=False)
	phoneno = fields.LongField(verbose_name="Phone Number", min_value=1000000000, max_value=9999999999, unique=True)
	passwd = fields.StringField(verbose_name="Password")
	last_sign_in = fields.DateTimeField(verbose_name="Last Sign In", default=datetime.now())
	birth_date = fields.DateField(verbose_name="Birth Date", blank=True)
	passport = fields.StringField(verbose_name="Passport Number", max_length=10, unique=False)
	img = fields.ImageField(verbose_name="Your Image", size=(500,400,False))

	# Generate url for redirection to dashboard
	def get_absolute_url(self):
		return f"/dashboard/"

	# meta = {
	# 	'indexes': ['-created_at', 'slug'],
	# 	'ordering': ['-created_at'],
	# }
