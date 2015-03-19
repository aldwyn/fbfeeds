from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	content = models.TextField()
	author = models.ForeignKey(User)
	likes = models.IntegerField(default=0)
	post_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.id


class Like(models.Model):
	post = models.ForeignKey(Post)
	liker = models.ForeignKey(User)
	like_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.id