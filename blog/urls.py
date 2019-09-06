from django.conf.urls import  url
from .import views
from django.contrib.auth import views as auth_views
urlpatterns=[
	#url(r'^$',views.index,name="index"),
	url(r'^$',views.post_list,name="post_list"),
	url(r'^post_list/$',views.post_list,name="post_list"),
	url(r'^blog/(?P<id>\d+)/post_edit/$',views.post_edit, name="post_edit"),
	url(r'^blog/(?P<id>\d+)/post_delete/$',views.post_delete, name="post_delete"),
	url(r'^blog/(?P<id>\d+)/(?P<slug>[\w-]+)/$',views.post_detail, name="post_detail"),
	url(r'^post_create/$',views.post_create,name="post_create"),
	url(r'^edit_profile/$',views.edit_profile,name="edit_profile"),


	#url(r'^register/',views.user_register,name="user_register"),
	#url(r'^login/',auth_views.login,{'template_name': 'blog/login.html'}, name='login'),
	#url(r'^logout/',auth_views.logout, {'next_page':'login'}, name='logout'),
]
