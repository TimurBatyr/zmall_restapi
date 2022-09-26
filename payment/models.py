from django.db import models



from account.models import  User


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_payment', null=True)
    amount = models.IntegerField(default=0)
    description = models.TextField(max_length=500)
    salt = models.CharField(max_length=100)
    # card_number = CardNumberField(verbose_name='card number')
    # card_expiry = CardExpiryField(verbose_name='expiration date')
    # card_code = SecurityCodeField(verbose_name='security code')

    class Meta:
        verbose_name = 'прием платежа'
        verbose_name_plural = 'прием платежей'
