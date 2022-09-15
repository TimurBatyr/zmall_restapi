from celery import shared_task
from django.core.mail import send_mail

from account.models import User
from adds.management.commands.catalog import run_pars_catalog
from adds.management.commands.doska import run_parser_doska
from adds.management.commands.selexy import run_pars_selexy
from adds.models import Post
from config import settings
from config.celery import app


@app.task
def send_mail_new_products():
    products = list(Post.objects.filter(is_activated=True).values_list('title', flat=True)[0:10])
    for user in User.objects.filter(is_active=True):
        mail_subject = 'New Products'
        message = f"We have announced new products. Please see list:{'-'.join(products)}"
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True,
        )

send_mail_new_products.delay()


@shared_task
def run_selexy():
    run_pars_selexy()


@shared_task
def run_catalog():
    run_pars_catalog()


@shared_task
def run_doska():
    run_parser_doska()



