from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


def LogInView(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, "You have successfully logged in")
            return redirect('retechecommerce:index')
        else:
            return render(request,'auth/login-register.html')
    return render(request, 'auth/login-register.html', {})

def LogOutView(request, *args, **kwargs):
    logout(request)
    messages.info(request,"You have successfully Logged Out")
    return redirect('retechecommerce:index')

def RegisterView(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "A user with the username exists")
                if User.objects.filter(email=email).exists():
                    messages.error(request, "The Email has already been used")
                    if password1 == password2:
                        messages.error(request, "Passwords do not match")
                        if len(password1)<6:
                            messages.error(request,"Password is too short")
                            return redirect('retechecommerce:login')
            else:
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password1)
                user.save()
                messages.success(request, "User has been created")
                return redirect('retechecommerce:index')
    context = {
        'form':form,
    }
    return render(request, 'auth/login-register.html', context)