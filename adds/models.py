from django.db import models
from django.db.models import Count
from phonenumber_field.modelfields import PhoneNumberField

from account.models import User


class Category(models.Model):
    """Category for post"""
    title = models.CharField(max_length=100, unique=True)
    icon_image = models.ImageField()

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
    ('urgent', 'urgent'),
    ('highlight', 'highlight'),
)

PERIOD = (
    ('5 days', '5 days'),
    ('10 days', '10 days'),
    ('15 days', '15 days'),
    ('20 days', '20 days'),
    ('25 days', '25 days'),
    ('30 days', '30 days'),
)


class Subscription(models.Model):
    choice = models.CharField(max_length=100, choices=LIST)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    icon_image = models.ImageField()
    period = models.CharField(max_length=100, choices=PERIOD)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id} {self.choice} -- {self.price} soms -- {self.period}'


STATUS = (
        ('in_progress', 'in_progress'),
        ('verified', 'verified'),
        ('rejected', 'rejected')
    )

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, related_name='posts', on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name='posts', on_delete=models.PROTECT, blank=True, null=True)
    subscription = models.ForeignKey(Subscription, related_name='posts', on_delete=models.PROTECT, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True, null=True)
    from_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    to_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', verbose_name='Фотография', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=100, default='No email')
    phone_number = PhoneNumberField(default='No number')
    wa_number = PhoneNumberField(default='No number')
    is_activated = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
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

#views
class PhoneNumber(models.Model):
    phone_number= models.CharField(max_length=10,default=500000000)
    view = models.IntegerField(default=0)
    post_number = models.ForeignKey(Post, related_name='phone_post', on_delete=models.CASCADE)
    def __str__(self):
        return self.phone_number


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


class Views(models.Model):
    user = models.CharField(max_length=100,null=True,blank=True)
    date = models.DateField(blank=True,null=True)
    views = models.IntegerField(default=0,blank=True,null=True)
    post = models.ForeignKey(Post, related_name='Views_Post', on_delete=models.CASCADE)

class ViewsContact(models.Model):
    date = models.DateField(blank=True, null=True)
    views = models.IntegerField(default=0, blank=True, null=True)
    phone = models.ForeignKey(PhoneNumber, related_name='contact', on_delete=models.CASCADE)
    view_key = models.ForeignKey(Views, related_name='view_contact', on_delete=models.CASCADE)


class Favorite(models.Model):
    post = models.ManyToManyField(Post, related_name='post')
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} - {self.user}'


class Transactions(models.Model):
    pass
