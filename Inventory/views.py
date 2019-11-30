from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from Users.models import User
from Users.permission import is_admin, is_gestor_usuario, is_cuarto_equipo, is_tesorero, is_activo, is_pasivo

######################
## VISTAS PRINCIPALES
######################
@login_required
def home_inventario_view(request):
    context = {
        'deuda' : 0.00,
        'grupo' : request.user.groups.all().first()
    }
    return render(request, "Inventory/home.html", context)

@login_required
@is_tesorero
def home_tesorero_view(request):
    if request.method == "GET":
        context = {
            "trimestral" : Transaction.objects.filter(reason='T'),
            "pagos" : Transaction.objects.filter(reason='P'),
            "multas" : Transaction.objects.filter(reason='M')

        }
    return render(request, "Inventory/tesorero.html", context)

@login_required
@is_cuarto_equipo
def home_cuarto_equipo_view(request):
    if request.method == "GET":
        context = {
            "prestamos" : Loan.objects.all(),
            "solicitudes" : Request.objects.all(),
            "categorias" : Category.objects.all(),
            "equipos" : Equipment.objects.all(),
        }
    return render(request, "Inventory/cuarto_equipo.html", context)

@login_required
@is_admin
def create_category(request):
    if request.method == "POST":
        cat_form = CategoryForm(request.POST)
        att_formset = AttributeFormset(request.POST)
        if cat_form.is_valid() and att_formset.is_valid():
            category = cat_form.save()
            for attform in att_formset:
                attribute = attform.save(commit=False)
                attribute.category = category
                attribute.save()
            messages.success(request, "Categoria añadida")
            return redirect("Inventory:create_category")
        else:
            messages.error(request, "Fallo al añadir categoria")
            return redirect("Inventory:home_inventory")
    else:
        category_form = CategoryForm()
        att_formset = AttributeFormset(queryset=Attribute.objects.none())
        return render(request, "Inventory/create_category.html", {"categoryform" : category_form, "formset" : att_formset})

@login_required
@is_cuarto_equipo
def create_group(request):
    if request.method == "POST":
        gr_form = GroupForm(request.POST)
        if gr_form.is_valid():
            gr_form.save()
            messages.success(request, "Grupo añadido")
        else:
            messages.error(request, "Fallo al añadir grupo")
        return redirect("Inventory:home_inventory")
    else:
        gr_form = GroupForm()
        return render(request, "Inventory/create_group.html", {"form" : gr_form})

@login_required
@is_cuarto_equipo
def equip_cat_selection(request):
    if request.method == "POST":
        form = CatQueryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category'].pk
            return redirect("Inventory:create_equipment_value", cat=category)
        else:
            messages.error(request,"No existe esta categoría.")
            return redirect("Inventory:home_inventory")
    else:
        form = CatQueryForm()
        return render(request, "Inventory/create_equipment.html", {"form" : form, })

@login_required
@is_cuarto_equipo
def create_equipment(request, cat):    
    if request.method == "POST":
        equip_form = EquipmentForm(request.POST)
        cat_attributes = list(Attribute.objects.filter(category=cat))
        att_forms=[]
        for att in cat_attributes:
            if att.attribute_type=='INT' or att.attribute_type=='FLT':
                att_forms.append(IntValueForm(request.POST))
            elif att.attribute_type=='TXT':
                att_forms.append(TxtValueForm(request.POST))
            elif att.attribute_type=='STR':
                att_forms.append(StrValueForm(request.POST))
            elif att.attribute_type=='BOO':
                att_forms.append(BoolValueForm(request.POST))
            elif att.attribute_type=='DAT':
                att_forms.append(DateValueForm(request.POST))
            elif att.attribute_type=='CHO':
                att_forms.append(ChoiceValueForm(request.POST))
        if equip_form.is_valid() and all(att_form.is_valid() for att_form in att_forms):
            equipment= equip_form.save(commit=False)
            equipment.category = Category.objects.get(pk=cat)
            equipment.save()
            i=0
            for att_form in att_forms:
                value = att_form.save(commit=False)
                value.equipment = equipment
                value.attribute = cat_attributes[i]
                value.save()
                i+=1
            messages.success(request, "Equipo Agregado")
        else:
            messages.error(request, "Fallo al agregar equipo")
        return redirect("Inventory:home_inventory")
    else:
        equip_form = EquipmentForm()
        cat_attributes = list(Attribute.objects.filter(category=cat))
        att_forms=[]
        for att in cat_attributes:
            att_name = att.name
            if att.attribute_type=='INT' or att.attribute_type=='FLT':
                att_forms.append((IntValueForm(),att_name))
            elif att.attribute_type=='TXT':
                att_forms.append((TxtValueForm(),att_name))
            elif att.attribute_type=='STR':
                att_forms.append((StrValueForm(),att_name))
            elif att.attribute_type=='BOO':
                att_forms.append((BoolValueForm(),att_name))
            elif att.attribute_type=='DAT':
                att_forms.append((DateValueForm(),att_name))
            elif att.attribute_type=='CHO':
                att_forms.append((ChoiceValueForm(),att_name))


        return render(request, "Inventory/create_equipment_value.html", context = {
            "equipform" : equip_form, "attforms" : att_forms, 'page_title': 'Crear Equipo'}
            )

@login_required
@is_activo
def create_request(request):
    if request.method == "POST":
        catformset = CatReqFormset(request.POST)
        eqformset  = EqReqFormset(request.POST)
        comments   = CommentsReqForm(request.POST)
       
        if catformset.is_valid() and eqformset.is_valid() and comments.is_valid():
            request_obj = Request.objects.create(user=request.user)
            request_obj.specs = comments.cleaned_data['comments']
            
            for form in catformset: 
                try:
                    category = form.cleaned_data['category'].pk              
                    quantity = form.cleaned_data['quantity']
                except KeyError:
                    continue
                requestcat =  RequestCategory.objects.create(
                                category=Category.objects.get(pk=category),
                                request=request_obj,
                                quantity=form.cleaned_data['quantity']
                              )
                requestcat.save()
            
            request_obj.save()

            for form in eqformset:
                try:
                    equipment = form.cleaned_data['equipment'].pk
                except KeyError:
                    continue
                request_obj.equipment.add(Equipment.objects.get(pk=equipment))
        
        else:
            messages.error(request,"Formularios Inválidos")
            return redirect("Inventory:create_request")
        
        messages.success(request,"Solicitud enviada")
        return redirect("Inventory:create_request")

    else:
        catform = CatReqFormset()
        eqform = EqReqFormset()
        comments = CommentsReqForm()
        return render(request, "Inventory/create_request.html", 
                      {"catformset" : catform, "eqformset" : eqform, "comments" : comments})

@login_required
@is_pasivo
def cat_query_view(request):
    if request.method == "POST":
        form = CatQueryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category'].pk
            return redirect("Inventory:show_equipment", category=category)
        else:
            messages.error(request,"No existe esta categoria.")
        return redirect("Inventory:home_inventory")
    else:
        form = CatQueryForm()
        return render(request, "Inventory/search.html", {"form" : form})

@login_required
@is_pasivo
def atts_query_view(request, category):
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
                    assert(value)
                except (KeyError, AssertionError):
                    continue
                if att_type == 'INT' or att_type == 'FLT':
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_int=value).values()]
                elif att_type == 'STR':
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_str=value).values()]
                elif att_type == 'TXT':
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_txt=value).values()]
                elif att_type == 'BOO':
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_boo=value).values()]
                elif att_type == 'DAT':
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_dat=value).values()]
                elif att_type == 'CHO':
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_cho=value).values()]
                query = query.filter(id__in=equipment_ids)              
            return render(request, "Inventory/table.html", {'table':query})
        else:
            messages.error(request,"Error: Valores no permitidos")
        return redirect("Inventory:home_inventory")
    else:
        form = AttsQueryForm(category)
        return render(request, "Inventory/search.html", {"form":form})

# VISTAS DE GESTOR DE USUARIOS
@login_required
@is_gestor_usuario
def manage_users(request, *args, **kwargs):
    return render(request, 'Inventory/manage_user.html', {'users': User.objects.all()})

@login_required
@is_cuarto_equipo
def loan_creation(request):
    if request.method == "POST":
        lc_form = LoanCreationForm(request.POST)
        if lc_form.is_valid():
            lc_form.save()
            messages.success(request, "Prestamo cargado")
        else:
            messages.error(request, "Fallo al cargar prestamo")
        return redirect("Inventory:home_inventory")
    else:
        lc_form = LoanCreationForm()
        return render(request, "Inventory/create_loan.html", {"form" : lc_form})

@login_required
@is_pasivo
def show_equipment(request,category):
    atts = Attribute.objects.filter(category=category)
    equip = Equipment.objects.filter(category=category)
    vals = []
    for eq in equip:
        vals2 = [eq.name, eq.serial, eq.entry_date, eq.elaboration_date, eq.discontinued, eq.discontinued_date, eq.notes, eq.category]
        for att in atts:
            att_type=att.attribute_type
            val=AttributeEquipmet.objects.get(attribute=att,equipment=eq)
            if att_type == 'INT' or att_type == 'FLT':
                vals2.append(val.value_int)
            elif att_type == 'STR':
                vals2.append(val.value_str)
            elif att_type == 'TXT':
                vals2.append(val.value_txt)
            elif att_type == 'BOO':
                vals2.append(val.value_boo)
            elif att_type == 'DAT':
                vals2.append(val.value_dat)
            elif att_type == 'CHO':
                vals2.append(val.value_cho)
        vals.append(vals2)
    return render(request, "Inventory/equipment_table.html", {'attributes': atts, 'values':vals})

@login_required
@is_tesorero
def load_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid() and form.cleaned_data['transaction'] > 0.00:
            trans = form.save(commit = False)
            if trans.reason != 'P':
                trans.transaction *= -1
            trans.save()
            messages.success(request, "Transacción cargada")
        else:
            messages.error(request, "Fallo al cargar transacción")
        return redirect("Inventory:tesorero")
    form = TransactionForm()
    return render(request, "Inventory/load_transaction.html", {"form" : form, "heading": "Cargar Transacciones"})
