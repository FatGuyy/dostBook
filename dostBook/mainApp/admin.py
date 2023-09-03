from django.contrib import admin
from .models import Profile, VideoUpload, Post

# Register your models here.
admin.site.register(Profile)
admin.site.register(VideoUpload)
admin.site.register(Post)