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
            for att in Attribute.objects.filter(category=category).values():
                att_id   = att['id']
                att_name = att['name']
                att_type = att['attribute_type']
                try:
                    value = user_atts[att_name]
                except KeyError:
                    continue
                print(att_id, att_name, att_type, value)
                print(Attribute_Equipment.objects.filter(attribute=att_id, value_str=value).values())
                if att_type == 'INT' or att_type == 'FLT':
                    equipm_ids = [valent['equipment_id'] for val in Attribute_Equipment.objects.filter(attribute=att_id, value_int=value).values()]
                elif att_type == 'STR':
                    equipment_ids = [val['equipment_id'] for val in Attribute_Equipment.objects.filter(attribute=att_id, value_str=value).values()]
                elif att_type == 'TXT':
                    equipment_ids = [val['equipment_id'] for val in Attribute_Equipment.objects.filter(attribute=att_id, value_txt=value).values()]
                elif att_type == 'BOO':
                    equipment_ids = [val['equipment_id'] for val in Attribute_Equipment.objects.filter(attribute=att_id, value_boo=value).values()]
                elif att_type == 'DAT':
                    equipment_ids = [val['equipment_id'] for val in Attribute_Equipment.objects.filter(attribute=att_id, value_dat=value).values()]
                elif att_type == 'CHO':
                    equipment_ids = [val['equipment_id'] for val in Attribute_Equipment.objects.filter(attribute=att_id, value_cho=value).values()]
                query = query.filter(id__in=equipment_ids)              
            return render(request, "Inventory/table.html", {'table':query})
        else:
            messages.error(request,"Error: Valores no permitidos")
        return redirect("oikos:home")
    else:
        form = AttsQueryForm(category)
        return render(request, "Inventory/search.html", {"form":form})

    