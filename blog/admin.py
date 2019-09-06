# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import post, Profile,Comment
# Register your models here.
class postAdmin(admin.ModelAdmin):
	list_display=('title','slug','author','status')
	list_filter=('status','created','updated')
	search_fields=('author__username','title')
	prepopulated_fields={'slug':('title',)}
	list_editable=('status',)

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user','dob','photo')



admin.site.register(post, postAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment)
