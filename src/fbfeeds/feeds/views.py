from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView
from feeds.models import Post, Like, Comment, Profile
from feeds import forms


class IndexView(TemplateView):
    template_name = 'feeds/index.html'

    def get(self, request):
        if not request.user.is_authenticated():
            return self.render_to_response({
                'forms_signup': forms.SignupForm(),
                'forms_login': forms.LoginForm()
            })
        else:
            return redirect(reverse('feeds:feeds'))


class FeedsView(TemplateView):
    template_name = 'feeds/feeds.html'

    def get(self, request):
        if request.user.is_authenticated():
            print Profile.objects.get(user=request.user)
            return self.render_to_response({
                'latest_posts': Post.objects.all().order_by('-post_date')[:10],
                'session_user': Profile.objects.get(user=request.user).user,
            })
        else:
            return redirect(reverse('feeds:index'))


class ProfileView(TemplateView):
    template_name = 'feeds/profile.html'

    def get(self, request, slug):
        profile = Profile.objects.get(user__username=slug)
        latest_posts = Post.objects.filter(
            author__user=profile).order_by('-post_date')[:10]
        return self.render_to_response({
            'profile': profile,
            'latest_posts': latest_posts,
            'session_user': request.user
        })


class DetailView(TemplateView):
    template_name = 'feeds/detail.html'

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        likers_count = Like.objects.filter(post=post).count
        comments = post.comment_set.order_by('-comment_date')
        return self.render_to_response({
            'post': post,
            'likers_count': likers_count,
            'session_user': request.user,
            'comments': comments,
        })


def logout_view(request):
    logout(request)
    return redirect(reverse('feeds:index'))


def create_user(request):
    username = request.POST['username']
    check_username = User.objects.filter(username=username)
    if not check_username:
        password = request.POST['password']
        conf_pass = request.POST['conf_pass']
        if password == conf_pass:
            new_user = User.objects.create_user(
                username=username,
                first_name=request.POST['firstname'],
                last_name=request.POST['lastname'],
                email=request.POST['email'],
                password=password
            )
            session_user = authenticate(
                username=new_user.username, password=new_user.password)
            login(request, session_user)
            return redirect(reverse('feeds:index'))
        else:
            return redirect(reverse('feeds:signup'))
    else:
        return redirect(reverse('feeds:signup'))


def likers_view(request, post_id):
    post = Post.objects.get(pk=post_id)
    likers = Like.objects.filter(post=post).order_by('-like_date')
    return render(request, 'feeds/likers.html', {
        'post': post,
        'likers': likers,
        'session_user': request.user
    })


def validate(request):
    username = request.POST['username']
    password = request.POST['password']
    session_user = authenticate(username=username, password=password)
    login(request, session_user)
    return redirect(reverse('feeds:feeds'))


def post(request):
    post = Post.objects.create(
        content=request.POST['content'],
        author=Profile.objects.get(user=request.user)
    )
    return redirect(reverse('feeds:detail', args=(post.id,)))


def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.content = request.POST['content']
    post.save()
    return redirect(reverse('feeds:detail', args=(post_id,)))


def edit_profile_view(request):
    return render(request, 'feeds/edit_profile.html', {
        'session_user': request.user
    })


def edit_profile(request):
    user = request.user
    user.first_name = request.POST['firstname']
    user.last_name = request.POST['lastname']
    user.email = request.POST['email']
    user.save()
    return redirect(reverse('feeds:profile', args=(user.id,)))


def like(request, post_id):
    like = Like.objects.create(
        post=Post.objects.get(pk=post_id), liker=request.user)
    return redirect(reverse('feeds:detail', args=(post_id,)))


def comment(request, post_id):
    comment = Comment.objects.create(
        content=request.POST['content'],
        post=Post.objects.get(pk=post_id),
        author=request.user
    )
    return redirect(reverse('feeds:detail', args=(post_id,)))
