from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, UserChangeForm, UserLoginForm
from .models import User

# Home
#def home(request):
#  return render(request,'templates/oikos/home.html')

# Authentication
def login_user(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)

            return redirect("oikos:home")
        else:
            messages.error(request,"Email o Password Incorrecto")
        return redirect("Users:login")
    else:
        form = UserLoginForm()
        return render(request, "Users/create_user.html", {"form" : form})

@login_required
def logout_user(request):
    logout(request)
    return redirect("oikos:home")

# CRUD User
def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario Agregado")
        else:
            messages.error(request,"Datos Inalidos")
        return redirect("oikos:home")
    else:
        form = UserCreationForm()
        return render(request, "Users/create_user.html", {"form" : form})

@login_required
def modify_user(request, pk, *args, **kwargs):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario Modificado")
        else:
            messages.error(request,"Datos Inalidos")
        return redirect("Users:modify_user", pk=pk)
    else:
        user = User.objects.get(pk = pk)
        form = UserChangeForm(instance=user)
        return render(request, "Users/create_user.html", {"form" : form})

@login_required
def delete_user(request, pk, *args, **kwargs):
    if request.method == "GET":
        user = User.objects.get(pk = pk)
        user.delete()
        messages.error(request,"Usuario Eliminado")
    
    return redirect("oikos:home")

@login_required
def change_password_user(request):
    pass