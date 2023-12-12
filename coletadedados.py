import requests
from calculoprorata import calcular_prorata
from datavencimento import calcular_data_vencimento
from datetime import datetime, timedelta

# URLs DAS APIs
urlAllCompany = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements'
urlAllStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student?expand=dependents%2CstudentContact%2CstudentAgreement%2CstudentAddress%2Ccompany'
urlAllDependent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/dependent?expand=student%2CdependentContact%2CdependentAgreement%2CdependentAddress'

# Listagem de Empresas e a data corte
respostaAllCompany = requests.get(urlAllCompany)
respostaAllStudents = requests.get(urlAllStudent)
respostaAllDependent = requests.get(urlAllDependent)

dia_emissao = 12
data_atual = datetime.now()

if respostaAllCompany.status_code == 200:
    companyJson = respostaAllCompany.json()
    listaEmpresas = companyJson['data']

    studentJson = respostaAllStudents.json()
    listaTitulares = studentJson

    dependentJson = respostaAllDependent.json()
    listaDependentes = dependentJson

    # Contador de empresas
    contagem_empresas = 0
   

    # Loop para coletar dados das empresas
    for empresa in listaEmpresas:
        empresa_cnpj = empresa['cnpj']  # Cnpj da empresa
        empresa_tradeName = empresa['tradeName']  # Nome da empresa
        empresa_companyStatus = empresa['companyStatus']  # Status da empresa
        empresa_cutoffDate = empresa['cutoffDate']  # Data corte
        empresa_companyAgreements_value = empresa['companyAgreements']  # Valor que a empresa paga
        if empresa_companyStatus == "EM IMPLANTACAO":
            for valor in empresa_companyAgreements_value:
                empresa_value = valor['value']
            contagem_value_titular = 0
            contagem_value_dependente = 0
            contagem_empresas += 1
             # Contador de titulares e dependentes
            contagem_titulares_empresa = 0
            contagem_dependentes_empresa = 0

            # Filtro das empresas que tem a data corte igual ao dia atual
            if dia_emissao == empresa_cutoffDate:
                print(f"Relação de ativos da empresa {empresa_tradeName} .")

                #Tratamento de dados das datas de emissão de boleto e data start do aluno 
                data_emissao = datetime(data_atual.year, data_atual.month, empresa_cutoffDate) #Data Emissão do Boleto | 2023-10-30
                
                data_emissao_date = data_emissao.date() #Emissão em Data 02/10/2023

                #Tratamento de dados dos valores
                valor_por_dia=2.663 #valor cobrado por dia
                data_corte = empresa_cutoffDate # Data Corte
                emissao_menos_mes = data_emissao_date - timedelta(days=30) #Emissão de boleto - 30 dias

                # Data de vencimento da cobrança
                calcular_data_vencimento
                data_vencimento = calcular_data_vencimento # Data de vencimento (data corte + 10)

                competencia_mes_ano = data_emissao_date.strftime('%B de %Y')
                print(f"Competência: {competencia_mes_ano}")
                #print(f"Data de vencimento: {data_vencimento}")

            # Loop para coletar dados dos Titulares
            for titular in listaTitulares:
                titular_firstName = titular['firstName']
                titular_status = titular['status']
                titular_startValidity = titular['startValidity']
                titular_cpf = titular['cpf']
                titular_agreement = titular['studentAgreement']
                titular_company = titular['company']
                titular_companyCNPJ = titular['company']['cnpj']
                titular_studentAgreement_value = titular['studentAgreement'][0]['value']
                titular_studentAgreement_type = titular['studentAgreement'][0]['type']
                titular_startValidity = titular['startValidity']
                print(titular_startValidity)
                entrada_titular = datetime.strptime(titular_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-10-01
                entrada_aluno_date = entrada_titular.date() #Entrada de aluno em Data 01/10/2023
                if titular_status == True and titular_studentAgreement_type == "F":
                    if titular_companyCNPJ == empresa_cnpj:
                        print(f"valor mensal titular: {titular_studentAgreement_value}")
                        contagem_value_titular += float(titular_studentAgreement_value)
                        contagem_titulares_empresa += 1
                        if emissao_menos_mes < entrada_aluno_date:
                            valor_calculo_prorata = calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia)
                            print(valor_calculo_prorata)
                            valor_mensal_titular = float(titular_studentAgreement_value) + float(valor_calculo_prorata)
                            print(f"O titular {titular_firstName} tem o valor pro rata igual a {valor_mensal_titular}")
                        else:
                            print(f"O titular {titular_firstName} não é prorata")

                        # Loop para coletar dados dos Dependentes dos titulares
                        for dependente in listaDependentes:
                            dependente_firstName = dependente['firstName']
                            dependente_status = dependente['status']
                            dependente_startValidity = dependente['startValidity']
                            dependente_cpf = dependente['cpf']
                            dependente_agreement = dependente['dependentAgreement']
                            dependente_student = dependente['student']['cpf']
                            dependente_studentAgreement_value = dependente['studentAgreement'][0]['value']
                            dependente_studentAgreement_type = dependente['studentAgreement'][0]['type']
                            dependente_startValidity = dependente['startValidity']
                            entrada_dependente = datetime.strptime(dependente_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-10-01
                            entrada_aluno_date = entrada_dependente.date() #Entrada de aluno em Data 01/10/2023
                            if dependente_status == True and dependente_studentAgreement_type == "F":
                                contagem_dependentes_empresa += 1
                                if dependente_student == titular_cpf:
                                    contagem_value_dependente += 1
                                    contagem_value_dependente += float(dependente_studentAgreement_value)
                                    if emissao_menos_mes < entrada_aluno_date:
                                        valor_calculo_prorata = calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia)
                                        valor_mensal_dependente = dependente_studentAgreement_value + valor_calculo_prorata
                                        print(f"O {dependente_firstName} tem o valor pro rata igual a {valor_calculo_prorata}")

                                    else:
                                        print(f"O {dependente_firstName} não é prorata")
                            else:
                                print(f"O dependente {dependente_firstName}, não está ATIVO")

        print(f"A empresa {empresa_tradeName} pagará {empresa_value} por valor de vida, ela tem {contagem_titulares_empresa} titulares e pagará {contagem_value_titular} por titular e {contagem_value_dependente} por dependente.")
        valor_total_empresa = float(empresa_value) + float(contagem_value_titular) + float(contagem_value_dependente)
        print(f"valor total da empresa: {valor_total_empresa}")
        print('                                                           ')
    print(contagem_empresas)

else:
    print(f"Erro na requisição. Código de Status: {respostaAllCompany.status_code}")
