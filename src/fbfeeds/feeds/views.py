from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import generic
from feeds.models import Post, Like, Comment


class LoginView(generic.TemplateView):
	template_name = 'feeds/login.html'


class IndexView(generic.ListView):
	template_name = 'feeds/index.html'
	context_object_name = 'latest_posts'

	def get_queryset(self):
		"""Return the latest 10 posts."""
		return Post.objects.all().order_by('-post_date')[:10]


class DetailView(generic.DetailView):
	template_name = 'feeds/detail.html'
	context_object_name = 'post'
	model = Post


class ProfileView(generic.DetailView):
	template_name = 'feeds/profile.html'
	context_object_name = 'profile'
	model = User


def likers(request, post_id):
	likers = User.objects.filter()
	return


def validate(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user:
		if user.is_active:
			login(request, user)
			return redirect(reverse('feeds:index'))
		else:
			return render(request, 'feeds/login.html', {
				'error_message': "Your account has been disabled. It is very much advised that you sign up."
			})
	else:
		return render(request, 'feeds/login.html', {
			'error_message': "Incorrect username or password."
		})


def post(request):
	post = Post.objects.create(
		content = request.POST['content'],
		author = request.user
	)
	return redirect(reverse('feeds:detail', args=(post.id,)))


def like(request, post_id):
	post = Post.objects.get(pk=post_id)
	post.likes += 1
	post.save()
	like = Like.objects.create(post=post, liker=request.user)
	return redirect(reverse('feeds:detail', args=(post_id,)))


def logout_view(request):
	logout(request)
	return redirect(reverse('feeds:login'))