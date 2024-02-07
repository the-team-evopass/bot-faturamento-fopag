from datetime import datetime
from coletadedados import FaturarEmpresas

#Substituir por datetime.now() e extrair o dia
dia_emissao = 8
data_atual = datetime.now()

FaturarEmpresas(dia_emissao, data_atual)