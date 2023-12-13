from datetime import datetime
from calculoprorata import calcular_prorata

def calcular_valor_titulares(listaTitulares, empresa_cnpj, emissao_menos_mes, valor_por_dia, data_emissao_date):
    contagem_value_titular = 0
    contador_titulares_empresa = 0

    for titular in listaTitulares:
        titular_firstName = titular['firstName']
        titular_status = titular['status']
        titular_startValidity = titular['startValidity']
        titular_cpf = titular['cpf']
        titular_company = titular['company']
        titular_companyCNPJ = titular['company']['cnpj']
        titular_studentAgreement_value = titular['studentAgreement'][-1]['value']
        titular_studentAgreement_type = titular['studentAgreement'][-1]['type']
        titular_startValidity = titular['startValidity']

        if titular_status == True and titular_studentAgreement_type == "F":
            if titular_companyCNPJ == empresa_cnpj:
                entrada_titular = datetime.strptime(titular_startValidity, '%Y-%m-%d')
                entrada_aluno_date = entrada_titular.date()
                contador_titulares_empresa += 1

                if emissao_menos_mes < entrada_aluno_date:
                    valor_calculo_prorata = calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia)
                    valor_mensal_titular = float(titular_studentAgreement_value) + float(valor_calculo_prorata)
                    print(f"O titular {titular_firstName} tem o valor pro rata + mensalidade igual a {valor_mensal_titular}")
                else:
                    valor_mensal_titular = titular_studentAgreement_value
                    print(f"O titular {titular_firstName} não é prorata, valor mensal = {titular_studentAgreement_value}")

                contagem_value_titular += float(valor_mensal_titular)

    return contagem_value_titular, contador_titulares_empresa