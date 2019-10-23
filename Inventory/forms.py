from django import forms
from .models import Category, Attribute, Request, Request_Category

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['name']

class RequestForm(forms.ModelForm):
	class Meta:
		model = Request
		fields = ['specs', 'equipment', 'category']

class Request_CategoryForm(forms.ModelForm):
	class Meta:
		model = Request_Category
		fields = ['request', 'category', 'quantity']
