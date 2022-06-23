import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv

from dotenv import load_dotenv

load_dotenv()


class EmailModel:
    email_from = getenv("EMAIL_FROM")
    password = getenv("PASS_EMAIL")

    def __init__(self, email_to_send: list, subject, message) -> None:
        self.email_to_send = email_to_send
        self.subject = subject
        self.message = message

    def send_email(self):
        email = MIMEMultipart()

        email["From"] = self.email_from
        email["Subject"] = self.subject

        email.attach(MIMEText(self.message, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(getenv("EMAIL_SMTP"), port=int(getenv("EMAIL_PORT")), context=context) as server:
            server.login(email["From"], self.password)
            server.sendmail(email["From"], self.email_to_send, email.as_string())
