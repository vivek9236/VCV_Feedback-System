from email.mime.text import MIMEText
import smtplib

def send_email(email, name, password,selection):
    from_email="sharevivek.com@gmail.com"
    from_password="9236553423"
    to_email=email

    subject="Account Access data"
    if selection == 0 :
        message="Hey there, <strong>%s</strong> your password is <strong>%s</strong>." % (name,password)
    if selection == 1 :
        message="Hey there, <strong>%s</strong> your valuable feedback has been successfully recorded." % (name,)
    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
