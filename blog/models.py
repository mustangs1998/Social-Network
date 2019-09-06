# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status="published")

# Create your models here.
class post(models.Model):
	objects = models.Manager()
	published = PublishedManager()

	STATUS=(
	('draft','Draft'),
	('published','Published',)
	)
	title=models.CharField(max_length=30)
	slug=models.SlugField(max_length=30)
	author=models.ForeignKey(User, related_name='blog_posts')
	body=models.TextField()
	likes=models.ManyToManyField(User, related_name="likes", blank=True)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)
	status=models.CharField(max_length=10, choices=STATUS, default='draft')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("post_detail", args=[self.id , self.slug])

@receiver(pre_save, sender=post)
def pre_save_slug(sender, **kwargs):
	slug=slugify(kwargs['instance'].title)
	kwargs['instance'].slug=slug


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	dob = models.DateTimeField(null=True, blank=True)
	photo = models.ImageField(null=True, blank=True)

	def __str__(self):
		return "Profile of user {}".format(self.user.username)

class Comment(models.Model):
	Post = models.ForeignKey(post)
	user = models.ForeignKey(User)
	reply = models.ForeignKey('Comment', null=True, related_name="replies")
	content = models.TextField(max_length=160)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{}-{}'.format(self.Post.title, str(self.user.username))
