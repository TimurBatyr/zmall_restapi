# Generated by Django 4.0.7 on 2022-11-09 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adds', '0002_alter_postcomplaint_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon_image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
