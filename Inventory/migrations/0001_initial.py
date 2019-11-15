# Generated by Django 2.2.5 on 2019-11-15 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('attribute_type', models.CharField(choices=[('INT', 'Entero'), ('TXT', 'Texto'), ('STR', 'String'), ('BOO', 'Booleano'), ('FLT', 'Decimal'), ('DAT', 'Fecha'), ('CHO', 'Selección')], max_length=3)),
                ('unit', models.CharField(blank=True, max_length=20, null=True)),
                ('nullity', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Attribute_Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_str', models.CharField(max_length=100, null=True)),
                ('value_txt', models.TextField(null=True)),
                ('value_int', models.IntegerField(null=True)),
                ('value_date', models.DateField(null=True)),
                ('value_bool', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('entry_date', models.DateField(blank=True, null=True)),
                ('elaboration_date', models.DateField(blank=True, null=True)),
                ('discontinued', models.BooleanField(default=False)),
                ('discontinued_date', models.DateField(null=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentDebt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('damage_date', models.DateField(null=True)),
                ('return_date', models.DateField(null=True)),
                ('specs', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hand_over_date', models.DateTimeField()),
                ('deadline', models.DateTimeField(null=True)),
                ('delivery_date', models.DateTimeField(null=True)),
                ('score', models.IntegerField(null=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repairer', models.CharField(max_length=100, null=True)),
                ('hand_over_date', models.DateField(null=True)),
                ('return_date', models.DateField(null=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('specs', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Request_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction', models.DecimalField(decimal_places=2, max_digits=7)),
                ('reason', models.CharField(choices=[('P', 'Pago'), ('M', 'Multa'), ('T', 'Trimestralidad')], max_length=1)),
            ],
        ),
    ]