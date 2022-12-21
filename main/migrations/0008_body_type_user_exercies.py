# Generated by Django 4.1.2 on 2022-12-20 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_enquiry_date_modified'),
    ]

    operations = [
        migrations.CreateModel(
            name='body_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_type', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_exercies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('times', models.IntegerField(blank=True, null=True)),
                ('Fitness_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.fitness_type')),
                ('body_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.body_type')),
            ],
        ),
    ]
