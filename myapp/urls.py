from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('make-audio/', views.make_audio, name='make-audio')
]