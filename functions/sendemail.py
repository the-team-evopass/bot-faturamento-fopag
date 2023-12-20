import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configurações do servidor SMTP e credenciais
smtplib_server = 'smtp.live.com'
smtplib_port = 587 
smtplib_username = 'gabriel.lima@academiaevoque.com.br'
smtplib_password = 'Ja921600'

# Destinatário e informações do e-mail
destinatario = 'limaruasgabriel@gmail.com'
assunto = 'Assunto do email'

# Criar o objeto MIMEMultipart para o e-mail
mensagem = MIMEMultipart()
mensagem['From'] = smtplib_username
mensagem['To'] = destinatario
mensagem['Subject'] = assunto

# Adicionar o corpo do e-mail (pode adicionar HTML se desejar)
corpo_email = 'Corpo do seu e-mail aqui.'
mensagem.attach(MIMEText(corpo_email, 'plain'))

try:
    # Configurar a conexão SMTP sem STARTTLS
    with smtplib.SMTP(smtplib_server, smtplib_port) as server:
        # Login no servidor
        server.login(smtplib_username, smtplib_password)

        # Enviar o e-mail
        server.sendmail(smtplib_username, destinatario, mensagem.as_string())
        print(f'E-mail enviado com sucesso para {destinatario}: {assunto}')

except Exception as e:
    print(f'Erro ao enviar e-mail: {str(e)}')
