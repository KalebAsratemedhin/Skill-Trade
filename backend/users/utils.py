from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user):
    token = user.generate_email_token()
    verification_link = f"http://localhost:8000/api/auth/verify-email/{token}" 

    subject = "Verify Your Email"
    message = f"Click the link below to verify your email:\n\n{verification_link}"

    print("sending email", token, settings.DEFAULT_FROM_EMAIL, user.email, settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])