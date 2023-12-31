from django.urls import path
from . import views

app_name = 'admin_app'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('chatgpt/', views.chatgpt, name='chatgpt'),
    path('chatgpt/<int:conversation_id>/', views.chatgpt_conversation, name='chatgpt_conversation'),
    path('profile/', views.profile_view, name='profile'),
    # ...
   
    # Các đường dẫn khác sẽ được thêm vào sau này
]
