from django.shortcuts import render, redirect
from django.forms import formset_factory
from .models import Category, Attribute
from .forms import CategoryForm, AttributeForm

def createCategory(request):
	AttributeCategoryFormset = formset_factory(AttributeForm, extra = 3)
	if request.method == "POST":
		catForm = CategoryForm(request.POST)
		attFormset = AttributeCategoryFormset(request.POST)
		if catForm.is_valid():
			category = catForm.save()
			for attForm in attFormset:
				if attForm.is_valid():
					attribute = attForm.save(commit=False)
					attribute.category = category
					attribute.save()
		return redirect("oikos:home")
	else:
		catForm = CategoryForm()
		attFormset = AttributeCategoryFormset()
		return render(request, "Inventory/create_category.html", {"form" : catForm, "formset" : attFormset})