from datetime import datetime, timedelta

contador_titulares = 0
data_emissao = datetime(2023, 11, 2).date()
entrada_aluno = datetime(2023, 10, 7).date()
empresa_cutoffDate = 3
valor_por_dia=2.663

# Remova a chamada `replace` para evitar o erro
data_corte = empresa_cutoffDate  # Utilize `empresa_cutoffDate` diretamente

emissao_menos_mes = data_emissao - timedelta(days=30)

valor_pro_rata = 0.0

if emissao_menos_mes < entrada_aluno:
    dias_pro_rata = (data_emissao - entrada_aluno).days
    valor_pro_rata = dias_pro_rata * valor_por_dia
else:
    print("A data de emissão não está dentro do período pró-rata.")

titular_studentAgreement_value = 29.0

valor_total = valor_pro_rata + titular_studentAgreement_value

print(f"Nome do Aluno: teste, Parentesco: TITULAR, CPF: 123, Pró rata: {valor_pro_rata}, Valor: {titular_studentAgreement_value}, Valor Total: {valor_total}")
contador_titulares += 1

valor_referencia = titular_studentAgreement_value * contador_titulares

#REFERÊNCIA
print('')
print(f"Pró rata - Titulares, Quantidade: {contador_titulares}, valor: {valor_referencia}")
print('')