from django.contrib import admin
from .models import Conversation, Message, Audio

admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Audio)
# Register your models here.
