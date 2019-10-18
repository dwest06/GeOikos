from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserChangeForm
from django.contrib import messages

# Home
#def home(request):
#  return render(request,'templates/oikos/home.html')

# Authentication
def login(request):
    pass

def logout(request):
    pass

# CRUD User
def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario Agregado")
        else:
            messages.error(request,"Datos Inalidos")
        return redirect("usuarios:create_user")
    else:
        form = UserCreationForm()

        return render(request, "usuarios/create_user.html", {"form" : form})

def modify_user(request, pk, *args, **kwargs):
    if request.method == "POST":
        pass
    else:
        user = User.objects.get(pk = pk)
        form = UserChangeForm()
def delete_user(request):
    pass

def change_password_user(request):
    pass