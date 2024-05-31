import smtplib
from smtplib import SMTP 
from email.message import EmailMessage
def cmail(to,subject,body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('anushamallela568@gmail.com','yame fsec kzmg hcvu')
    msg=EmailMessage()
    msg['FROM']='anushamallela568@gmail.com'
    msg['SUBJECT']=subject
    msg['TO']=to
    msg.set_content(body)
    server.send_message(msg)
    server.quit()