from django.shortcuts import render, redirect
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
                'forms_signup': forms.SignupForm(),
                'forms_login': forms.LoginForm(),
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
                'session_user': Profile.objects.get(user=request.user),
                'shoutout_form': forms.ShoutoutForm(),
                'is_more_than_10': False,
            })
        else:
            return redirect(reverse('feeds:index'))


class ProfileView(TemplateView):
    template_name = 'feeds/profile.html'

    def get(self, request, slug):
        profile = Profile.objects.get(user__username=slug)
        latest_posts = Post.objects.filter(
            author=profile).order_by('-post_date')[:10]
        return self.render_to_response({
            'profile': profile,
            'latest_posts': latest_posts,
            'shoutout_form': forms.ShoutoutForm(),
            'session_user': Profile.objects.get(user=request.user)
        })


class ProfileEditView(TemplateView):
    template_name = 'feeds/edit_profile.html'

    def get(self, request):
        session_user = Profile.objects.get(user=request.user)
        print session_user.__dict__
        return self.render_to_response({
            'session_user': session_user,
            'shoutout_form': forms.ShoutoutForm(),
            'profile_edit_forms': forms.ProfileEditForm(
                initial=session_user.to_dict())
        })


class DetailView(TemplateView):
    template_name = 'feeds/detail.html'

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        likers = Like.objects.filter(post=post).order_by('-like_date')
        comments = post.comment_set.order_by('-comment_date')
        session_user = Profile.objects.get(user=request.user)
        return self.render_to_response({
            'post': post,
            'likers_count': likers.count,
            'session_user': session_user,
            'shoutout_form': forms.ShoutoutForm(),
            'comment_form': forms.CommentForm(initial={
                'author': session_user,
                'post': post,
            }),
            'has_liked': bool(likers.filter(liker=session_user)),
            'likes': likers[:10],
            'comments': comments,
            'comment_forms': forms.CommentForm(),
        })


class CreateUserRedirectView(RedirectView):

    def get(self, request):
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect(reverse('feeds:edit_profile'))
        else:
            return redirect(reverse('feeds:index'))


class PostRedirectView(RedirectView):

    def get(self, request):
        form = forms.ShoutoutForm(request.POST)
        post = form.save()
        return redirect(reverse('feeds:detail', args=(post.id,)))


class EditPostRedirectView(RedirectView):

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.content = request.POST['content']
        post.save()
        return redirect(reverse('feeds:detail', args=(post_id,)))


class DeletePostRedirectView(RedirectView):

    def get(get, request, post_id):
        Post.objects.get(pk=post_id).delete()
        return redirect(reverse('feeds:feeds'))


class EditProfileRedirectView(RedirectView):

    def get(self, request):
        form = forms.ProfileEditForm(request.POST, request.FILES)
        if not form.is_valid():
            form.save()
        return redirect(reverse('feeds:profile'), args=(request.user,))


class LikeRedirectView(RedirectView):

    def get(self, request, post_id):
        like = Like.objects.create(
            post=Post.objects.get(pk=post_id),
            liker=Profile.objects.get(user=request.user)
        )
        return redirect(reverse('feeds:detail', args=(post_id,)))


class UnlikeRedirectView(RedirectView):

    def get(self, request, post_id):
        Like.objects.filter(
            post=Post.objects.get(pk=post_id),
            liker=Profile.objects.get(user=request.user)
        ).delete()
        return redirect(reverse('feeds:detail', args=(post_id,)))


class CommentRedirectView(RedirectView):

    def get(self, request):
        form = forms.CommentForm(request.POST)
        comment = form.save()
        return redirect(reverse('feeds:detail', args=(request.POST['post'],)))
