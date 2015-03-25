from django.db import models
from django.contrib.auth.models import User
from fbfeeds import settings



GENDER = (
	('F', 'Female'),
	('M', 'Male'),
)


class Profile(models.Model):
	user = models.OneToOneField(User, related_name='profile')
	gender = models.CharField(max_length=7, choices=GENDER)
	prof_pic = models.ImageField(upload_to=settings.PROFILE_IMAGE)
	birthdate = models.DateField()
	bio = models.TextField()

	def __unicode__(self):
		return self.user


class Post(models.Model):
	content = models.TextField()
	author = models.ForeignKey(User)
	likes = models.IntegerField(default=0)
	post_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.content


class Like(models.Model):
	post = models.ForeignKey(Post)
	liker = models.ForeignKey(User)
	like_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return repr(self.id)


class Comment(models.Model):
	content = models.TextField()
	post = models.ForeignKey(Post)
	author = models.ForeignKey(User)
	comment_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.content