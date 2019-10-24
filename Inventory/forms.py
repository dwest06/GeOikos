from django import forms
from django.forms import modelformset_factory
from .models import Category, Equipment, Attribute, Group, Request, Request_Category, Loan, Repair, EquipmentDebt, Transaction

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['name']
		labels = {
			'name' : 'Category Name'
		}

class EquipmentForm(forms.ModelForm):
	class Meta:
		model = Equipment
		fields = [
				'serial', 'name', 'entry_date', 
				'elaboration_date', 'notes', 'category'
			]
		labels = {
			'serial' : 'Serial No.',
			'name' : 'Equipment Name',
			'entry_date' : 'Entry Date',
			'elaboration_date' : 'Elaboration Date',
			'notes' : 'Notes',
			'category' : 'Category'
		}

AttributeFormset = modelformset_factory(
	Attribute,
	fields = ['name', 'attribute_type', 'unit', 'nullity'],
	extra = 1,
	labels = {
		'name' : 'Attribute Name',
		'attribute_type' : 'Type',
		'unit' : 'Unit',
		'nullity' : 'Not Essential'
	}
)

class GroupForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = ['name']

class RequestForm(forms.ModelForm):
	class Meta:
		model = Request
		fields = ['specs', 'equipment', 'category']

class Request_CategoryForm(forms.ModelForm):
	class Meta:
		model = Request_Category
		fields = ['request', 'category', 'quantity']

class LoanCreationForm(forms.ModelForm):
	class Meta:
		model = Loan 
		fields = ['equipment', 'user', 'hand_over_date']

class LoanDevolutionForm(forms.ModelForm):
	class Meta:
		model = Loan
		fields = ['delivery_date', 'score', 'notes']

class RepairCreationForm(forms.ModelForm):
	class Meta:
		model = Repair
		fields = ['equipment', 'notes']

class RepairHandOverForm(forms.ModelForm):
	class Meta:
		model = Repair
		fields = ['repairer', 'hand_over_date', 'notes']

class RepairDevolutionForm(forms.ModelForm):
	class Meta:
		model = Repair
		fields = ['return_date', 'notes']

class EquipmentDebtCreationForm(forms.ModelForm):
	class Meta:
		model = EquipmentDebt
		fields = ['user', 'category', 'damage_date', 'specs']

class EquipmentDebtReturnForm(forms.ModelForm):
	class Meta:
		model = EquipmentDebt
		fields = ['return_date', 'specs']

class TransactionForm(forms.ModelForm):
	class Meta:
		model = Transaction
		fields = ['user', 'transaction', 'reason']