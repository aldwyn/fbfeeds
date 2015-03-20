from django.conf.urls import patterns, url
from feeds import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	url(r'^(?P<post_id>\d+)/like/$', views.like, name='like'),
	url(r'^profile/(?P<pk>\d+)/$', views.ProfileView.as_view(), name='profile'),
	url(r'^post/$', views.post, name='post'),
	url(r'^login/$', views.LoginView.as_view(), name='login'),
	url(r'^validate/$', views.validate, name='validate'),
	url(r'^logout/$', views.logout_view, name='logout'),
)