# Generated by Django 3.2.25 on 2024-12-13 07:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_menu_meal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='date',
            field=models.DateTimeField(default=datetime.date.today, verbose_name='Дата'),
        ),
    ]
