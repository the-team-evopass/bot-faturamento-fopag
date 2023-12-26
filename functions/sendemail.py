import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(assunto, para, html):            
    # Configurações da conta SendGrid
    Username = "apikey"
    Password = "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"

    # Criar objeto EmailMessage
    msg = MIMEMultipart('alternative')
    # msg.attach(MIMEText("<div style='background-color: #f5f5f5;'>Teste</div>", 'html'))
    msg.attach(MIMEText(html, 'html'))

    # Configurar cabeçalhos
    msg['Subject'] = assunto
    msg['From'] = "cobranca@evopass.app.br"
    msg['To'] = para

    # Conectar e enviar e-mail usando SMTP_SSL
    with smtplib.SMTP_SSL('smtp.sendgrid.net', 465) as smtp:
        smtp.login(Username, Password)
        smtp.send_message(msg)

# send_email('Testando envio de html', 'felipe@evopass.app.br')
# send_email('Faturamento Evopass', 'felipe@evopass.app.br', render_html('Felipe SA', '12/2023', '20,89', 'https://www.evopass.app.br', '9238409'))
# send_email('Faturamento Evopass', 'felipemelo.unidade@gmail.com', myMail)