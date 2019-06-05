#!/usr/bin/env python

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(subject, message_text, html_elements, email):
    """
    sends an Email with the given subject, message_text and an html_elements version of the text
    """
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "message.alert.system@gmail.com"  # Users address
    receiver_email = email  # receivers address
    password = "OneTwoThree"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = message_text
    # Use the html_element to populate the html file
    html = """\
    <html>
      <body>
        <p>this message was send automatically from the Twitter message alert system. <br>
            the following information was retrieved: <br>
        </p>
        {variable}
      </body>
    </html>
    """.format(variable=html_elements)
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


    send_mail("message-alert-system","testing the message system... ","<p>testing the message system... </p>","mauri_31.12@hotmail.com")


__author__ = 'Cesar Mauricio Acuna Herrera'
