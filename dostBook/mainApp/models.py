import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profolieImg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self): # Gets called when object type expected for the output is str
        return str(self.user)


class VideoUpload(models.Model):
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')

    def __str__(self) -> str:
        return str(self.title)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4)
    user = models.TextField(max_length=100)
    image = models.ImageField(upload_to='post_images/')
    file = models.FileField(upload_to='posts_videos/')
    captions = models.TextField(max_length=200)
    no_of_likes = models.IntegerField(default=0)
    date_of_upload = models.TimeField(default=datetime.now) # type: ignore

    def __str__(self) -> str:
        return str(self.user)
    
    def likePost(self):
        self.no_of_likes += 1