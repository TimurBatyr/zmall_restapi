# Generated by Django 4.1 on 2022-09-05 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='from_price',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='to_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
