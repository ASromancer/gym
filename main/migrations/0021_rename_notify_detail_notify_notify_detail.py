# Generated by Django 4.1.2 on 2022-11-24 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_rename_notifiuserstatus_notifuserstatus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notify',
            old_name='Notify_detail',
            new_name='notify_detail',
        ),
    ]
