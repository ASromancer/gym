# Generated by Django 4.1.2 on 2022-12-16 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0045_fitness_exercises_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fitness_type',
            name='id',
        ),
        migrations.AlterField(
            model_name='fitness_type',
            name='type_name',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
