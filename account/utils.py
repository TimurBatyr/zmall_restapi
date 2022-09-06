from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from account.models import UserProfile
from config.celery import app


def generate_activation_code():
    code = get_random_string(8)
    return code


def get_activation_code():
    code = generate_activation_code()
    if UserProfile.objects.filter(activation_code=code).exists():
        get_activation_code()
    return code


def send_activation_mail(activation_code, email):
    message = f'Hello! Thank you for registering on our site! Your activation code: {activation_code}'
    send_mail(
        'Account verification',
        message,
        "test@gmail.com",
        [email]
    )

def send_new_password(new_password, email):
    message = f'Your new password: {new_password}'
    send_mail(
        'Reset password',
        message,
        'test@gmail.com',
        [email]
    )


@app.task
def send_mail_new_post(new_products, email):
    message = f'New products has been added: {new_products}'
    send_mail(
        'New products',
        message,
        'test@gmail.com',
        [email]
    )
