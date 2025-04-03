from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

from django.conf import settings


# @shared_task
def send_otp(first_name,email,otp):

    subject = 'Verify Your Otp'
    context = {
        'first_name': first_name,
        'otp_code': otp,
    }
    html_message = render_to_string('otp_verification.html', context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [email], html_message=html_message)


# @shared_task
def send_success_email(first_name,email):

    subject = 'Account is Active'
    context = {
        'first_name': first_name,
    }
    html_message = render_to_string('otp_success.html', context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [email], html_message=html_message)


def send_reset_password_success(first_name,email):

    subject = 'Reset Password Successful'
    context = {
        'first_name': first_name,
    }
    html_message = render_to_string('forgot_password.html', context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [email], html_message=html_message)
