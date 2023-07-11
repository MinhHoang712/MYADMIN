from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.core.paginator import Paginator

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_app:home')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không chính xác.')
    
    return render(request, 'admin_app/login.html')

@login_required(login_url='admin_app:login')
def home_view(request):
    # Nếu người dùng đã đăng nhập, chuyển hướng đến trang home
    if request.user.is_authenticated:
        return render(request, 'admin_app/home.html')

    # Nếu người dùng chưa đăng nhập, chuyển hướng đến trang đăng nhập
    else:
        return redirect('admin_app:login')
def logout_view(request):
    logout(request)
    return redirect('admin_app:login')

@login_required(login_url='admin_app:login')
def chatgpt(request):
    conversations = Conversation.objects.all()
    paginator = Paginator(conversations, 5)  # Số cuộc hội thoại hiển thị trên mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        # 'conversations':conversations,
        'conversations': page_obj
    }
    return render(request, 'admin_app/chatgpt.html', context)



@login_required(login_url='admin_app:login')
def chatgpt_conversation(request, conversation_id):
    if conversation_id == 0:
        conversation = Conversation.objects.create(title = "New Conversation", user_id = request.user.id)
        conversation_id = conversation.id
        conversation.save()
        return redirect('admin_app:chatgpt_conversation', conversation_id=conversation_id)

    else:
        conversation = get_object_or_404(Conversation, id=conversation_id)
    
    messages = conversation.message_set.all()
    
    print(conversation_id)
    # print(messages[0].content)
    if messages:
        conversation.title = messages[0].content
        conversation.save()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.is_user = True
            message.save()
            return redirect('admin_app:chatgpt_conversation', conversation_id=conversation_id)
    else:
        
        form = MessageForm()
    # return redirect('admin_app:chatgpt_conversation', conversation_id=conversation_id)
    context = {
        'conversation': conversation,
        'messages': messages,
        'form': form
    }
    return render(request, 'admin_app/conversation.html', context)

@login_required(login_url='admin_app:login')
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_app:profile')
    else:
        form = CustomUserForm(instance=user)

    context = {
        'user': user,
        'form': form
    }
    return render(request, 'admin_app/profile.html', context)
