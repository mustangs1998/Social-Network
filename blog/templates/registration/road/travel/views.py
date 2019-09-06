# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse
from travel.models import user_contact
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def first(request):
	return render(request,'travel/first.html')
	
def last(request):
	return render(request,'travel/last.html')	

def pack(request):
	if request.method == 'POST' :
		return render(request,'travel/last.html')
	else:
		return render(request,'travel/pack.html')
	
def index(request):
	if request.method == 'POST' :
		name=request.POST.get('name')
		#lname=request.POST.get('last_name')
		email=request.POST.get('email')
		phone_no=request.POST.get('phone_no')
		message=request.POST.get('message')
		
		a=user_contact(name=name,email=email,phone_no=phone_no,message=message)
		
		a.save()
		return render(request,'travel/index.html')
	
	else:
		return render(request,'travel/index.html')
def signup(request):
	if request.method == 'POST':
		form=UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			raw_password=form.cleaned_data.get('password1')
			user=authenticate(username=username,password=raw_password)
			login(request,user)
			return redirect('/pack/')
	else:
		form=UserCreationForm()
	return render(request,'travel/signup.html',{'form':form})
