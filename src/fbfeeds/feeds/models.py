from django.db import models
from django.contrib.auth.models import User
from fbfeeds import settings


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    gender = models.CharField(
        blank=True, max_length=1, choices=(('F', 'Female'), ('M', 'Male'),))
    prof_pic = models.ImageField(null=True, upload_to='feeds/prof_pics/')
    birthdate = models.DateField(null=True)
    bio = models.TextField(blank=True)

    def __unicode__(self):
        return self.user.username

    def to_dict(self):
        return {
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'password': self.user.password,
            'email': self.user.email,
            'birthdate': self.birthdate,
            'prof_pic': self.prof_pic,
            'gender': self.gender,
            'bio': self.bio,
        }


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(Profile)
    likes = models.IntegerField(default=0)
    post_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content

    def to_dict(self):
        return {
            'content': self.content,
            'author': author,
        }


class Like(models.Model):
    post = models.ForeignKey(Post)
    liker = models.ForeignKey(Profile)
    like_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return repr(self.id)


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post)
    author = models.ForeignKey(Profile)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content
