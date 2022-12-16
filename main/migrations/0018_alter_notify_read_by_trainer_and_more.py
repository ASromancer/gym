# Generated by Django 4.1.2 on 2022-11-21 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0017_remove_notify_read_by_remove_notify_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notify',
            name='read_by_trainer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.trainer'),
        ),
        migrations.AlterField(
            model_name='notify',
            name='read_by_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]