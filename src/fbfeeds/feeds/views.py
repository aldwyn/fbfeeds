from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, RedirectView

from feeds.models import Post, Like, Comment, Profile
from feeds import forms


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispath(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


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


class FeedsView(LoginRequiredMixin, TemplateView):
    template_name = 'feeds/feeds.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FeedsView, self).get_context_data(*args, **kwargs)
        context.update({
            'latest_posts': Post.objects.all().order_by('-post_date')[:10],
            'session_user': self.request.user.profile,
            'shoutout_form': forms.ShoutoutForm(initial={
                'author': self.request.user.profile,
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
        context.update({
            'profile': profile,
            'latest_posts': latest_posts,
            'shoutout_form': forms.ShoutoutForm(initial={
                'author': self.request.user.profile,
            }),
            'session_user': self.request.user.profile
        })
        return context


class ProfileEditView(TemplateView):
    template_name = 'feeds/edit_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileEditView, self).get_context_data(
            *args, **kwargs)
        context.update({
            'session_user': self.request.user.profile,
            'shoutout_form': forms.ShoutoutForm(initial={
                'author': self.request.user.profile,
            }),
            'user_edit_form': forms.UserEditForm(instance=self.request.user),
            'profile_edit_form': forms.ProfileEditForm(
                instance=self.request.user.profile, initial={
                    'user_id': self.request.user.profile.pk}),
        })
        return context


class DetailView(TemplateView):
    template_name = 'feeds/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        likers = Like.objects.filter(post=post).order_by('-like_date')
        comments = post.comment_set.order_by('-comment_date')
        context.update({
            'post': post,
            'session_user': self.request.user.profile,
            'shoutout_form': forms.ShoutoutForm(initial={
                'author': self.request.user.profile,
            }),
            'comment_form': forms.CommentForm(initial={
                'author': self.request.user.profile,
                'post': post,
            }),
            'has_liked': bool(likers.filter(liker=self.request.user.profile)),
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
                    messages.error(request, 'It was a disabled account.')
                    return redirect(reverse('feeds:index'))
            else:
                messages.error(request, 'Invalid login.')
                return redirect(reverse('feeds:index'))
        else:
            messages.error(request, 'Please input valid data accordingly.')
            return redirect(reverse('feeds:index'))


class PostRedirectView(RedirectView):

    def get(self, request):
        form = forms.ShoutoutForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            post = form.save()
            messages.success(request, 'You posted a shoutout successfully.')
            return redirect(reverse('feeds:detail', args=(post.id,)))
        else:
            messages.error(request, 'It was an invalid post.')
            return redirect(reverse('feeds:feeds'))


class EditPostRedirectView(RedirectView):

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        post.content = request.POST['content']
        post.save()
        messages.success(request, 'You modified this post.')
        return redirect(reverse('feeds:detail', args=(post_id,)))


class DeletePostRedirectView(RedirectView):

    def get(get, request, post_id):
        Post.objects.get(pk=post_id).delete()
        messages.success(request, 'You deleted a shoutout.')
        return redirect(reverse('feeds:feeds'))


class EditProfileRedirectView(RedirectView):

    def get(self, request):
        password = None
        if not request.user.is_anonymous():
            password = request.user.password
        user_form = forms.UserEditForm(
            request.POST, instance=request.user,
            initial={'password': password})
        profile_form = forms.ProfileEditForm(request.POST, request.FILES,
                                             instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
        else:
            messages.error(request, 'Invalid login.')
        return redirect(reverse(
            'feeds:profile', args=(request.user.username,)))


class LikeRedirectView(RedirectView):

    def get(self, request, post_id):
        like = Like.objects.create(
            post=get_object_or_404(Post, pk=post_id),
            liker=request.user.profile,
        )
        return redirect(reverse('feeds:detail', args=(post_id,)))


class UnlikeRedirectView(RedirectView):

    def get(self, request, post_id):
        Like.objects.filter(
            post=get_or_create(Post, pk=post_id),
            liker=request.user.profile,
        ).delete()
        return redirect(reverse('feeds:detail', args=(post_id,)))


class CommentRedirectView(RedirectView):

    def get(self, request):
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('feeds:detail', args=(request.POST['post'],)))
