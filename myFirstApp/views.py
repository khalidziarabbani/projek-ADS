from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile

def index(request):
    return render(request, 'index.html')

def loginview(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html')
    elif request.method == 'GET':
        return render(request, 'login.html')

def logoutview(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Password tidak sama')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, 'Registrasi berhasil. Anda berhasil login.')
        return redirect('login')

    elif request.method == 'GET':
        return render(request, 'register.html')
