# Generated by Django 4.1.2 on 2022-12-19 06:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_enquiry_date_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='date_modified',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]