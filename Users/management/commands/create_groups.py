from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from Users.models import User

GROUPS = ['admin', 'gestor_usuarios', 'tesorero', 'cuarto_equipo' , 'activo', 'pasivo']
PERMISSIONS = ['consultar deuda personal', ]

class Command(BaseCommand):
    help = 'Create groups and permission for Geoikos users'

    def handle(self, *args, **options):
        try:
            # Imprimir los grupos disponibles
            print('Creando Grupos: ', end="")
            for i in GROUPS:
                print(i, end=", ")
            print()

            # Creamos los grupos
            for i in GROUPS:
                newgroup, c = Group.objects.get_or_create(name=i)
            print("Grupos creados.")

        except:
            raise CommandError("ERROR")