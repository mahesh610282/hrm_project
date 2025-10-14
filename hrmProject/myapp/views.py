from django.shortcuts import render

# Create your views here.

def reigster(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            print(first_name, last_name, username, email, password)
    return render(request, 'register.html')
