from django import forms
from .models import Conversation, Message, CustomUser
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class CustomUserForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True), label='Password')
    profile_picture = forms.ImageField(required=False)
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username','first_name', 'last_name', 'email', 'profile_picture')

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['title']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
