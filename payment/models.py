from django.db import models



from account.models import  User
from adds.models import Post


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_payment', null=True)
    amount = models.IntegerField(default=0)
    description = models.TextField(max_length=500)
    salt = models.CharField(max_length=100)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='post_payment',null=True)


    class Meta:
        verbose_name = 'прием платежа'
        verbose_name_plural = 'прием платежей'

class StoreTarsaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_store', null=True)
    title = models.CharField(max_length=100)
    type_adverments = models.CharField(max_length=100)
    date = models.DateTimeField(null=True)
    price = models.DecimalField(max_digits=20,decimal_places=0)
