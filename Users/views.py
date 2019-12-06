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
                messages.success(request, "Bienvenido " + str(user.username))
                return redirect("Inventory:home_inventory")
        messages.error(request,"Email o Password Incorrecto")
        return redirect("Users:login")
    else:
        form = UserLoginForm()
        return render(request, "Users/login.html", {"form" : form, 'title': 'Iniciar Sesiรณn'})

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
            try:
                group = Group.objects.get(name = request.POST.get('group'))
                user.groups.add(group)
            except:
                pass

            status = request.POST.get('status')
            if status != "":
                user.status = status
                user.save()
            messages.success(request, "Usuario Agregado")
        else:
            messages.error(request,"Datos Inválidos")
        return redirect("Inventory:manage_users")
    else:
        form = UserCreationForm()
        context = {
            "form" : form, 
            'title': 'Crear Usuario', 
            'groups': GROUPS,
            'status': dict(User.STATUS_CHOICES)
        }
        return render(request, "Users/create_user.html", context)

@login_required
def modify_user(request, pk, *args, **kwargs):
    if request.method == "POST":
        instance = User.objects.get(pk=pk)
        form = UserChangeForm(request.POST, instance=instance)
        if form.is_valid():
            user = form.save()
            if request.user.groups.filter(Q(name='admin') | Q(name='gestor_usuarios')).exists():
                try:
                    group = Group.objects.get(name = request.POST.get('group'))
                    user.groups.clear()
                    user.groups.add(group)
                except:
                    pass
                status = request.POST.get('status')
                if status != "":
                    user.status = status
                    user.save()
            messages.success(request, "Usuario Modificado")
        else:
            messages.error(request,"Datos Inalidos")
        return redirect("Inventory:home_inventory")
    
    if((request.user.groups.first().name != 'admin' or
        request.user.groups.first().name != 'gestor_usuarios') and 
        request.user.pk != pk):
        messages.error(request,"Operaci?n no permitida.")
        return redirect("Inventory:home_inventory") 
        
    user = User.objects.get(pk = pk)
    form = UserChangeForm(instance=user)
    context = {
        "form" : form, 
        'title': 'Modificar Usuario', 
        'groups': GROUPS, 
        'user_group': request.user.groups.first().name,
        'status': dict(User.STATUS_CHOICES)
    }
    return render(request, "Users/create_user.html", context)

@login_required
@is_gestor_usuario  
def delete_user(request, *args, **kwargs):
    if request.method == "POST":
        pk = request.POST.get("user")
        user = User.objects.get(pk = pk)
        user.delete()
        messages.success(request,"Usuario Eliminado Exitosamente")
    
    return redirect("Inventory:manage_users")

@login_required
def change_password_user(request):
    pass