# Generated by Django 4.1.2 on 2022-12-22 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_body_type_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='body_type',
            name='fat',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
