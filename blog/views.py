# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,Http404,JsonResponse
from django.db.models import Q
from datetime import datetime
from django.urls import reverse
from .models import post, Profile,Comment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.contrib import messages
from django.template.loader import render_to_string
# Create your views here.
def post_list(request):
	post_list = post.published.all().order_by('-id')
	query = request.GET.get('q')
	if query:
		post_list = post.published.filter(
		Q(title__icontains=query)|
		Q(author__username=query)|
		Q(body__icontains=query)
		)
	paginator = Paginator(post_list, 8)
	page = request.GET.get('page')
	try:
		posts= paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	if page is None:
		start_index = 0
		end_index = 7
	else:
		(start_index, end_index )= proper_pagination(posts, index=3)

	page_range = list(paginator.page_range)[start_index:end_index]
	context={
	'posts':posts,
	'page_range':page_range,
	}
	return render(request,'blog/post_list.html',context)

def proper_pagination(posts, index):
	start_index = 0
	end_index = 7
	if posts.number>index:
		start_index = posts.number - index
		end_index = start_index + end_index
	return (start_index, end_index)



def post_detail(request,id,slug):
	Post=get_object_or_404(post, id=id, slug=slug )
	comments = Comment.objects.filter(Post=Post, reply=None).order_by('-id')
	if request.method == "POST":
		comment_form = CommentForm(request.POST or None)
		if comment_form.is_valid():
			content = request.POST.get('content')
			reply_id = request.POST.get('comment_id')
			comment_qs = None
			if reply_id:
				comment_qs = Comment.objects.get(id=reply_id)
			comment = Comment.objects.create(Post=Post, user=request.user, content=content, reply=comment_qs)
			comment.save()
			#return HttpResponseRedirect(Post.get_absolute_url())
	else:
		comment_form= CommentForm()
	context={
	'Post':Post,
	'comments': comments,
	'comment_form': comment_form,
	}
	if request.is_ajax():
		html = render_to_string('blog/comments.html', context, request=request)
		return JsonResponse({'form': html})
	return render(request,'blog/post_detail.html',context)


#def like_post(request):
#	Post = get_object_or_404(post, id=request.POST.get('post_id'))
#	Post.likes.add(request.user)
#	return HttpResponseRedirect(post.get_absolute_url())







def post_create(request):
	if request.method == 'POST':
		form=PostCreateForm(request.POST)
		if form.is_valid():
			post=form.save(commit=False)
			post.author = request.user
			post.save()
			messages.success(request, "Post has been successfully created.")
			return redirect('post_list')
	else:
		form=PostCreateForm()
	context={
			'form':form,
			}

	return render(request,'blog/post_create.html', context)


def post_edit(request, id):
	Post = get_object_or_404(post,id=id)
	if Post.author != request.user:
		raise Http404()
	if request.method == "POST":
		form = PostEditForm(request.POST or None, instance=Post)
		if form.is_valid():
			form.save()
			messages.success(request, "{} has been successfully updated!".format(Post.title))
			return HttpResponseRedirect(Post.get_absolute_url())
	else:
		form = PostEditForm(instance=Post)
	context = {
		'form':form,
		'Post':Post,
	}
	return render(request, 'blog/post_edit.html', context)

def post_delete(request, id):
	Post = get_object_or_404(post,id=id)
	if Post.author != request.user:
		raise Http404()
	Post.delete()
	messages.warning(request, "post has been successfully deleted")
	return redirect('post_list')













def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('post_list'))
				else:
					return HttpResponse("User is not active")
			else:
				return HttpResponse("User is none")
	else:
		form = UserLoginForm()

	context = {
		'form':form,
	}
	return render(request, 'blog/login.html', context)

def user_logout(request):
	logout(request)
	return redirect('login')

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST or None)
		if form.is_valid():
			new_user = form.save(commit=False)
			new_user.set_password(form.cleaned_data['password'])
			new_user.save()
			Profile.objects.create(user=new_user)
			return redirect('login')
	else:
		form = UserRegistrationForm()
	context = {
		'form':form,
	}
	return render(request, 'registration/register.html', context)

@login_required
def edit_profile(request):
	if request.method == 'POST':
		user_form = UserEditForm(data=request.POST or None, instance=request.user)
		profile_form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return HttpResponseRedirect(reverse("post_list"))
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)

	context = {
		'user_form':user_form,
		'profile_form':profile_form,
	}
	return render(request, 'blog/edit_profile.html', context)
