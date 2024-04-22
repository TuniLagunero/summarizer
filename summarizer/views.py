import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
import google.generativeai as genai
from google.generativeai import GenerativeModel
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.views import logout_then_login
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout as auth_logout

os.environ["API_KEY"] = "AIzaSyBSsyGiTNZbXhnGngA2EEbOnA4n9Rqx7nc"
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        model = GenerativeModel('gemini-pro')
        chat = model.start_chat()
        response = chat.send_message(content)
        summary = response.text
        author = request.user
        post = Post.objects.create(title=title, content=content, summary=summary, author=author)
        return redirect('index')
    return render(request, 'create_post.html')

@login_required
def view_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    return render(request, 'view_post.html', {'post': post})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        post.delete()
        return redirect('index')
    else:
        return HttpResponse("You are not authorized to delete this post.")

def user_logout(request):
    auth_logout(request)
    return redirect('login')