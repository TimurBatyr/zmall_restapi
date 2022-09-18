# Generated by Django 4.0.7 on 2022-09-18 07:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adds', '0003_remove_subscription_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='post',
        ),
        migrations.AddField(
            model_name='favorite',
            name='post',
            field=models.ManyToManyField(related_name='post', to='adds.post'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
