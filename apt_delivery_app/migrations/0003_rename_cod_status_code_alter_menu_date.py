# Generated by Django 5.0.7 on 2025-03-07 08:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apt_delivery_app', '0002_alter_menu_date_alter_order_order_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='status',
            old_name='cod',
            new_name='code',
        ),
        migrations.AlterField(
            model_name='menu',
            name='date',
            field=models.DateField(default=datetime.date(2025, 3, 8), verbose_name='Дата'),
        ),
    ]
