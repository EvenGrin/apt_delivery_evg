# Generated by Django 3.2.25 on 2024-12-14 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='home.category', verbose_name='Категория'),
        ),
        migrations.CreateModel(
            name='MenuDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_day', models.IntegerField(choices=[(0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'), (3, 'Четверг'), (4, 'Пятница'), (5, 'Суббота')], default=0)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.meal')),
            ],
            options={
                'verbose_name': 'Меню на день',
                'verbose_name_plural': 'Меню на день',
            },
        ),
    ]