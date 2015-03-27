from django.conf.urls import patterns, url
from feeds import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^feeds/$', views.FeedsView.as_view(), name='feeds'),
    url(r'^(?P<post_id>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<post_id>\d+)/like/$', views.like, name='like'),
    url(r'^(?P<post_id>\d+)/comment/$', views.comment, name='comment'),
    url(r'^(?P<post_id>\d+)/likers/$', views.likers_view, name='likers'),
    url(r'^(?P<post_id>\d+)/edit_post/$',
        views.edit_post, name='edit_post'),
    url(r'^profile/(?P<slug>\w+)/$',
        views.ProfileView.as_view(), name='profile'),
    url(r'^profile/edit/$', views.edit_profile_view,
        name='edit_profile_view'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^post/$', views.post, name='post'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^create_user/$', views.create_user, name='create_user'),
    url(r'^validate/$', views.validate, name='validate'),
)
