from datetime import datetime
from tratativa1 import Tratativa

#Substituir por datetime.now() e extrair o dia
dia_emissao = 2
data_atual = datetime.now()

Tratativa(dia_emissao, data_atual)