from datetime import datetime
from coletadedados import FaturarEmpresas

dia_emissao = 25
data_atual = datetime.now()

def Faturar(dia_emissao, data_atual):
    try:
        FaturarEmpresas(dia_emissao, data_atual)
    except Exception as e:
        print(f"Ocorreu um erro: {e}. Tentando novamente...")
        FaturarEmpresas(dia_emissao, data_atual)

Faturar(dia_emissao, data_atual)
