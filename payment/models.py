from django.db import models

from account.models import  User


class StoreTarsaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_store', null=True)
    title = models.CharField(max_length=100)
    type_adverments = models.CharField(max_length=100)
    date = models.DateTimeField(null=True)
    price = models.DecimalField(max_digits=20,decimal_places=0)