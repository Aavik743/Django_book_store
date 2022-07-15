from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse


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
        Mail.send_email(subject, message, sender, recipient)

    @staticmethod
    def order_notification(data):
        subject = 'Order Placed'
        message = f'Hi {data["username"]}, Your order has been placed for book {data["book"]} ' \
                  f'and the total price is {data["total_price"]}'
        sender = 'fake.abhik@gmail.com'
        recipient = f'{data["email"]}'
        Mail.send_email(subject, message, sender, recipient)


def to_send_email(subject, message, sender, recipient):
    send_mail(subject, message, sender,
              [recipient], fail_silently=False)
