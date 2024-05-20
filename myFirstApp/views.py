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
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    elif request.method == 'GET':
        return render(request, 'login.html')

def logoutview(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        full_name = request.POST['full_name']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already in use')
            return render(request, 'register.html')

        # Periksa apakah pengguna sudah memiliki profil
        user = User.objects.create_user(username=username, email=email, password=password)
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user, phone_number=phone_number, full_name=full_name)
        else:
            messages.error(request, 'Profile already exists for this user')

        login(request, user)
        messages.success(request, 'Registration successful. You are now logged in.')
        return redirect('login')

    elif request.method == 'GET':
        return render(request, 'register.html')
    
def product_detail(request):
    return render(request, 'product_detail.html')