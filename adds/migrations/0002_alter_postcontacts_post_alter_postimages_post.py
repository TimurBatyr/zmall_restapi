# Generated by Django 4.1 on 2022-09-01 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcontacts',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone', to='adds.post'),
        ),
        migrations.AlterField(
            model_name='postimages',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='adds.post'),
        ),
    ]
