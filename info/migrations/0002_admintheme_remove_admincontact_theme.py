# Generated by Django 4.0.7 on 2022-09-27 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='admincontact',
            name='theme',
        ),
    ]
