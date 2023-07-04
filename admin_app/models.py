from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()

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