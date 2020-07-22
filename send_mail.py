import smtplib
import config


def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(config.EMAIL_ADDRESS,
                        config.DESTINATION_EMAIL_ADDRESS, message, )
        server.quit()
        print("Email sent successfully!")
    except:
        print("Email failed to send.")
