# Generated by Django 4.0.7 on 2022-09-13 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adds', '0005_alter_subscription_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='choice',
            field=models.CharField(blank=True, choices=[('VIP', 'VIP'), ('urgent', 'urgent'), ('highlight', 'highlight')], max_length=100, null=True),
        ),
    ]