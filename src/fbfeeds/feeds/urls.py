from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from feeds.forms import LoginForm, SignupForm
from feeds import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^feeds/$', views.FeedsView.as_view(), name='feeds'),
    url(r'^login/$', 'django.contrib.auth.views.login', {
        'template_name': 'feeds/index.html',
        'extra_context': {
            'signup_form': SignupForm(),
            'login_form': LoginForm(),
        },
    }, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/shoutout'}, name='logout'),
    url(r'^(?P<post_id>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<post_id>\d+)/like/$',
        views.LikeRedirectView.as_view(), name='like'),
    url(r'^(?P<post_id>\d+)/unlike/$',
        views.UnlikeRedirectView.as_view(), name='unlike'),
    url(r'^comment/$', views.CommentRedirectView.as_view(), name='comment'),
    url(r'^(?P<post_id>\d+)/edit_post/$',
        views.EditPostRedirectView.as_view(), name='edit_post'),
    url(r'^(?P<post_id>\d+)/delete_post/$',
        views.DeletePostRedirectView.as_view(), name='delete_post'),
    url(r'^profile/(?P<slug>\w+)/$',
        views.ProfileView.as_view(), name='profile'),
    url(r'^profile_edit/$', views.ProfileEditView.as_view(),
        name='edit_profile_view'),
    url(r'^edit_profile/$', views.EditProfileRedirectView.as_view(),
        name='edit_profile'),
    url(r'^post/$', views.PostRedirectView.as_view(), name='post'),
    url(r'^create_user/$', views.CreateUserRedirectView.as_view(),
        name='create_user'),
)
