import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    proflieImg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    following = models.ManyToManyField('self', related_name='followers', blank=True)
    followers = models.ManyToManyField('self', related_name='following', blank=True)

    def __str__(self): # Gets called when object type expected for the output is str
        return str(self.user)
    
    def is_following(self, profile):
        return self.following.filter(pk=profile.pk).exists()

    
    def follow(self, profile_to_follow) -> None:
        if not self.is_following(profile_to_follow):
            self.following.add(profile_to_follow)

    def unfollow(self, profile_to_unfollow):
        if self.is_following(profile_to_unfollow):
            self.following.remove(profile_to_unfollow)

    def following_count(self):
        return self.following.count()

class VideoUpload(models.Model):
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')

    def __str__(self) -> str:
        return str(self.title)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    captions = models.TextField(max_length=200)
    image = models.ImageField(upload_to='post_images/')
    no_of_likes = models.IntegerField(default=0)
    date_of_upload = models.TimeField(default=datetime.now) # type: ignore

    def __str__(self) -> str:
        return str(self.user)
    
    def likePost(self):
        self.no_of_likes += 1
        