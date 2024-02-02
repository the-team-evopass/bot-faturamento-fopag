def calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia):
    dias_pro_rata = (data_emissao_date - entrada_aluno_date).days  # dias pro rata é igual a data de emissão menos a entrada do titular
    valor_pro_rata = dias_pro_rata * valor_por_dia  # Valor prorata é igual ao dias pro rata vezes o valor por dia
    return valor_pro_rata