from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, RedirectView

from feeds.models import Post, Like, Comment, Profile
from feeds import forms


class IndexView(TemplateView):
    template_name = 'feeds/index.html'

    def get(self, request):
        if not request.user.is_authenticated():
            return self.render_to_response({
                'signup_form': forms.SignupForm(),
                'login_form': forms.LoginForm(),
            })
        else:
            return redirect(reverse('feeds:feeds'))


class FeedsView(TemplateView):
    template_name = 'feeds/feeds.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FeedsView, self).get_context_data(*args, **kwargs)
        session_user = get_object_or_404(Profile, user=self.request.user)
        context.update({
            'latest_posts': Post.objects.all().order_by('-post_date')[:10],
            'session_user': session_user,
            'shoutout_form': forms.ShoutoutForm(initial={
                'author': session_user,
            }),
            'is_more_than_10': False,
        })
        return context


class ProfileView(TemplateView):
    template_name = 'feeds/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        profile = get_object_or_404(Profile, user__username=kwargs['slug'])
        latest_posts = Post.objects.filter(
            author=profile).order_by('-post_date')[:10]
        session_user = get_object_or_404(Profile, user=request.user)
        context.update({
            'profile': profile,
            'latest_posts': latest_posts,
            'shoutout_form': forms.ShoutoutForm(initial={
                'author': session_user,
            }),
            'session_user': session_user
        })
        return context


class ProfileEditView(TemplateView):
    template_name = 'feeds/edit_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileEditView, self).get_context_data(
            *args, **kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context.update({
            'session_user': profile,
            'shoutout_form': forms.ShoutoutForm(initial={
                'author': profile,
            }),
            'user_edit_form': forms.UserEditForm(instance=profile.user),
            'profile_edit_form': forms.ProfileEditForm(
                instance=profile, initial={
                    'user_id': profile.user.pk}),
        })
        return context


class DetailView(TemplateView):
    template_name = 'feeds/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        likers = Like.objects.filter(post=post).order_by('-like_date')
        comments = post.comment_set.order_by('-comment_date')
        session_user = get_object_or_404(Profile, user=self.request.user)
        context.update({
            'post': post,
            'likers_count': likers.count,
            'session_user': session_user,
            'shoutout_form': forms.ShoutoutForm(initial={
                'author': session_user,
            }),
            'comment_form': forms.CommentForm(initial={
                'author': session_user,
                'post': post,
            }),
            'has_liked': bool(likers.filter(liker=session_user)),
            'likes': likers[:10],
            'comments': comments,
        })
        return context


class CreateUserRedirectView(RedirectView):

    def post(self, request):
        signup_form = forms.SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            print user
            session_user = authenticate(
                username=request.POST['username'],
                password=request.POST['password1']
            )
            if session_user:
                if session_user.is_active():
                    login(request, session_user)
                    return redirect(reverse('feeds:edit_profile_view'))
                else:
                    return redirect(reverse('feeds:index'))
            else:
                return redirect(reverse('feeds:index'))
        else:
            return redirect(reverse('feeds:index'))


class PostRedirectView(RedirectView):

    def get(self, request):
        form = forms.ShoutoutForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            post = form.save()
            return redirect(reverse('feeds:detail', args=(post.id,)))
        else:
            return redirect(reverse('feeds:feeds'))


class EditPostRedirectView(RedirectView):

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        post.content = request.POST['content']
        post.save()
        return redirect(reverse('feeds:detail', args=(post_id,)))


class DeletePostRedirectView(RedirectView):

    def get(get, request, post_id):
        Post.objects.get(pk=post_id).delete()
        return redirect(reverse('feeds:feeds'))


class EditProfileRedirectView(RedirectView):

    def get(self, request):
        user_form = forms.UserEditForm(
            request.POST, instance=request.user,
            initial={
                'password': request.user.password if not request.user.is_anonymous() else None
            })
        if user_form.is_valid():
            user_form.save()
        profile_form = forms.ProfileEditForm(
            request.POST, request.FILES,
            instance=get_object_or_404(Profile, user=request.user))
        if profile_form.is_valid():
            profile_form.save()
        return redirect(reverse(
            'feeds:profile', args=(request.user.username,)))


class LikeRedirectView(RedirectView):

    def get(self, request, post_id):
        like = Like.objects.create(
            post=get_object_or_404(Post, pk=post_id),
            liker=get_object_or_404(Profile, user=request.user)
        )
        return redirect(reverse('feeds:detail', args=(post_id,)))


class UnlikeRedirectView(RedirectView):

    def get(self, request, post_id):
        Like.objects.filter(
            post=get_or_create(Post, pk=post_id),
            liker=get_object_or_404(Profile, user=request.user)
        ).delete()
        return redirect(reverse('feeds:detail', args=(post_id,)))


class CommentRedirectView(RedirectView):

    def get(self, request):
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('feeds:detail', args=(request.POST['post'],)))
