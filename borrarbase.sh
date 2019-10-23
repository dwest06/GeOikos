./loadlocaldb.sh
python3 manage.py makemigrations
python3 manage.py migrate
echo "from Users.models import User; User.objects.create_superuser(username='admin',email='admin@admin.com',password='da123456')" | python manage.py shell
