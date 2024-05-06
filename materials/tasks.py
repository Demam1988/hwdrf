import smtplib

from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_mail_for_update(lesson, email):
    try:
        result = send_mail(
            subject="Обновление по курсу!",
            message=f"Курс {lesson} был обновлён!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email,
            fail_silently=False,
        )

        if result:
            print("OK")

    except smtplib.SMTPException as e:
        print(str(e))
