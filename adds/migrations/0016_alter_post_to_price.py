# Generated by Django 4.1 on 2022-09-03 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adds', '0015_remove_subscription_highlight_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='to_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
