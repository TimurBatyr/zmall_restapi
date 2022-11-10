from django.db import models
from django.db.models import Count
from phonenumber_field.modelfields import PhoneNumberField

from account.models import User


class Category(models.Model):
    """Category for post"""
    title = models.CharField(max_length=100, unique=True)
    icon_image = models.ImageField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='subcategory', unique=True)

    def __str__(self):
        return self.title + '--' + self.category.title


    class Meta:
        ordering = ['-id']


class City(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150)

    def __str__(self):
        return self.title


LIST = (
    ('VIP', 'VIP'),
    ('Добавить стикер "Срочно"', 'Добавить стикер "Срочно"'),
    ('Выделить цветом', 'Выделить цветом'),
    ('', ''),
)

PERIOD = (
    ('5', '5'),
    ('10', '10'),
    ('15', '15'),
    ('20', '20'),
    ('25', '25'),
    ('30', '30'),
    ('', ''),
)


class Subscription(models.Model):
    choice = models.CharField(max_length=100, choices=LIST, default='')
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    text = models.CharField(max_length=100)
    icon_image = models.ImageField()
    outer_image = models.ImageField()
    period = models.CharField(max_length=100, choices=PERIOD, default='')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id} {self.choice} -- {self.price} soms -- {self.period}'


STATUS = (
        ('в рассмотрени', 'в рассмотрении'),
        ('одобрено', 'одобрено'),
        ('отклонено', 'отклонено'),

    )

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, related_name='posts', on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name='posts', on_delete=models.PROTECT, blank=True, null=True)
    subscription = models.ForeignKey(Subscription, related_name='posts', on_delete=models.PROTECT, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=900, blank=True, null=True)
    from_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    to_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', verbose_name='Фотография', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=100, default='No email')
    phone_number = PhoneNumberField(default='No number')
    wa_number = PhoneNumberField(default='No number')
    is_activated = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=100, choices=STATUS, default='in_progress')

    def __str__(self):
        return f'ID {self.id} : {self.title}'


class PostImages(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images', blank=True, verbose_name='Фотографии')

    def __str__(self):
        return f'PostImage_ID {self.id} : {self.post.title} ID: {self.post.id}'

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        return super().delete(using, keep_parents)


class PostContacts(models.Model):
    post_number = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_phone')
    phone_number = models.CharField(max_length=13, blank=True)
    view = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f'Contact ID: {self.id}_ {str(self.phone_number)} : {self.post_number.title} ID: {self.post_number.id}'


#views
class Views(models.Model):
    user = models.CharField(max_length=100,null=True,blank=True)
    date = models.DateField(blank=True,null=True)
    views = models.IntegerField(default=0,blank=True,null=True)
    post = models.ForeignKey(Post, related_name='views_post', on_delete=models.CASCADE)


class ViewsContact(models.Model):
    date = models.DateField(blank=True, null=True)
    views = models.IntegerField(default=0, blank=True, null=True)
    phone = models.ForeignKey(PostContacts, related_name='contact', on_delete=models.CASCADE)
    view_key = models.ForeignKey(Views, related_name='view_contact', on_delete=models.CASCADE)


class ReviewPost(models.Model):
    '''Comment to posts'''
    email = models.EmailField()
    text = models.TextField(max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Parent', on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='children')
    post = models.ForeignKey(Post, verbose_name='post', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'{self.post}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Favorite(models.Model):
    favorites = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f'{self.id} - {self.user}'

COMPLAIN_LIST = (
    ('Неверная рубрика', 'Неверная рубрика'),
    ('Запрещенный товар', 'Запрещенный товар/услуги'),
    ('Объявление не актуально', 'Объявление не актуально'),
    ('Неверный адрес', 'Неверный адрес'),
    ('Другое', 'Другое'),
    ('', ''),
)


class PostComplaint(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_complain")
    reason_message = models.CharField(max_length=100, blank=True, null=True)
    choice = models.CharField(max_length=100, choices=COMPLAIN_LIST, default=(''), null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id} {self.post} -- {self.choice}'



class Transactions(models.Model):
    pass
