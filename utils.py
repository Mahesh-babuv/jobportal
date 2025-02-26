import random
import string
from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp):
    subject = "Your OTP Code"
    message = f"Your OTP code is {otp}. It is valid for 5 minutes."
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])


def generate_otp(length=6):
    otp = ''.join(random.choices(string.digits, k=length))
    return otp
