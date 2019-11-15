from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from .forms import UserCreationForm, UserChangeForm, UserLoginForm
from .models import User

# Decorators
from .permission import is_admin, is_gestor_usuario, is_cuarto_equipo, is_tesorero, is_activo, is_pasivo
from .management.commands.create_groups import GROUPS
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
            print(User.objects.all(), request)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Bienvenido " + str(user.username))
            return redirect("Inventory:home_inventory")
        else:
            messages.error(request,"Email o Password Incorrecto")
        return redirect("Users:login")
    else:
        form = UserLoginForm()
        return render(request, "Users/login.html", {"form" : form, 'title': 'Iniciar Sesión'})

@login_required
def logout_user(request):
    logout(request)
    return redirect("oikos:home")

# CRUD User
@login_required
@is_gestor_usuario
def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name = request.POST.get('group'))
            user.groups.add(group)
            messages.success(request, "Usuario Agregado")
        else:
            messages.error(request,"Datos Invalidos")
        return redirect("oikos:home")
    else:
        form = UserCreationForm()
        context = {
            "form" : form, 
            'title': 'Crear Usuario', 
            'groups': GROUPS
        }
        return render(request, "Users/create_user.html", context)

@login_required
def modify_user(request, pk, *args, **kwargs):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            if request.user.groups.filter(Q(name='admin') | Q(name='gestor_usuarios')).exists():
                group = Group.objects.get(name = request.POST.get('group'))
                user.groups.clear()
                user.groups.add(group)
            messages.success(request, "Usuario Modificado")
        else:
            messages.error(request,"Datos Inalidos")
        return redirect("Inventory:home_inventory")
    else:
        user = User.objects.get(pk = pk)
        form = UserChangeForm(instance=user)
        context = {
            "form" : form, 
            'title': 'Modificar Usuario', 
            'groups': GROUPS, 
            'user_group': request.user.groups.first().name
        }
        return render(request, "Users/create_user.html", context)

@login_required
@is_gestor_usuario  
def delete_user(request, pk, *args, **kwargs):
    if request.method == "GET":
        user = User.objects.get(pk = pk)
        user.delete()
        messages.error(request,"Usuario Eliminado")
    
    return redirect("oikos:home")

@login_required
def change_password_user(request):
    pass