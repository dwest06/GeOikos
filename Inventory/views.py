from django.shortcuts import render, redirect
from .forms import CatQueryForm, AttsQueryForm

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
        return render(request, "Inventory/search.html", {"form":form})
    else:
        form = AttsQueryForm(category)
        return render(request, "Inventory/search.html", {"form":form})

    