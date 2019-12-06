from django import template
from django.db.models import Q
from Users.models import User

STATUS_DICT = dict(User.STATUS_CHOICES)

register = template.Library()

@register.filter
def is_admin(user):
	return user.groups.filter(name='admin').exists()

@register.filter
def is_gestor_usuario(user):
	return user.groups.filter(Q(name='admin') | Q(name='gestor_usuarios')).exists()

@register.filter
def is_tesorero(user):
	return user.groups.filter(Q(name='admin') | Q(name='tesorero')).exists()

@register.filter
def is_cuarto_equipo(user):
	return user.groups.filter(Q(name='admin') | Q(name='cuarto_equipo')).exists()

@register.filter
def is_activo(user):
	return user.groups.filter(
            Q(name='admin') |
            Q(name='cuarto_equipo') |
            Q(name='gestor_usuarios') |
            Q(name='tesorero') |
            Q(name='activo')
        ).exists()

@register.filter
def is_pasivo(user):
	return user.groups.filter(
            Q(name='admin') |
            Q(name='cuarto_equipo') |
            Q(name='gestor_usuarios') |
            Q(name='tesorero') |
            Q(name='activo') |
            Q(name='pasivo')
        ).exists()

@register.filter
def get_status(status):
	return STATUS_DICT.get(status)

@register.filter
def clean(grupo):
    if grupo == "admin":
        return 'Administrador'
    elif grupo == 'cuarto_equipo':
        return 'Cuarto de Equipo'
    elif grupo == 'tesorero':
        return 'Tesorero'
    elif grupo == 'gestor_usuarios':
        return 'Gestor de Usuarios'
    elif grupo == 'activo':
        return 'Miembro Activo'
    return 'Inactivo'

@register.filter
def getReason(c):
    if c == 'P':
        return 'Pago'
    elif c == 'M':
        return 'Multa'
    return 'Trimestralidad'