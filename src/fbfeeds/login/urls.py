from django.conf.urls import patterns, url
from login import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^validate/$', views.validate, name='validate'),
	url(r'^logout/$', views.logout_view, name='logout'),
)