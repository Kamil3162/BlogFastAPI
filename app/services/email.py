import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiosmtplib import SMTP  # Import send for direct sending or SMTP for more control
from dotenv import load_dotenv

import ssl
load_dotenv()


class EmailService:
    @staticmethod
    def send_reset_email(email_to: str, reset_link: str):
        EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
        EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

        # Prepare the email message
        message = MIMEMultipart()
        message["From"] = EMAIL_ADDRESS
        message["To"] = email_to
        message["Subject"] = "Password Reset Request"

        body = f"""Hi,
                Click on the link below to reset your password:
                {reset_link}
            """
        message.attach(MIMEText(body, "plain"))

        # Send the email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465,
                              context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, email_to, message.as_string())