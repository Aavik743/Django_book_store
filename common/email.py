from django.core.mail import send_mail
from celery.utils.log import get_task_logger
from celery import shared_task

logger = get_task_logger(__name__)


class Mail:
    @staticmethod
    def send_email(subject, message, sender, recipient):
        send_mail(subject, message, sender,
                  [recipient], fail_silently=False)

    @staticmethod
    def register_user(data):
        subject = 'Activation Link'
        message = f'Hi {data["username"]}, ' \
                  f'' \
                  f'Click on the link to activate your account ' \
                  f'' \
                  f'{data["url"]}'
        sender = 'fake.abhik@gmail.com'
        recipient = f'{data["email"]}'
        send_mail_task.delay(subject, message, sender, recipient)

    @staticmethod
    def order_notification(data):
        subject = 'Order Placed'
        message = f'Hi {data["username"]}, Your order has been placed for book {data["book"]} ' \
                  f'and the total price is {data["total_price"]}'
        sender = 'fake.abhik@gmail.com'
        recipient = f'{data["email"]}'
        send_mail_task.delay(subject, message, sender, recipient)

    @staticmethod
    def forgot_password(data, url):
        subject = 'Forgot Password Link'
        message = f'Hi {data.username}, ' \
                  f'Click on the link to reset your password ' \
                  f'{url}'
        sender = 'fake.abhik@gmail.com'
        recipient = f'{data.email}'
        send_mail_task.delay(subject, message, sender, recipient)


@shared_task(name='send_mail')
def send_mail_task(subject, message, sender, recipient):
    logger.info('send mail using celery')
    return Mail.send_email(subject, message, sender, recipient)
