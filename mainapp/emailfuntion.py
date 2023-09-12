from django.core.mail import send_mail

from django.conf import settings
def send_forget_password_email(email,token):
    
    subject="Your forget password link "
    message=f"Hi you requested for a password reset click this link or paste it in the browser http://127.0.0.1:8000/resetpassword/{token}/"
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    return True

