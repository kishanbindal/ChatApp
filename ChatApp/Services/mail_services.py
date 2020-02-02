from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
import logging

logging.basicConfig(level=logging.DEBUG)


class MailServices:

    @staticmethod
    def send_registration_email(request, user, to_email, token):

        subject = f"Activate Your Account on {get_current_site(request)}"
        message = render_to_string('activate.html', {
            "user": user,
            "domain": get_current_site(request).domain,
            "token": token
        })
        send_mail(subject, message, 'djangomailer4@gmail.com', [to_email], fail_silently=True)
        logging.info(f"Message Sent Successfully to {to_email}")

    @staticmethod
    def send_forgot_password_email(request, to_email, short_url):

        subject = f'Reset Password - from {get_current_site(request)}'
        message = render_to_string('reset.html', {
            "domain": get_current_site(request).domain,
            "token": short_url
        })
        send_mail(subject, message, 'djangomailer4@gmail.com', [to_email], fail_silently=True)
        logging.info(f'Message sent Successfully to {to_email}')
