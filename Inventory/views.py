from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Attribute, Equipment, Attribute_Equipment
from .forms import CategoryForm, AttributeFormset, CatQueryForm, EquipmentForm, IntValueForm, TxtValueForm, StrValueForm, DateValueForm, BoolValueForm, ChoiceValueForm

def homeInventarioView(request):
    return render(request, "Inventory/home.html")

def createCategory(request):
	if request.method == "POST":
		catForm = CategoryForm(request.POST)
		attFormset = AttributeFormset(request.POST)
		if catForm.is_valid() and attFormset.is_valid():
			category = catForm.save()
			for attform in attFormset:
				attribute = attform.save(commit=False)
				attribute.category = category
				attribute.save()
			messages.success(request, "Category Added!")
		else:
			messages.error(request, "Failed to add Category :c")
		return redirect("oikos:home")
	else:
		catForm = CategoryForm()
		attFormset = AttributeFormset(queryset=Attribute.objects.none())
		return render(request, "Inventory/create_category.html", {"categoryform" : catForm, "formset" : attFormset})


def EquipCatSelection(request):
    if request.method == "POST":
        form = CatQueryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category'].pk
            return redirect("Inventory:create_equipment_value", cat=category)
        else:
            messages.error(request,"No existe esta categoria.")
        return redirect("oikos:home")
    else:
        form = CatQueryForm()
        return render(request, "Inventory/create_equipment.html", {"form" : form})

def createEquipment(request, cat):
	if request.method == "POST":
		equipForm = EquipmentForm(request.POST)
		catAttributes = list(Attribute.objects.filter(category=cat))
		attForms=[]
		for att in catAttributes:
			if att.attribute_type=='INT' or att.attribute_type=='FLT':
				attForms.append(IntValueForm(request.POST))
			elif att.attribute_type=='TXT':
				attForms.append(TxtValueForm(request.POST))
			elif att.attribute_type=='STR':
				attForms.append(StrValueForm(request.POST))
			elif att.attribute_type=='BOO':
				attForms.append(BoolValueForm(request.POST))
			elif att.attribute_type=='DAT':
				attForms.append(DateValueForm(request.POST))
			elif att.attribute_type=='CHO':
				attForms.append(ChoiceValueForm(request.POST))
		if equipForm.is_valid() and all(attForm.is_valid() for attForm in attForms):
			equipment= equipForm.save(commit=False)
			equipment.category = cat
			equipment.save()
			i=0
			for attForm in attForms:
				value = attForm.save(commit=False)
				value.equipment = equipment
				value.attribute = catAttributes[i]
				value.save()
				i+=1
			messages.success(request, "Equpiment Added!")
		else:
			messages.error(request, "Failed to add Category :c")
		return redirect("oikos:home")
	else:
		equipForm = EquipmentForm()
		catAttributes = list(Attribute.objects.filter(category=cat))
		attForms=[]
		for att in catAttributes:
			attName = att.name
			if att.attribute_type=='INT' or att.attribute_type=='FLT':
				attForms.append((IntValueForm(),attName))
			elif att.attribute_type=='TXT':
				attForms.append((TxtValueForm(),attName))
			elif att.attribute_type=='STR':
				attForms.append((StrValueForm(),attName))
			elif att.attribute_type=='BOO':
				attForms.append((BoolValueForm(),attName))
			elif att.attribute_type=='DAT':
				attForms.append((DateValueForm(),attName))
			elif att.attribute_type=='CHO':
				attForms.append((ChoiceValueForm(),attName))

		return render(request, "Inventory/create_equipment_value.html", {"equipform" : equipForm, "attforms" : attForms})




