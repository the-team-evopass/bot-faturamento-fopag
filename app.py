from flask import Flask
import criarcobranca
import os
import signal

app = Flask(__name__)

@app.get('/')
def home():
    return 'Bot online'


@app.get('/run')
def executar_bot():
    criarcobranca
    print('Encerrando a aplicação...')
    encerrar_servidor()
    print('Aplicação encerrada')
    return "Executando Bot de Faturamento EVOPASS"

def encerrar_servidor():
    # Encerre o processo Flask usando o sinal SIGINT
    os.kill(os.getpid(), signal.SIGINT)

# Rodar a API
if __name__ == '__main__':
    app.run()