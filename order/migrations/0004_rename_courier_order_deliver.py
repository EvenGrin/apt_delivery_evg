# Generated by Django 3.2.25 on 2024-12-28 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_result'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='courier',
            new_name='deliver',
        ),
    ]