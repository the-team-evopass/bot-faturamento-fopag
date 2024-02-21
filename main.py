from datetime import datetime
from coletadedados import FaturarEmpresas

dia_emissao = 20
data_atual = datetime.now()

FaturarEmpresas(dia_emissao, data_atual)