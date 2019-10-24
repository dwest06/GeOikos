from django.shortcuts import render, redirect
from .forms import SearchForm, EquipmentForm

# Create your views here.
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        form1 = AForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            return redirect("oikos:home", {category:category})
        else:
            messages.error(request,"Email o Password Incorrecto")
        return redirect("Users:login")
    else:
        form = EquipmentForm()
        print(form)
        return render(request, "Inventory/search.html", {"form" : form})

# def instance_category(request, category):
#     if methog get:
#         form = nuevoforrmcat(categ).__init__(ca)

    