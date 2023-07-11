from django.db import models
from django.contrib.auth.models import AbstractUser
import os

class CustomUser(AbstractUser):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile/', blank=True, null=True)

    def __str__(self):
        return self.username

# Create your models here.
class Conversation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title
    
    
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_user = models.BooleanField(default=False)

    def __str__(self):
        return f'Message {self.id}'

    class Meta:
        ordering = ['timestamp']
    
class Audio(models.Model):
    audio = models.FileField(upload_to='admin_app/static/audio/', blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    audio_file_name = models.CharField(max_length=255, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_filename = self.audio
        audio_id = self.id
        if base_filename:
            file_upload_name = base_filename.replace('admin_app/static/audio/', '')
            file_name_without_ext = os.path.splitext(file_upload_name)[0]
            extension = os.path.splitext(file_upload_name)[1]
            if extension == 'mp3':
                self.audio_file_name = f'{file_name_without_ext}_{audio_id}.mp3'

    def __str__(self):
        return f'{self.id}'