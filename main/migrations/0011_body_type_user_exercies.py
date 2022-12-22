# Generated by Django 4.1.2 on 2022-12-20 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_user_exercies_body_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Body_type',
            fields=[
                ('body_type', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Body types',
            },
        ),
        migrations.CreateModel(
            name='User_exercies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('times', models.IntegerField(blank=True, null=True)),
                ('body_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.body_type')),
                ('fitness_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.fitness_type')),
            ],
            options={
                'verbose_name_plural': 'User Exercies',
            },
        ),
    ]