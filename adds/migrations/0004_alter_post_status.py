# Generated by Django 4.0.7 on 2022-09-20 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adds', '0003_alter_post_status_alter_postcomplaint_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('in_progress', 'в рассмотрении'), ('verified', 'одобрено'), ('rejected', 'отклонено')], default='in_progress', max_length=100),
        ),
    ]