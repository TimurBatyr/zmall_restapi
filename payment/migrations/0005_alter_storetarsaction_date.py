# Generated by Django 4.0.7 on 2022-09-27 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_storetarsaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storetarsaction',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
