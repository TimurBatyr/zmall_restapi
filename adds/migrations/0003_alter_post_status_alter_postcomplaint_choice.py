<<<<<<< HEAD
# Generated by Django 4.0.7 on 2022-09-20 14:02
=======
# Generated by Django 4.0.7 on 2022-09-20 14:20
>>>>>>> feature_adds

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adds', '0002_subscription_text_alter_subscription_choice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('in_progress', 'in_progress'), ('verified', 'verified'), ('rejected', 'rejected')], default='in_progress', max_length=100),
        ),
        migrations.AlterField(
            model_name='postcomplaint',
            name='choice',
            field=models.CharField(blank=True, choices=[('wrong', 'Неверная рубрика'), ('forbidden', 'Запрещенный товар'), ('not_relevant', 'Объявление не актуально'), ('wrong_address', 'Неверный адрес'), ('other', 'Другое'), ('', '')], default='', max_length=100, null=True),
        ),
    ]
