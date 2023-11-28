from datetime import datetime, timedelta

def calcular_data_vencimento(empresa_cutoffDate, dias_adicionais):
    # Obtém a data atual
    data_atual = datetime.now()

    # Cria um objeto datetime com o mesmo ano e mês que a data atual, mas com o dia de empresa_cutoffDate
    data_corte = datetime(data_atual.year, data_atual.month, empresa_cutoffDate)

    # Adiciona dias_adicionais à data_corte
    data_final = data_corte + timedelta(days=dias_adicionais)

    # Formata a data final para imprimir apenas a parte da data
    data_final_formatada = data_final.strftime("%Y-%m-%d")

    return data_final_formatada
