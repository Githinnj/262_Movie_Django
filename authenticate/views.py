from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'registration/register.html', {'error_message': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {'error_message': 'Username already exists'})

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'registration/register.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to your desired home page
        else:
            # Return an 'invalid login' error message.
            return render(request, 'registration/login.html', {'error_message': 'Invalid login'})
    return render(request, 'registration/login.html')
