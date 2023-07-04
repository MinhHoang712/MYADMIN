from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login

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
def chatgpt_view(request, conversation_id=None):
    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id)
    else:
        conversation = Conversation.objects.create(user=request.user, title='New Conversation')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.is_user = True
            message.save()
            # print(message)
            # print(message.content)
            conversation.question = message.content
            answer = 'Hello'
            conversation.answer = answer
            reply = Message(content=answer, conversation=conversation)
            reply.save()
            # form = MessageForm()  # Clear the form after saving the message
            
    else:
        form = MessageForm()
    
    # print(conversation.message_set.all())
    # for message in conversation.message_set.all():
    #     print(message.content)
    context = {
        'conversation': conversation,
        'form': form,
    }
    return render(request, 'admin_app/chatgpt.html', context)