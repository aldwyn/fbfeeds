from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from feeds.models import Post, Like, Comment


def index(request):
	if request.user.is_authenticated():
		latest_posts = Post.objects.all().order_by('-post_date')[:10]
		session_user = request.user
		return render(request, 'feeds/feeds.html', {'latest_posts': latest_posts, 'session_user': session_user})
	else:
		return render(request, 'feeds/index.html')


def profile_view(request, user_id):
	profile = User.objects.get(pk=user_id)
	return render(request, 'feeds/profile.html', {
		'profile': profile,
		'is_sessioned': (profile.pk == request.user.id),
	})


def logout_view(request):
	logout(request)
	return redirect(reverse('feeds:index'))


def signup_view(request):
	return render(request, 'feeds/signup.html')


def create_user(request):
	username = request.POST['username']
	check_username = User.objects.get(username=username)
	if not check_username:
		password = request.POST['password']
		conf_pass = request.POST['conf_pass']
		if password == conf_pass:
			new_user = User.objects.create_user(
				username = username,
				first_name = request.POST['firstname'],
				last_name = request.POST['lastname'],
				email = request.POST['email'],
				password = password
			)
			session_user = authenticate(username=new_user.username, password=new_user.password)
			login(request, session_user)
			return redirect(reverse('feeds:index'))
		else:
			return redirect(reverse('feeds:signup'))
	else:
		return redirect(reverse('feeds:signup'))
	

def detail(request, post_id):
	post = Post.objects.get(pk=post_id)
	likers_count = Like.objects.filter(post=post).count
	comments = post.comment_set.order_by('-comment_date')
	return render(request, 'feeds/detail.html', {
		'post': post,
		'likers_count': likers_count,
		'is_author': (post.author.pk == request.user.pk),
		'comments': comments,
	})


def likers_view(request, post_id):
	post = Post.objects.get(pk=post_id)
	likers = Like.objects.filter(post=post).order_by('-like_date')
	return render(request, 'feeds/likers.html', {'post': post, 'likers': likers})


def validate(request):
	username = request.POST['username']
	password = request.POST['password']
	session_user = authenticate(username=username, password=password)
	login(request, session_user)
	return redirect(reverse('feeds:index'))


def post(request):
	post = Post.objects.create(
		content = request.POST['content'],
		author = request.user
	)
	return redirect(reverse('feeds:detail', args=(post.id,)))


def edit_post_view(request, post_id):
	post = Post.objects.get(pk=post_id)
	return render(request, 'feeds/edit_post.html', {'post': post})


def edit_post(request ,post_id):
	post = Post.objects.get(pk=post_id)
	post.content = request.POST['content']
	post.save()
	return redirect(reverse('feeds:detail', args=(post_id,)))


def edit_profile_view(request):
	return render(request, 'feeds/edit_profile.html', {'session_user': request.user})


def edit_profile(request):
	user = request.user
	user.first_name = request.POST['firstname']
	user.last_name = request.POST['lastname']
	user.email = request.POST['email']
	user.save()
	return redirect(reverse('feeds:profile', args=(user.id,)))


def like(request, post_id):
	like = Like.objects.create(post=Post.objects.get(pk=post_id), liker=request.user)
	return redirect(reverse('feeds:detail', args=(post_id,)))


def comment(request, post_id):
	comment = Comment.objects.create(
		content = request.POST['content'],
		post = Post.objects.get(pk=post_id),
		author = request.user
	)
	return redirect(reverse('feeds:detail', args=(post_id,)))


def edit(request, post_id):
	comment = Comment.objects.get(pk=post_id)
	comment.content = request.POST['content']