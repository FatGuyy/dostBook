from django import forms
from .models import VideoUpload

class Videoform(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ['title', 'video_file']
