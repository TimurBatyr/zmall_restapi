from django.core.mail import send_mail

from account.models import UserProfile
from config import settings
from config.celery import app


@app.task
def send_mail_new_post(new_product):
    # emails = UserProfile.objects.filter(is_active=True).values_list('email', flat=True)
    for user in UserProfile.objects.filter(is_active=True):
        mail_subject = 'New Products'
        message = f"""We have announced a new product.
                      Please click the link: http://127.0.0.1:8000/api/v1/adds/detailpost/{new_product}"""
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True,
        )