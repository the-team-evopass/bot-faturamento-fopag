
from datetime import datetime
from flask import Flask
from main import FaturarEmpresas

app = Flask(__name__)

@app.get('/')
def home():
    return 'Bot online'


@app.get('/run')
def executar_bot():
    dia_emissao = data_atual
    data_atual = datetime.now()
    FaturarEmpresas(dia_emissao, data_atual)
    
    return "Executando Bot de Faturamento EVOPASS"


# Rodar a API
if __name__ == '__main__':
    app.run()