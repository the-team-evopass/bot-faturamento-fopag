from datetime import datetime
from coletadedados import FaturarEmpresas
from teste import FaturarEmpresasTeste

#Substituir por datetime.now() e extrair o dia
dia_emissao = 2
data_atual = datetime.now()

FaturarEmpresasTeste(dia_emissao, data_atual)