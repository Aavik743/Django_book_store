from django.core.mail import send_mail


def to_send_email(subject, message, sender, recipient):
    send_mail(subject, message, sender,
              [recipient], fail_silently=False)
