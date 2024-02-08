def calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia):
    meses_31 = [1, 3, 5, 7, 10, 12]
    dias_pro_rata = (data_emissao_date - entrada_aluno_date).days  # dias pro rata é igual a data de emissão menos a entrada do titular
    valor_pro_rata = dias_pro_rata * valor_por_dia  # Valor prorata é igual ao dias pro rata vezes o valor por dia
    
    if entrada_aluno_date.month in meses_31:
        valor_pro_rata -= valor_por_dia
        
    elif entrada_aluno_date.month == 2: # data vigente no mes com menos de 30 dias
        valor_pro_rata += (valor_por_dia * 3)
    
    return valor_pro_rata