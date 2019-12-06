from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import *
from .forms import *
from Users.models import User
from Users.permission import is_admin, is_gestor_usuario, is_cuarto_equipo, is_tesorero, is_activo, is_pasivo
import datetime

######################
## VISTAS PRINCIPALES
######################
@login_required
def home_inventario_view(request):
    user = User.objects.get(pk=request.user.pk)

    # Deuda total
    deuda = Decimal(0)
    for i in user.transaction_set.all():
        deuda -= i.transaction

    # Solicitudes

    context = {
        'deuda' : deuda,
        'trans' : Transaction.objects.filter(user=user),
        'grupo' : request.user.groups.all().first().name,
        'solicitudes' : Request.objects.filter(user1=user),
        'prestamos' : Loan.objects.filter(user=user)
    }
    return render(request, "Inventory/home.html", context)

@login_required
@is_tesorero
def home_tesorero_view(request):
    if request.method == "GET":
        context = {
            "trimestral" : Transaction.objects.filter(reason='T'),
            "pagos" : Transaction.objects.filter(reason='P'),
            "multas" : Transaction.objects.filter(reason='M'),
            "trim" : Quarterly.objects.get_or_create(pk=1)[0].amount
        }
    return render(request, "Inventory/tesorero.html", context)

@login_required
@is_cuarto_equipo
def home_cuarto_equipo_view(request):
    if request.method == "GET":
        borrowedEq = [ x['equipment'] for x in Loan.borrowedEq() ]
        discontinuedEq = [ x['id'] for x in Equipment.discontinuedEq() ]
        equipment = []
        for eq in Equipment.objects.all():
            available = 'Disponible'
            if(eq.id in borrowedEq):
                available = 'Prestado'
            elif(eq.id in discontinuedEq):
                available = 'Descontinuado'
            equipment.append((eq,available))
        context = {
            "prestamos" : Loan.objects.all(),
            "solicitudes" : Request.objects.all(),
            "categorias" : Category.objects.all(),
            "equipos" : equipment
        }
    return render(request, "Inventory/cuarto_equipo.html", context)

@login_required
@is_admin
def create_category(request):
    if request.method == "POST":
        cat_form = CategoryForm(request.POST)
        if cat_form.is_valid():
            category = cat_form.save()
            names = request.POST.getlist('att_name')
            types = request.POST.getlist('att_type')
            units = request.POST.getlist('unit')
            nulls = request.POST.getlist('nullity')
            for i in range(0,len(names)):
                att = Attribute(name=names[i],attribute_type=types[i],unit=units[i])
                if(nulls[i] == 'Opcional'):
                    att.nullity = True
                att.category = category
                att.save()
            messages.success(request, "Categoria añadida")
            return redirect("Inventory:create_category")
        else:
            messages.error(request, "Fallo al añadir categoria")
            return redirect("Inventory:home_inventory")
    else:
        category_form = CategoryForm()
        return render(request, "Inventory/create_category.html", {"categoryform" : category_form})

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
        return render(request, "Inventory/create_equipment.html", {"form" : form })

def filterAndFill(lists, attributes):
    atts = []
    idxs = [0,0,0,0,0,0]
    for att in attributes:
        att_val = AttributeEquipmet()
        print(lists)
        if att.attribute_type=='INT': #0
            if att.nullity and lists[0][idxs[0]] == '':
                att_val.value_int = None
            else:
                if lists[0][idxs[0]] == '':
                    messages.error(request, "Fallo al agregar equipo")
                    return render(request, "Inventory:create-equipment")
                att_val.value_int = int(lists[0][idxs[0]])
                idxs[0]+=1
        elif att.attribute_type=='TXT': #1
            if att.nullity and lists[1][idxs[1]] == '':
                att_val.value_txt = None
            else:
                if lists[1][idxs[1]] == '':
                    messages.error(request, "Fallo al agregar equipo")
                    return render(request, "Inventory:create-equipment")
                att_val.value_txt = lists[1][idxs[1]]
                idxs[1]+=1
        elif att.attribute_type=='STR': #2
            if att.nullity and lists[2][idxs[2]] == '':
                att_val.value_str = None
            else:
                if lists[2][idxs[2]] == '':
                    messages.error(request, "Fallo al agregar equipo")
                    return render(request, "Inventory:create-equipment")
                att_val.value_str = lists[2][idxs[2]]
                idxs[2]+=1
        elif att.attribute_type=='BOO': #3
            if att.nullity and lists[3][idxs[3]] == '':
                att_val.value_bool = None
            else:
                if lists[3][idxs[3]] == '':
                    messages.error(request, "Fallo al agregar equipo")
                    return render(request, "Inventory:create-equipment")
                att_val.value_bool = (lists[3][idxs[3]] == "True")
                idxs[3]+=1
        elif att.attribute_type=='DAT': #4
            if att.nullity and lists[4][idxs[4]] == '':
                att_val.value_date = None
            else:
                if lists[4][idxs[4]] == '':
                    messages.error(request, "Fallo al agregar equipo")
                    return render(request, "Inventory:create-equipment")
                att_val.value_date = lists[4][idxs[4]]
                idxs[4]+=1
        elif att.attribute_type=='FLT': #5
            if att.nullity and lists[5][idxs[5]] == '':
                att_val.value_float = None
            else:
                if lists[5][idxs[5]] == '':
                    messages.error(request, "Fallo al agregar equipo")
                    return render(request, "Inventory:create-equipment")
                att_val.value_float = Decimal(lists[5][idxs[5]])
                idxs[5]+=1
        att_val.attribute = att
        atts.append(att_val)
    return atts

@login_required
@is_cuarto_equipo
def create_equipment(request, cat):    
    if request.method == "POST":
        equip_form = EquipmentForm(request.POST,request.FILES)

        if equip_form.is_valid():
            
            equipment = equip_form.save(commit=False)
            
            if not Category.objects.filter(pk=cat).exists():
                messages.error(request, "Categoría inexistente")
                return render(request, "Inventory:create-equipment")
            
            equipment.category = Category.objects.get(pk=cat)
            cat_attributes = list(Attribute.objects.filter(category=cat))
            lists = [
                request.POST.getlist('value_int'),
                request.POST.getlist('value_txt'),
                request.POST.getlist('value_str'),
                request.POST.getlist('value_bool'),
                request.POST.getlist('value_date'),
                request.POST.getlist('value_float')
            ]
            att_val = filterAndFill(lists,cat_attributes)
            equipment.save()
            for group in request.POST.getlist('group'):
                if group != '':
                    g = Group.objects.get(name=group)
                    equipment.group.add(g)
            for att in att_val:
                att.equipment = equipment
                att.save()
            messages.success(request, "Equipo Agregado")
            return redirect("Inventory:home_inventory")
        else:                
            messages.error(request, "Fallo al agregar equipo")
            return render(request, "Inventory:ḧome_inventory")
    else:
        equip_form = EquipmentForm()
        cat_attributes = list(Attribute.objects.filter(category=cat))
        att_forms=[]
        for att in cat_attributes:
            att_name = att.name
            att_required = not att.nullity
            if att.attribute_type=='INT':
                form = IntValueForm(att_required)
            elif att.attribute_type=='TXT':
                form = TxtValueForm(att_required)
            elif att.attribute_type=='STR':
                form = StrValueForm(att_required)
            elif att.attribute_type=='BOO':
                form = BoolValueForm(att_required)
            elif att.attribute_type=='DAT':
                form = DateValueForm(att_required)
            elif att.attribute_type=='CHO':
                form = ChoiceValueForm(att_required)
            elif att.attribute_type=='FLT':
                form = FltValueForm(att_required)
            att_forms.append((form,att_name,att_required))
        groups = Group.objects.all()
        return render(request, "Inventory/create_equipment_value.html", context = {
            "equipform" : equip_form, "attforms" : att_forms, 'groups':groups, 'page_title': 'Crear Equipo'
            })

def filterAndFillM(lists, attributes, equipment):
    atts = []
    idxs = [0,0,0,0,0,0]
    for att in attributes:
        att_val = AttributeEquipmet.objects.get(equipment=equipment,attribute=att)
        if att.attribute_type=='INT': #0
            if att.nullity and lists[0][idxs[0]] == '':
                att_val.value_int = None
            else:
                if lists[0][idxs[0]] == '':
                    messages.error(request, "Fallo al agregar equipo")
                    return render(request, "Inventory:create-equipment")
                att_val.value_int = int(lists[0][idxs[0]])
                idxs[0]+=1
        elif att.attribute_type=='TXT': #1
            if att.nullity and lists[1][idxs[1]] == '':
                att_val.value_txt = None
            else:
                if lists[1][idxs[1]] == '':
                    messages.error(request, "Fallo al agregar equipo")
                    return render(request, "Inventory:create-equipment")
                att_val.value_txt = lists[1][idxs[1]]
                idxs[1]+=1
        elif att.attribute_type=='STR': #2
            if att.nullity and lists[2][idxs[2]] == '':
                att_val.value_str = None
            else:
                if lists[2][idxs[2]] == '':
                    messages.error(request, "Fallo al agregar equipo")
                    return render(request, "Inventory:create-equipment")
                att_val.value_str = lists[2][idxs[2]]
                idxs[2]+=1
        elif att.attribute_type=='BOO': #3
            if att.nullity and lists[3][idxs[3]] == '':
                att_val.value_bool = None
            else:
                if lists[3][idxs[3]] == '':
                    messages.error(request, "Fallo al agregar equipo")
                    return render(request, "Inventory:create-equipment")
                att_val.value_bool = (lists[3][idxs[3]] == "True")
                idxs[3]+=1
        elif att.attribute_type=='DAT': #4
            if att.nullity and lists[4][idxs[4]] == '':
                att_val.value_date = None
            else:
                if lists[4][idxs[4]] == '':
                    messages.error(request, "Fallo al agregar equipo")
                    return render(request, "Inventory:create-equipment")
                att_val.value_date = lists[4][idxs[4]]
                idxs[4]+=1
        elif att.attribute_type=='FLT': #5
            if att.nullity and lists[5][idxs[5]] == '':
                att_val.value_float = None
            else:
                if lists[5][idxs[5]] == '':
                    messages.error(request, "Fallo al agregar equipo")
                    return render(request, "Inventory:create-equipment")
                att_val.value_float = Decimal(lists[5][idxs[5]])
                idxs[5]+=1
        att_val.attribute = att
        atts.append(att_val)
    return atts

@login_required
@is_cuarto_equipo
def modify_equipment(request,eq_id):    
    if request.method == "POST":
        equip_form = EquipmentForm(request.POST, request.FILES)
       
        if equip_form.is_valid():

            if not Equipment.objects.filter(pk=eq_id).exists():
                messages.error(request, "Esta instancia de equipo no existe.")
                return render(request, "Inventory:home_inventory")

            eq_obj = Equipment.objects.get(pk=eq_id)
            
            equipment = equip_form.save(commit=False)
            equipment.id = eq_id

            if request.FILES.get('pic') is None:
                equipment.pic = eq_obj.pic

            equipment.category = Category.objects.get(pk=eq_obj.category.pk)
            cat_attributes = list(Attribute.objects.filter(category=eq_obj.category.pk))
            lists = [
                request.POST.getlist('value_int'),
                request.POST.getlist('value_txt'),
                request.POST.getlist('value_str'),
                request.POST.getlist('value_bool'),
                request.POST.getlist('value_date'),
                request.POST.getlist('value_float')
            ]
            att_val = filterAndFillM(lists,cat_attributes,eq_id)
            equipment.save()
            for group in request.POST.getlist('group'):
                if group != '':
                    g = Group.objects.get(name=group)
                    equipment.group.add(g)
            for att in att_val:
                att.save()
            messages.success(request, "Equipo Agregado")
            return redirect("Inventory:home_inventory")
        else:                
            messages.error(request, "Fallo al agregar equipo")
            return render(request, "Inventory:ḧome_inventory")
    else:

        if not Equipment.objects.filter(pk=eq_id).exists():
            messages.error(request, "Esta instancia de equipo no existe.")
            return render(request, "Inventory:ḧome_inventory")

        eq_obj = Equipment.objects.get(pk=eq_id)
        initial = {
            'serial' : eq_obj.serial,
            'name' : eq_obj.name,
            'notes': eq_obj.notes
        }
        entry_date = str(eq_obj.entry_date)
        elab_date = str(eq_obj.elaboration_date)

        equip_form = EquipmentForm(initial=initial)

        cat_attributes = list(Attribute.objects.filter(category=eq_obj.category))
        att_forms=[]
        for att in cat_attributes:
            att_name = att.name
            att_required = not att.nullity
            val = AttributeEquipmet.objects.get(equipment=eq_obj.pk,attribute=att.pk)
            if att.attribute_type=='INT':
                initial = {'value_int': val.value_int}
                form = IntValueForm(att_required, initial=initial)
            elif att.attribute_type=='TXT':
                initial = {'value_txt': val.value_txt }
                form = TxtValueForm(att_required, initial=initial)
            elif att.attribute_type=='STR':
                initial = {'value_str': val.value_str }
                form = StrValueForm(att_required, initial=initial)
            elif att.attribute_type=='BOO':
                initial = {'value_bool': val.value_bool }
                form = BoolValueForm(att_required, initial=initial)
            elif att.attribute_type=='DAT':
                initial = {'value_date': val.value_date }
                form = DateValueForm(att_required, initial=initial)
            elif att.attribute_type=='FLT':
                print(val.value_float)
                initial = {'value_float': val.value_float }
                form = FltValueForm(att_required, initial=initial)
            att_forms.append((form,att_name,att_required))
        groups = Group.objects.all()

        return render(request, "Inventory/modify_equipment_value.html", context = {
            'attforms' : att_forms,
            "equipform" : equip_form,
            "entry_date": entry_date,
            "elab_date" : elab_date
            })
            
            


@login_required
@is_activo
def create_request(request):
    if request.method == "POST":

        cat_list = request.POST.getlist('cat_value')
        q_list = request.POST.getlist('cat_q')

        if(len(cat_list)!=len(q_list)):
            messages.error(request,"Solicitud incorrecta")
            return redirect("Inventory:create_request")

        if(any(int(q)<=0 for q in q_list) or 
           not all(Category.objects.filter(name=cat).exists() for cat in cat_list)):
           messages.error(request,"Solicitud incorrecta")
           return redirect("Inventory:create_request")

        request_obj = Request.objects.create(user1=request.user,specs=request.POST['comments'])
        print(request_obj)
        for i in range(0,len(cat_list)):
            quantity = int(q_list[i])
            category = Category.objects.get(name=cat_list[i])
            request_cat = RequestCategory.objects.create(
                                                        request=request_obj,
                                                        category=category,
                                                        quantity=quantity
                                                        )
            request_cat.save()
        
        messages.success(request,"Solicitud enviada")
        return redirect("Inventory:create_request")

    else:
        categories = Category.objects.all()
        return render(request, "Inventory/create_request.html", {'categories':categories})

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
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_bool=value).values()]
                elif att_type == 'DAT':
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_date=value).values()]
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
def loan_creation(request,eq_id):
    if request.method == "POST":
        lc_form = LoanCreationForm(request.POST)
        if lc_form.is_valid():
            loan= lc_form.save(commit=False)
            equipment = Equipment.objects.get(pk=eq_id)
            loan.equipment = equipment
            loan.creator = request.user
            loan.save()
            messages.success(request, "Prestamo cargado")
        else:
            messages.error(request, "Fallo al cargar prestamo")
        return redirect("Inventory:home_inventory")
    else:
        if not Equipment.objects.filter(pk=eq_id).exists():
            messages.error(request, "Fallo al cargar prestamo: No existe tal equipo.")
            return redirect("Inventory:home_inventory")
        name = Equipment.objects.get(pk=eq_id).name
        lc_form = LoanCreationForm()
        return render(request, "Inventory/create_loan.html", {"form" : lc_form, 'eq':name})

@login_required
@is_cuarto_equipo
def loan_devolution(request,loan):
    if request.method == "POST":
        if not Loan.objects.filter(pk=loan).exists():
            messages.error(request, "Préstamo no existente")
            return redirect("Inventory:home_inventory")
        instance = Loan.objects.get(pk=loan)
        form = LoanDevolutionForm(request.POST)
        if form.is_valid():
            instance.delivery_date=form.cleaned_data.get("delivery_date")
            instance.score=form.cleaned_data.get("score")
            instance.notes=form.cleaned_data.get("notes")
            instance.save()
            messages.success(request, "Devolución cargada")
        else:
            messages.error(request, "Fallo al cargar devolución")
        return redirect("Inventory:home_inventory")
    else: 
        form = LoanDevolutionForm()
        return render(request, "Inventory/loan_devolution.html", {"form" : form})

@login_required
@is_pasivo
def show_request(request,request_id):
    if request.method == "GET":
       
        if not Request.objects.filter(id=request_id).exists(): 
            messages.error(request, "No existe esta solicitud")
            return redirect("Inventory:cuarto_equipo") 

        req = Request.objects.get(id=request_id)
        if ((request.user.groups.first().name!='cuarto_equipo' and
             request.user.groups.first().name!='admin') and 
             request.user.id != req.user1.id):
            messages.error(request, "Permiso denegado")
            return redirect("Inventory:cuarto_equipo") 

        req_cat = RequestCategory.objects.filter(request=request_id)
        context = {'req':req,'requestCat':req_cat}
        return render(request,"Inventory/show_request.html",context)

    else:

        if not Request.objects.filter(id=request_id).exists(): 
            messages.error(request, "No existe esta solicitud")
            return redirect("Inventory:cuarto_equipo") 
        req = Request.objects.get(id=request_id)

        if (request.user.groups.first().name!='cuarto_equipo' and
            request.user.groups.first().name!='admin'):
            messages.error(request, "Permiso denegado")
            return redirect("Inventory:cuarto_equipo") 

        req.user2 = request.user
        req.status = request.POST['value']
        req.comments = request.POST['comments']
        print(request.POST)
        print(req.comments)
        req.save()
        messages.success(request,"Solicitud procesada con éxito.")
        return redirect("Inventory:cuarto_equipo")


@login_required
@is_pasivo
def show_equipment(request,category):

    atts = Attribute.objects.filter(category=category)
    equip = Equipment.objects.filter(category=category)
    catname = Category.objects.get(id=category).name
    borrowedEq = [ x['equipment'] for x in Loan.borrowedEq() ]
    discontinuedEq = [ x['id'] for x in Equipment.discontinuedEq() ]
    loans = Loan.objects.filter(delivery_date__isnull=True)
    rows = []
    for eq in equip:

        user = None

        available = 'Disponible'
        if eq.id in borrowedEq:
            available = 'Prestado'
            user = loans.get(equipment=eq).user
        elif(eq.id in discontinuedEq):
            available = 'Descontinuado'
        
        vals = [(eq.serial,''),(eq.name,'')]
        name = eq.name
        for att in atts:
            att_type=att.attribute_type
            unit = att.unit
            val=AttributeEquipmet.objects.get(attribute=att,equipment=eq)
            if att_type == 'INT':
                vals.append((val.value_int,unit))
            elif att_type == 'STR':
                vals.append((val.value_str,unit))
            elif att_type == 'TXT':
                vals.append((val.value_txt,unit))
            elif att_type == 'BOO':
                vals.append((val.value_bool,unit))
            elif att_type == 'DAT':
                vals.append((val.value_date,unit))
            elif att_type == 'FLT':
                vals.append((val.value_float,unit))
            elif att_type == 'CHO':
                vals.append((val.value_cho,unit))

        date = eq.elaboration_date

        info = [  
            {'name':'Fecha de llegada a Oikos', 'value':eq.entry_date},
            {'name':'Fecha de descontinuación', 'value':eq.discontinued_date}, 
            {'name':'Notas sobre el equipo', 'value':eq.notes}
            ]

        groups = [group for group in eq.group.all()]

        rows.append({
            'name':name, 
            'vals':vals, 
            'av':available, 
            'info':info, 
            'groups':groups, 
            'user':user,
            'date':date,
            'pic':eq.pic
            })

    return render(request, "Inventory/equipment_table.html", {'attributes': atts, 
                                                              'rows' : rows,
                                                              'name' : catname                                                
                                                              })

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


@login_required
@is_cuarto_equipo
def devolution_deadline_global(request):
    if request.method == "POST":

        date = request.POST['date']
        activeloans = Loan.objects.filter(delivery_date__isnull=True).exclude(deadline__isnull = False, deadline__lte=date)

        for loan in activeloans:
            loan.deadline = date
            loan.save()

        messages.success(request, "Fecha de entrega cargada")
    return redirect("Inventory:cuarto_equipo")

@login_required
@is_cuarto_equipo
def devolution_deadline_single(request,loan):
    if request.method == "POST":
        date = request.POST['date']
        loan = Loan.objects.get(pk=loan)
        loan.deadline = date
        loan.save()
        messages.success(request, "Fecha de entrega cargada")
    return redirect("Inventory:cuarto_equipo")

@login_required
@is_tesorero
def load_all_trim(request):
    if request.method == "POST":
        activos = User.objects.filter(status="AC")
        tcost = Quarterly.objects.get_or_create(pk=1)[0].amount
        for act in activos:
            t = Transaction(user=act, transaction=-tcost, reason='T')
            t.save()
        messages.success(request, "Trimestralidades cargadas")
    return redirect("Inventory:tesorero")

@login_required
@is_tesorero
def setQuarterly(request):
    if request.method == "POST":
        price = request.POST['price']
        q = Quarterly.objects.get_or_create(pk=1)[0]
        q.amount = price
        q.save()
        messages.success(request, "Trimestralidad Actualizada")
    return redirect("Inventory:tesorero")

@login_required
@is_cuarto_equipo
def discontinue_eq(request, eq):
    if request.method == "POST":
        equipment = Equipment.objects.get(id=eq)
        equipment.discontinued = True
        equipment.discontinued_date = datetime.date.today()
        equipment.save()
        messages.success(request, "Solicitud procesada con éxito")
    return redirect("Inventory:cuarto_equipo")
        