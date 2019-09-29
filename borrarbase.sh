./loadlocaldb.sh
python3 manage.py makemigrations
python3 manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.com', 'da123456')" | python manage.py shell
