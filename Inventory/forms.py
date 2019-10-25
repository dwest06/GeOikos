from django import forms
from django.forms import modelformset_factory
from .models import (Category, Equipment, Attribute, Group, 
                    Request, Request_Category, Loan, Repair,
                    EquipmentDebt, Transaction, Attribute_Equipment)
from django.core.validators import MaxValueValidator

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
				'elaboration_date', 'notes', 'group'
			]
		labels = {
			'serial' : 'Serial No.',
			'name' : 'Equipment Name',
			'entry_date' : 'Entry Date',
			'elaboration_date' : 'Elaboration Date',
			'notes' : 'Notes',
			'group' : 'Group'
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

class IntValueForm(forms.ModelForm):
	class Meta:
		model = Attribute_Equipment
		fields = ['value_int']
		labels = { 'value_int' : ''}
	def add_prefix(self, field_name):
		return super(IntValueForm, self).add_prefix('value')

class TxtValueForm(forms.ModelForm):
	class Meta:
		model = Attribute_Equipment
		fields = ['value_txt']
		labels = { 'value_txt' : ''}
	def add_prefix(self, field_name):
		return super(TxtValueForm, self).add_prefix('value')

class StrValueForm(forms.ModelForm):
	class Meta:
		model = Attribute_Equipment
		fields = ['value_str']
		labels = { 'value_str' : ''}
	def add_prefix(self, field_name):
		return super(StrValueForm, self).add_prefix('value')

class DateValueForm(forms.ModelForm):
	class Meta:
		model = Attribute_Equipment
		fields = ['value_date']
		labels = { 'value_date' : ''}
	def add_prefix(self, field_name):
		return super(DateValueForm, self).add_prefix('value')

class BoolValueForm(forms.ModelForm):
	class Meta:
		model = Attribute_Equipment
		fields = ['value_bool']
		labels = { 'value_bool' : ''}
	def add_prefix(self, field_name):
		return super(BoolValueForm, self).add_prefix('value')

class ChoiceValueForm(forms.ModelForm):
	class Meta:
		model = Attribute_Equipment
		fields = ['value_cho']
		labels = { 'value_cho' : ''}
	def add_prefix(self, field_name):
		return super(ChoiceValueForm, self).add_prefix('value')




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

class CatQueryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

class AttsQueryForm(forms.Form):

    def __init__(self, category, *args, **kwargs):
        
        super(AttsQueryForm, self).__init__(*args, **kwargs)

        for att in Attribute.objects.filter(category=category):
            if att.attribute_type == 'INT' or att.attribute_type == 'FLT':
                self.fields[att.name] = forms.IntegerField(label=att.name, required=att.nullity)
            elif att.attribute_type == 'STR':
                self.fields[att.name] = forms.CharField(max_length=100, label=att.name, required=att.nullity)
            elif att.attribute_type == 'TXT':
                self.fields[att.name] = forms.CharField(label=att.name, required=att.nullity)
            elif att.attribute_type == 'BOO':
                self.fields[att.name] = forms.BooleanField(label=att.name, required=att.nullity)
            elif att.attribute_type == 'DAT':
                self.fields[att.name] = forms.DateField(label=att.name, required=att.nullity)
            elif att.attribute_type == 'CHO':
                CHOICES = [dic['option_name'] for dic in Choices.objects.filter(attribute=att).values('option_name')]
                self.fields[att.name] = forms.ChoiceField(choices=CHOICES, label=att.name, required=att.nullity)
    
