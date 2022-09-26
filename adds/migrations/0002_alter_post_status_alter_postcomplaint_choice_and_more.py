# Generated by Django 4.0.7 on 2022-09-26 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('в рассмотрени', 'в рассмотрении'), ('одобрено', 'одобрено'), ('отклонено', 'отклонено')], default='in_progress', max_length=100),
        ),
        migrations.AlterField(
            model_name='postcomplaint',
            name='choice',
            field=models.CharField(blank=True, choices=[('Неверная рубрика', 'Неверная рубрика'), ('Запрещенный товар', 'Запрещенный товар'), ('Объявление не актуально', 'Объявление не актуально'), ('Неверный адрес', 'Неверный адрес'), ('Другое', 'Другое'), ('', '')], default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='postcontacts',
            name='post_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_phone', to='adds.post'),
        ),
        migrations.AlterField(
            model_name='postcontacts',
            name='view',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='choice',
            field=models.CharField(choices=[('VIP', 'VIP'), ('Добавить стикер "Срочно"', 'Добавить стикер "Срочно"'), ('Выделить цветом', 'Выделить цветом'), ('', '')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='period',
            field=models.CharField(choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('', '')], default='', max_length=100),
        ),
    ]
