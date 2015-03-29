from django.contrib.auth import forms as user_forms
from django.contrib.auth.models import User
from feeds.models import Post, Comment, Profile
from django import forms


class LoginForm(user_forms.AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username...',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password...',
    }))

    class Meta:
        model = User
        fields = ['username', 'password']


class SignupForm(user_forms.UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username...',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password...',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password...',
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name',
                  'last_name']
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email...',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter first name...',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter last name...',
                }
            )
        }


class ProfileEditForm(user_forms.UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username...',
        'disabled': True,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Cannot be seen because it is hashed...',
        'disabled': True,
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter first name...',
        'required': True,
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter last name...',
        'required': True,
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email address...',
        'required': True,
    }))

    class Meta:
        model = Profile
        fields = ['username', 'password', 'first_name', 'last_name',
                  'email', 'birthdate', 'bio', 'prof_pic', 'gender']
        widgets = {
            'birthdate': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'type': 'date',
                }
            ),
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Let us know a description, or two, about yourself...',
                    'required': True,
                    'rows': 3,
                }
            ),
            'prof_pic': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'gender': forms.RadioSelect(
                attrs={
                    'required': True,
                }
            ),

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
                    'rows': 7,
                }
            ),
        }