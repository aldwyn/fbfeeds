from django.contrib.auth import forms as user_forms
from django.contrib.auth.models import User

from feeds.models import Post, Comment, Profile
from django import forms


class LoginForm(user_forms.AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username...',
        'required': True,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password...',
        'required': True,
    }))

    class Meta:
        model = User
        fields = ['username', 'password']


class SignupForm(user_forms.UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username...',
        'required': True,
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password...',
        'required': True,
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password...',
        'required': True,
    }))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'placeholder': 'Enter email...',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'placeholder': 'Enter first name...',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'placeholder': 'Enter last name...',
                }
            )
        }


class UserEditForm(user_forms.UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'disabled': True,
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'placeholder': 'Enter email...',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'placeholder': 'Enter first name...',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'placeholder': 'Enter last name...',
                }
            )
        }


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['birthdate', 'bio', 'prof_pic', 'gender']
        widgets = {
            'user_id': forms.HiddenInput(),
            'birthdate': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'yyyy-mm-dd',
                }
            ),
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Let your fans know about yourself...',
                    'rows': 3,
                }
            ),
            'prof_pic': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'gender': forms.RadioSelect(),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content', 'post', 'author']
        widgets = {
            'post': forms.HiddenInput(),
            'author': forms.HiddenInput(),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 600px',
                    'placeholder': 'What do you think...?',
                    'required': True,
                    'rows': 2,
                }
            )
        }


class ShoutoutForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['content', 'author']
        widgets = {
            'author': forms.HiddenInput(),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'placeholder': 'Blurt out your thoughts...',
                    'required': True,
                    'rows': 7,
                }
            ),
        }
