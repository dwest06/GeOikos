from django.shortcuts import render, redirect
from .forms import CatQueryForm, AttsQueryForm
from .models import *

# Create your views here.
def CatQueryView(request):
    if request.method == "POST":
        form = CatQueryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category'].pk
            return redirect("inventory:select-atts", category=category)
        else:
            messages.error(request,"No existe esta categoria.")
        return redirect("oikos:home")
    else:
        form = CatQueryForm()
        return render(request, "Inventory/search.html", {"form" : form})

def AttsQueryView(request, category):
    if request.method == "POST":
        form = AttsQueryForm(category,request.POST)
        if form.is_valid():
            user_atts = form.cleaned_data
            query = Equipment.objects.filter(category=category)
            for dic in Attribute.objects.filter(category=category).values():
                att_name = dic['name']
                try:
                    value = user_atts[att_name]
                except KeyError:
                    continue
                query = ...
            redirect("oikos:home")
        else:
            messages.error(request,"Error: Valores no permitidos")
        return redirect("oikos:home")
    else:
        form = AttsQueryForm(category)
        return render(request, "Inventory/search.html", {"form":form})

    