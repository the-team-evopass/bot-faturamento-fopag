import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(assunto, para, html):            

    username = "apikey"
    password = "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"

    msg = MIMEMultipart('alternative')
    msg.attach(MIMEText(html, 'html'))

    msg['Subject'] = assunto
    msg['From'] = "cobranca@evopass.app.br"
    msg['To'] = para

    with smtplib.SMTP('smtp.sendgrid.net', 587) as smtp:
        smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(msg)