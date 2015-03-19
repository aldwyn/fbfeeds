from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	content = models.TextField()
	author = models.OneToOneField(User)
	likes = models.IntegerField(default=0)
	post_date = models.DateTimeField('date posted')

	def __unicode__(self):
		return self.id


class Like(models.Model):
	post = models.OneToOneField(Post)
	liker = models.ForeignKey(User)
	like_date = models.DateTimeField('date liked')

	def __unicode__(self):
		return self.id