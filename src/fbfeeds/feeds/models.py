from django.db import models
from django.contrib.auth.models import User
from fbfeeds import settings


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    gender = models.CharField(
        max_length=7, choices=(('F', 'Female'), ('M', 'Male'),))
    prof_pic = models.ImageField(upload_to=settings.PROFILE_IMAGE_DIRS)
    birthdate = models.DateField()
    bio = models.TextField()

    def __unicode__(self):
        return self.user.username


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(Profile)
    likes = models.IntegerField(default=0)
    post_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content


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
