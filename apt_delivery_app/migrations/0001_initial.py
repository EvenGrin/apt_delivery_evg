# Generated by Django 5.1.1 on 2025-03-09 16:39

import apt_delivery_app.models.m_order
import apt_delivery_app.models.validators
import datetime
import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(max_length=10, verbose_name='Номер')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Кабинет',
                'verbose_name_plural': 'Кабинеты',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('code', models.CharField(max_length=30, null=True)),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(error_messages={'unique': 'Пользователь с таким именем уже существует'}, help_text='Обязательное поле. Только латиница, цифры и тире.', max_length=150, unique=True, validators=[apt_delivery_app.models.validators.LoginValidator()], verbose_name='Логин')),
                ('first_name', models.CharField(max_length=150, validators=[apt_delivery_app.models.validators.NameValidator()], verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, validators=[apt_delivery_app.models.validators.NameValidator()], verbose_name='last name')),
                ('patronymic', models.CharField(blank=True, max_length=150, validators=[apt_delivery_app.models.validators.NameValidator()], verbose_name='Отчество')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('price', models.IntegerField(verbose_name='Цена (руб.)')),
                ('out', models.CharField(max_length=10, verbose_name='Выход')),
                ('image', models.ImageField(upload_to='images', verbose_name='Изображение')),
                ('quantity', models.IntegerField(default=3, verbose_name='Количество')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apt_delivery_app.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=None, verbose_name='Количество')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('meal', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='apt_delivery_app.meal', verbose_name='Блюдо')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date(2025, 3, 10), verbose_name='Дата')),
                ('meal', models.ManyToManyField(to='apt_delivery_app.meal', verbose_name='Блюдо')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')),
                ('order_date', models.TimeField(default=apt_delivery_app.models.m_order.get_default_created_at, verbose_name='Дата и время получения заказа')),
                ('result', models.CharField(blank=True, max_length=50, null=True, verbose_name='Причина отказа')),
                ('user_comment', models.TextField(blank=True, help_text='Не обязательное поле', null=True, verbose_name='Комментарий пользователя к заказу')),
                ('cab', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apt_delivery_app.cabinet', verbose_name='Кабинет')),
                ('deliver', models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'deliver'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courier_orders', to=settings.AUTH_USER_MODEL, verbose_name='Курьер')),
                ('user', models.ForeignKey(limit_choices_to=models.Q(('is_superuser', False), ('is_staff', False), ('groups__isnull', True)), on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apt_delivery_app.status', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Количество товаров')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apt_delivery_app.meal', verbose_name='Блюдо')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apt_delivery_app.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Заказ блюд',
                'verbose_name_plural': 'Заказы блюд',
            },
        ),
    ]
