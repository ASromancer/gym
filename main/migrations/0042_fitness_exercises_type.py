# Generated by Django 4.1.2 on 2022-12-16 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_fitness_exercises'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitness_exercises',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.fitness_type'),
        ),
    ]
