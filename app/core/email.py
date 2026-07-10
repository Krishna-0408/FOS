import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings


def send_welcome_email(user_name: str, user_email: str):

    message = MIMEMultipart()

    message["From"] = settings.SMTP_EMAIL
    message["To"] = user_email
    message["Subject"] = "Welcome to Food Ordering App"

    body = f"""
Hello {user_name},

Welcome to Food Ordering Application.

Your account has been created successfully.

Happy Ordering!

Regards,
Food Ordering Team
"""

    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(
        settings.SMTP_SERVER,
        settings.SMTP_PORT
    )

    server.starttls()

    server.login(
        settings.SMTP_EMAIL,
        settings.SMTP_PASSWORD
    )

    server.sendmail(
        settings.SMTP_EMAIL,
        user_email,
        message.as_string()
    )

    server.quit()


def send_otp_email(user_name: str, user_email: str, otp: str):

    message = MIMEMultipart()

    message["From"] = settings.SMTP_EMAIL
    message["To"] = user_email
    message["Subject"] = "Password Reset OTP"

    body = f"""
Hello {user_name},

Your OTP for resetting your password is

{otp}

This OTP is valid for 10 minutes.

If you didn't request this, please ignore this email.

Regards,
Food Ordering Team
"""

    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(
        settings.SMTP_SERVER,
        settings.SMTP_PORT
    )

    server.starttls()

    server.login(
        settings.SMTP_EMAIL,
        settings.SMTP_PASSWORD
    )

    server.sendmail(
        settings.SMTP_EMAIL,
        user_email,
        message.as_string()
    )

    server.quit()