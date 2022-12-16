# Generated by Django 4.1.2 on 2022-12-10 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0029_delete_trainerachivement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enquiry',
            name='detail',
        ),
        migrations.RemoveField(
            model_name='enquiry',
            name='email',
        ),
        migrations.RemoveField(
            model_name='enquiry',
            name='full_name',
        ),
        migrations.AddField(
            model_name='enquiry',
            name='height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enquiry',
            name='today_calories',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enquiry',
            name='today_training_activity',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='enquiry',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enquiry',
            name='weight',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
