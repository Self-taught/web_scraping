import smtplib, ssl
import os
from key import username, key, receiver


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    user_email = username
    password = key

    receiver_email = receiver
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(user_email, password)
        server.sendmail(user_email, receiver_email, message)
