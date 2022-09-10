from django.db import models
from django.db.models import Count
from phonenumber_field.modelfields import PhoneNumberField

from account.models import User


class Category(models.Model):
    """Category for post"""
    title = models.CharField(max_length=100, unique=True)
    icon_image = models.ImageField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='Subcategory', unique=True)

    def __str__(self):
        return self.title + '--' + self.category.title


    class Meta:
        ordering = ['-id']


class City(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


LIST = (
    ('VIP', 'VIP'),
    ('urgent', 'urgent'),
    ('ordinary', 'ordinary'),
    ('highlight', 'highlight'),
)


class Subscription(models.Model):
    choice = models.CharField(max_length=100, choices=LIST, default=('ordinary', 'ordinary'))
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id} {self.choice} -- {self.price}'


STATUS = (
        ('in_progress', 'in_progress'),
        ('verified', 'verified'),
        ('rejected', 'rejected')
    )

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, related_name='posts', on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name='posts', on_delete=models.PROTECT)
    subscription = models.ManyToManyField(Subscription, related_name='posts')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    from_price = models.DecimalField(max_digits=20, decimal_places=2)
    to_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', verbose_name='Фотография', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=100)
    phone_number = PhoneNumberField()
    wa_number = PhoneNumberField()
    is_activated = models.BooleanField()
    # views = models.IntegerField(default=0)
    status = models.CharField(max_length=100, choices=STATUS, default=('in_progress', 'in_progress'))



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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='phone')
    add_number = PhoneNumberField()

    def __str__(self):
        return f'Contact ID: {self.id}_ {str(self.add_number)} : {self.post.title} ID: {self.post.id}'


class Views(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField()
    post = models.ForeignKey(Post, related_name='Views_Post', on_delete=models.CASCADE)


class Favorite(models.Model):
    post = models.ManyToManyField(Post, related_name='Favorite_Post')
    user = models.ForeignKey(User, related_name='Favorite_User', on_delete=models.CASCADE)

    def __str__(self):
        return self.post


class Transactions(models.Model):
    pass


class Chat(models.Model):
    pass


class ReviewPost(models.Model):
    '''Comment to posts'''
    email = models.EmailField()
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Parent', on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='children')
    post = models.ForeignKey(Post, verbose_name='post', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'{self.title} - {self.post}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
