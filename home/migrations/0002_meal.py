# Generated by Django 3.2.25 on 2024-11-11 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('price', models.FloatField()),
                ('out', models.CharField(max_length=10)),
                ('image', models.ImageField(upload_to='images')),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.category')),
            ],
        ),
    ]