from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
# Create your views here.


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password, email=email)
        user.save()
        messages.success(request, 'User registered successfully')
        return redirect('login')
    return render(request, 'register.html')


def login_user(request):
    return render(request, 'login.html')



def forgot_password_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():
            return render(request, 'forgot_request.html', {'error': 'Email does not exist'})
        # ✅ Pass the email in the URL as a query parameter
        return redirect(reverse('forgot_password') + f'?email={email}')
    return render(request, 'forgot_request.html')

def forgot_password(request):
    email = request.GET.get('email') 
    if not email:
        return redirect('forgot_password_request')

    
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            return render(request, 'forgot_password.html', {'error': 'Passwords do not match'})
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully')
            return redirect('login')
        except User.DoesNotExist:
            return render(request, 'forgot_password.html', {'error': 'User not found'})
        
    return render(request, 'forgot_password.html', {'email': email})
