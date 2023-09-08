from django.contrib import admin

from .models import User, Post, PostPictures, PostComments
# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(PostPictures)
admin.site.register(PostComments)
