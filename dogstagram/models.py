from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	pfp = models.URLField(blank='true', null='true')
	following = models.ManyToManyField("User", related_name="followers")

	def serialize(self):
		return {
			'username' : self.username,
			'pfp' : self.pfp,
			'following' : [user.username for user in self.following.all()],
			'followers' : [user.username for user in self.followers.all()],
		}
	pass

class Post(models.Model):
	author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
	body = models.TextField(blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	liked_by = models.ManyToManyField("User", related_name="likes")

	def serialize(self):
		return {
			"id": self.id,
			"author": self.author.username,
			"timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
			"body": self.body,
			"liked_by": [user.username for user in self.liked_by.all()],
		}

class PostPictures(models.Model):
	url = models.URLField(blank='true')
	onPost = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='pictures')

	def serialize(self):
    			return {
    				'id' : self.id,
    				"url" : self.url,
    				"postId" : self.onPost.id,
    			}

class PostComments(models.Model):
	body = models.TextField(blank='true')
	author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')
	post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
	timestamp = models.DateTimeField(auto_now_add=True)
	liked_by = models.ManyToManyField("User", related_name='likesComments')

	def serialize(self):
    			return {
    				"id": self.id,
    				"body": self.body,
    				"author": self.author.username,
    				"postId" : self.onPost.id,
    				"timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
    				"liked_by": [user.username for user in self.liked_by.all()],
    			}

class DMs(models.Model):
	sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sentDMs')
	receiver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='receivedDMs')
	body = models.TextField(blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def serialize(self):
    			return {
    				"sender" : self.sender.username,
    				"receiver" : self.receiver.username,
    				"body" : self.body,
    				"timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
    			}