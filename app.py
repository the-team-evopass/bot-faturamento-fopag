from flask import Flask
import functions.criarcobranca as criarcobranca

app = Flask(__name__)

@app.get('/')
def home():
    return 'Bot online'


@app.get('/run')
def executar_bot():
    criarcobranca
    return "Executando Bot de Faturamento EVOPASS"


# Rodar a API
if __name__ == '__main__':
    app.run()