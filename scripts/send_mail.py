import smtplib
import config
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders

EMAIL_ADDRESS = os.environ.get("EMAIL")
PASSWORD = os.environ.get("EMAIL_PASSWORD")

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(EMAIL_ADDRESS,
                        config.DESTINATION_EMAIL_ADDRESS, message, )
        server.quit()
        print("Email sent successfully!")
    except:
        print("Email failed to send.")


def send_mail_with_attachment(chapter_number):
    # cast to string
    chapter_number = str(chapter_number)
    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    password = PASSWORD
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = config.DESTINATION_EMAIL_ADDRESS
    msg['Subject'] = "Chapter "+chapter_number+" is out!"

    # create the zip MIME
    msgZip = MIMEBase('application', 'zip')
    fp = open('./chapters/'+chapter_number+'.zip', 'rb')
    msgZip.set_payload(fp.read())
    encoders.encode_base64(msgZip)
    msgZip.add_header('Content-Disposition', 'attachment',
                      filename=chapter_number+".zip")
    fp.close()

    # attach the zip file
    msg.attach(msgZip)

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
