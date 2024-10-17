import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

import ssl
load_dotenv()


class EmailService:
    @staticmethod
    def send_reset_email(email_to: str, reset_link: str):
        email_address = os.environ.get("EMAIL_ADDRESS")
        email_password = os.environ.get("EMAIL_PASSWORD")

        # Prepare the email message
        message = MIMEMultipart()
        message["From"] = email_address
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
            server.login(email_address, email_password)
            server.sendmail(email_address, email_to, message.as_string())