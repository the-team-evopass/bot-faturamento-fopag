import requests
from calculoprorata import calcular_prorata
from datavencimento import calcular_data_vencimento
from datetime import datetime, timedelta
from criarcobranca import criar_cobrancas

# URLs DAS APIs
urlAllCompany = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements%2Cstudents'
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
    contador_empresas = 0

    for empresa in listaEmpresas:
        empresa_cnpj = empresa['cnpj']  # Cnpj da empresa
        empresa_tradeName = empresa['tradeName']  # Nome da empresa
        empresa_companyStatus = empresa['companyStatus']  # Status da empresa
        empresa_cutoffDate = empresa['cutoffDate']  # Data corte
        empresa_value = empresa['companyAgreements'][-1]['value']  # Valor que a empresa paga se ela tem apenas um contrato

        if empresa_companyStatus == "EM IMPLANTACAO":
            if dia_emissao == empresa_cutoffDate:
                contagem_value_titular = 0
                contagem_value_dependente = 0
                # Contador de titulares e dependentes
                contador_titulares_empresa = 0
                contador_dependentes_empresa = 0
                contador_empresas += 1

                # Filtro das empresas que têm a data de corte igual ao dia atual
                print(f"Relação de ativos da empresa {empresa_tradeName} .")

                # Tratamento de dados das datas de emissão de boleto e data start do aluno
                data_atual = datetime.now()
                data_emissao = datetime(data_atual.year, data_atual.month, empresa_cutoffDate)  # Data Emissão do Boleto | 2023-10-30
                data_emissao_date = data_emissao.date()  # Emissão em Data 02/10/2023

                # Tratamento de dados dos valores
                valor_por_dia = 2.663  # valor cobrado por dia
                data_corte = empresa_cutoffDate  # Data Corte
                emissao_menos_mes = data_emissao_date - timedelta(days=30)  # Emissão de boleto - 30 dias

                dias_adicionais = 10

                # Data de vencimento da cobrança
                data_vencimento = calcular_data_vencimento(empresa_cutoffDate, dias_adicionais)

                competencia_mes_ano = data_emissao_date.strftime('%B de %Y')

                # Loop para coletar dados dos Titulares
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
                            entrada_titular = datetime.strptime(titular_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-10-01
                            entrada_aluno_date = entrada_titular.date() #Entrada de aluno em Data 01/10/2023
                            contador_titulares_empresa += 1
                            if emissao_menos_mes < entrada_aluno_date:
                                valor_calculo_prorata = calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia)
                                valor_mensal_titular = float(titular_studentAgreement_value) + float(valor_calculo_prorata)
                            else:
                                valor_mensal_titular = titular_studentAgreement_value
                            
                            contagem_value_titular += float(valor_mensal_titular)

                            # Loop para coletar dados dos Dependentes dos titulares
                            for dependente in listaDependentes:
                                dependente_firstName = dependente['firstName']
                                dependente_status = dependente['status']
                                dependente_startValidity = dependente['startValidity']
                                dependente_cpf = dependente['cpf']
                                dependente_student_cpf = dependente['student']['cpf']
                                dependente_studentAgreement_value = dependente['dependentAgreement'][-1]['value']
                                dependente_studentAgreement_type = dependente['dependentAgreement'][-1]['type']
                                dependente_startValidity = dependente['startValidity']

                                entrada_dependente = datetime.strptime(dependente_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-10-01
                                entrada_aluno_date = entrada_dependente.date() #Entrada de aluno em Data 01/10/2023
                                if dependente_status == True and dependente_studentAgreement_type == "F":
                                    if dependente_student_cpf == titular_cpf:
                                        if emissao_menos_mes < entrada_aluno_date:
                                            contador_dependentes_empresa += 1
                                            valor_calculo_prorata = calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia)
                                            valor_mensal_dependente = float(dependente_studentAgreement_value) + float(valor_calculo_prorata)
                                        else:
                                            valor_mensal_dependente = dependente_studentAgreement_value
                                            contador_dependentes_empresa += 1
                                        
                                        contagem_value_dependente += float(valor_mensal_dependente)
                                else:
                                    print(f"O dependente {dependente_firstName}, não está ATIVO")

                valor_total_empresa = float(empresa_value) + float(contagem_value_titular) + float(contagem_value_dependente)

                #CRIAR COBRANÇA
                #Api do asaas
                api_key = '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNTg2MTM6OiRhYWNoX2QyMGQ0MGYwLWYwZTEtNDI5NS1iYmRlLTIyNzFjMTZlNjZhNw=='

                #URLs do asaas
                urlListarClientes = 'https://sandbox.asaas.com/api/v3/customers'
                urlCriarCobranca = 'https://sandbox.asaas.com/api/v3/payments'

                #Cabeçalho
                headers = {
                    'Content-Type': 'application/json',
                    'access_token': api_key
                }

                #Listar clientes
                response = requests.get(urlListarClientes, headers=headers)

                if response.status_code == 200:
                    #Função para Criar Cobrança
                    criar_cobrancas(urlListarClientes, urlCriarCobranca, empresa_cnpj, valor_total_empresa, headers, data_vencimento)
                    print(f"Cobrança criada para {contador_empresas} empresas")
                else:
                    print(f"Erro ao listar os clientes. Status Code: {response.status_code}")
                    print(f"Resposta: {response.text}")

else:
    print(f"Erro na requisição. Código de Status: {respostaAllCompany.status_code}")
