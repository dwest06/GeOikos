./loadlocaldb.sh
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py create_groups
echo "\
from Users.models import User;\
from django.contrib.auth.models import Group;\
u = User.objects.create_superuser(username='admin',email='admin@admin.com',password='da123456');\
u.groups.add(Group.objects.get(name='admin'))\
" | python manage.py shell
