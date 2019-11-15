from django import forms
from django.forms import formset_factory, modelformset_factory
from .models import (Category, Equipment, Attribute, Group, 
                    Request, Request_Category, Loan, Repair, 
                    EquipmentDebt, Transaction, Attribute_Equipment)
from django.core.validators import MaxValueValidator

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name' : 'Nombre de la categoria'
        }
        error_messages = {
            'name' : {
                'required' : 'Campo obligatorio'
            }
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
                'serial', 'name', 'entry_date', 
                'elaboration_date', 'notes', 'group'
            ]
        labels = {
            'serial' : 'Serial',
            'name' : 'Nombre del Equipo',
            'entry_date' : 'Fecha de Entrada',
            'elaboration_date' : 'Fecha de Elaboracion',
            'notes' : 'Notas',
            'group' : 'Grupo'
        }
        error_messages = {
            'serial' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Entrada inválida',
            },
            'name' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Entrada inválida',
                'max_length' : 'Máximo de caracteres excedido',
            },
            'entry_date' : {
                'invalid' : 'Fecha inválida',
            },
            'elaboration_date' : {
                'invalid' : 'Fecha inválida',
            }
        }

AttributeFormset = modelformset_factory(
    Attribute,
    fields = ['name', 'attribute_type', 'unit', 'nullity'],
    extra = 1,
    labels = {
        'name' : 'Nombre del Atributo',
        'attribute_type' : 'Tipo de dato',
        'unit' : 'Unidad',
        'nullity' : '(Unidad no esencial)'
    },
    error_messages = {
        'name' : {
            'required' : 'Campo obligatorio',
            'invalid' : 'Entrada inválida',
            'max_length' : 'Máximo de caracteres excedido',
        },
        'attribute_type' : {
            'required' : 'Campo obligatorio',
            'invalid' : 'Entrada inválida',
        },
        'unit' : {
            'invalid' : 'Entrada inválida',
            'max_length' : 'Máximo de caracteres excedido',
        }
    }
)

class IntValueForm(forms.ModelForm):
    class Meta:
        model = Attribute_Equipment
        fields = ['value_int']
        labels = { 'value_int' : ''}

        error_messages = {
            'value_int' : {
                'invalid' : 'Entrada inválida'
            }
        }

class TxtValueForm(forms.ModelForm):
    class Meta:
        model = Attribute_Equipment
        fields = ['value_txt']
        labels = { 'value_txt' : ''}

        error_messages = {
            'value_txt' : {
                'invalid' : 'Entrada inválida',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class StrValueForm(forms.ModelForm):
    class Meta:
        model = Attribute_Equipment
        fields = ['value_str']
        labels = { 'value_str' : ''}

        error_messages = {
            'value_str' : {
                'invalid' : 'Entrada inválida',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class DateValueForm(forms.ModelForm):
    class Meta:
        model = Attribute_Equipment
        fields = ['value_date']
        labels = { 'value_date' : ''}

        error_messages = {
            'value_date' : {
                'invalid' : 'Fecha inválida',
            }
        }

class BoolValueForm(forms.ModelForm):
    class Meta:
        model = Attribute_Equipment
        fields = ['value_bool']
        labels = { 'value_bool' : ''}

class ChoiceValueForm(forms.ModelForm):
    class Meta:
        model = Attribute_Equipment
        fields = ['value_cho']
        labels = { 'value_cho' : ''}


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

        error_messages = {
            'name' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Entrada inválida',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['user', 'specs', 'equipment', 'category']

        error_messages = {
            'specs' : {
                'invalid' : 'Entrada inválida',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class Request_CategoryForm(forms.ModelForm):
    class Meta:
        model = Request_Category
        fields = ['request', 'category', 'quantity']

        error_messages = {
            'request' : {
                'required' : 'Campo obligatorio',
            },
            'category' : {
                'required' : 'Campo obligatorio',
            },
            'quantity' : {
                'required' : 'Campo obligatorio'
            }
        }

class LoanCreationForm(forms.ModelForm):
    class Meta:
        model = Loan 
        fields = ['equipment', 'user', 'hand_over_date']
        labels = {
            'equipment' : 'Equipo',
            'user' : 'Usuario',
            'hand_over_date' : 'Fecha'
        }

        error_messages = {
            'equipment' : {
                'required' : 'Campo obligatorio',
            },
            'user' : {
                'required' : 'Campo obligatorio',
            },
            'hand_over_date' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Fecha inválida'
            }
        }

class LoanDevolutionForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['delivery_date', 'score', 'notes']
        labels = {
            'delivery_date' : 'Fecha',
            'score' : 'Puntaje',
            'notes' : 'Notas'
        }

        error_messages = {
            'delivery_date' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Fecha inválida'
            },
            'score' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Entrada inválida'
            },
            'notes' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class RepairCreationForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ['equipment', 'notes']

        error_messages = {
            'equipment' : {
                'required' : 'Campo obligatorio',
            },
            'notes' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class RepairHandOverForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ['repairer', 'hand_over_date', 'notes']

        error_messages = {
            'repairer' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            },
            'hand_over_date' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Fecha inválida'
            },
            'notes' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class RepairDevolutionForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ['return_date', 'notes']

        error_messages = {
            'return_date' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Fecha inválida'
            },
            'notes' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class EquipmentDebtCreationForm(forms.ModelForm):
    class Meta:
        model = EquipmentDebt
        fields = ['user', 'category', 'damage_date', 'specs']

        error_messages = {
            'user' : {
                'required' : 'Campo obligatorio',
            },
            'category' : {
                'required' : 'Campo obligatorio',
            },
            'damage_date' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Fecha inválida'
            },
            'specs' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class EquipmentDebtReturnForm(forms.ModelForm):
    class Meta:
        model = EquipmentDebt
        fields = ['return_date', 'specs']

        error_messages = {
            'return_date' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Fecha inválida'
            },
            'specs' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user', 'transaction', 'reason']
        labels = {
            'user' : 'Usuario: ',
            'transaction'  : 'Monto: ',
            'reason' : 'Motivo: '
        }
        error_messages = {
            'user' : {
                'required' : 'Campo obligatorio',
            },
            'transaction' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Entrada inválida',
                'max_digits' : 'Máximo de 7 dígitos',
                'max_decimals' : 'Máximo de 2 decimales'
            }
        }

class CatReqForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    quantity = forms.IntegerField(label="quantity", required=True, initial=1)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("Debes especificar una cantidad positiva")
        return quantity

class CatQueryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Categoría: ')

CatReqFormset = formset_factory(
    CatReqForm,
    extra = 1
)

class EqReqForm(forms.Form):
    equipment = forms.ModelChoiceField(queryset=Equipment.objects.all())

class CommentsReqForm(forms.Form):
    comments = forms.CharField(required=False, widget=forms.Textarea)

EqReqFormset = formset_factory(
    EqReqForm,
    extra = 1
)

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
    