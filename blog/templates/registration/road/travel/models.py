# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class user_contact(models.Model):
	name=models.CharField(max_length=100, blank=True, null=True)
	#lname=models.CharField(max_length=100, blank=True, null=True)
	email=models.CharField(max_length=100, blank=True, null=True)
	phone_no=models.CharField(max_length=100, blank=True, null=True)
	message=models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.name
