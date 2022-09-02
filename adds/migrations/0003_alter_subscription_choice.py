# Generated by Django 4.1 on 2022-09-02 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adds', '0002_alter_subscription_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='choice',
            field=models.CharField(choices=[('VIP', 'VIP'), ('highlight', 'highlight'), ('urgent', 'urgent'), ('ordinary', 'ordinary')], default=('ordinary', 'ordinary'), max_length=100),
        ),
    ]
