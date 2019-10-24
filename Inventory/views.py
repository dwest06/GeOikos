from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Attribute
from .forms import CategoryForm, AttributeFormset

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