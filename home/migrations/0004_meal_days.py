# Generated by Django 3.2.25 on 2024-12-11 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_dayofweek_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='days',
            field=models.ManyToManyField(blank=True, to='home.DayOfWeek'),
        ),
    ]
