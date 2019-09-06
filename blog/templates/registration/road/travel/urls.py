from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns=[
	
	url(r'^signup/', views.signup,name='signup'),
	url(r'^login/',auth_views.login,{'template_name': 'travel/login.html'}, name='login'),
	url(r'^logout/',auth_views.logout, {'next_page':'login'}, name='logout'),
	url(r'^$', views.first, name='first'),
	url(r'^index/', views.index, name='index'),
	url(r'^pack/', views.pack, name='pack'),
	url(r'^last/', views.last, name='last'),
	
	]