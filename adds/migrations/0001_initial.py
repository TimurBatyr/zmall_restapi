# Generated by Django 4.0.7 on 2022-09-26 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('icon_image', models.ImageField(upload_to='')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=900, null=True)),
                ('from_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('to_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/%Y/%m/%d', verbose_name='Фотография')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(default='No email', max_length=100)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(default='No number', max_length=128, region=None)),
                ('wa_number', phonenumber_field.modelfields.PhoneNumberField(default='No number', max_length=128, region=None)),
                ('is_activated', models.BooleanField(default=True)),
                ('views', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('в рассмотрени', 'в рассмотрении'), ('одобрено', 'одобрено'), ('отклонено', 'отклонено')], default='in_progress', max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='adds.category')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='adds.city')),
            ],
        ),
        migrations.CreateModel(
            name='PostContacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=13)),
                ('view', models.IntegerField(blank=True, default=0, null=True)),
                ('post_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_phone', to='adds.post')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(choices=[('VIP', 'VIP'), ('Добавить стикер "Срочно"', 'Добавить стикер "Срочно"'), ('Выделить цветом', 'Выделить цветом'), ('', '')], default='', max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('text', models.CharField(max_length=100)),
                ('icon_image', models.ImageField(upload_to='')),
                ('outer_image', models.ImageField(upload_to='')),
                ('period', models.CharField(choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('', '')], default='', max_length=100)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Views',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('views', models.IntegerField(blank=True, default=0, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views_post', to='adds.post')),
            ],
        ),
        migrations.CreateModel(
            name='ViewsContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('views', models.IntegerField(blank=True, default=0, null=True)),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to='adds.postcontacts')),
                ('view_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='view_contact', to='adds.views')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='subcategory')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='adds.category')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ReviewPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('text', models.TextField(max_length=5000)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='adds.reviewpost', verbose_name='Parent')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='adds.post', verbose_name='post')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='PostImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images', verbose_name='Фотографии')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='adds.post')),
            ],
        ),
        migrations.CreateModel(
            name='PostComplaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason_message', models.CharField(blank=True, max_length=100, null=True)),
                ('choice', models.CharField(blank=True, choices=[('Неверная рубрика', 'Неверная рубрика'), ('Запрещенный товар', 'Запрещенный товар'), ('Объявление не актуально', 'Объявление не актуально'), ('Неверный адрес', 'Неверный адрес'), ('Другое', 'Другое'), ('', '')], default='', max_length=100, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_complain', to='adds.post')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='post',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='adds.subcategory'),
        ),
        migrations.AddField(
            model_name='post',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='adds.subscription'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorites', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='adds.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
