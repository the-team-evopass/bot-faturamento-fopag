import requests
from tabulate import tabulate
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

# Dados Extrato
cabecalhos_extrato = ["Nome do Aluno", "Parentesco", "CPF", "Pró rata", "Valor", "Valor Total"] # Cabeçalhos das colunas
cabecalhos_relatorio = ["Referência", "Quantidade", "Valor"]# Cabeçalhos das colunas

dados_extrato = []
dados_relatorio = []

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
        dados_extrato = []
        dados_relatorio = []
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

                contador_titulares_prorata = 0

                soma_valor_titulares_prorata = 0
                soma_valor_dependentes_prorata = 0
                soma_valor_mensalidade_titulares = 0
                soma_valor_mensalidade_dependentes = 0

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
                    
                    contador_dependentes_prorata = 0
                    contador_dependentes_empresa = 0
                        
                    if titular_status == True and titular_studentAgreement_type == "F":
                        if titular_companyCNPJ == empresa_cnpj:
                            entrada_titular = datetime.strptime(titular_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-12-05
                            entrada_aluno_date = entrada_titular.date() #Entrada de aluno em Data 05/12/2023
                            contador_titulares_empresa += 1
                            soma_valor_mensalidade_titulares += float(titular_studentAgreement_value)

                            if emissao_menos_mes < entrada_aluno_date:
                                valor_calculo_prorata = calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia)
                                valor_mensal_titular = float(titular_studentAgreement_value) + float(valor_calculo_prorata)
                                contador_titulares_prorata += 1
                                soma_valor_titulares_prorata += float(titular_studentAgreement_value)

                                dados_extrato.append([titular_firstName, "TITULAR", titular_cpf, valor_calculo_prorata, titular_studentAgreement_value, valor_mensal_titular])

                            else:
                                valor_mensal_titular = titular_studentAgreement_value
                                
                                dados_extrato.append([titular_firstName, "TITULAR", titular_cpf, "-", titular_studentAgreement_value, valor_mensal_titular])

                            dados_relatorio.append(["Pró rata - Titulares", contador_titulares_prorata, soma_valor_titulares_prorata])
                            dados_relatorio.append(["Mensalidade - Titulares", contador_titulares_empresa, soma_valor_mensalidade_titulares])
                            
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
                                if dependente_status == True and dependente_studentAgreement_type == "F":
                                    if dependente_student_cpf == titular_cpf:
                                        contador_dependentes_empresa += 1
                                        soma_valor_mensalidade_dependentes += float(dependente_studentAgreement_value)

                                        entrada_dependente = datetime.strptime(dependente_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-10-01
                                        entrada_aluno_date = entrada_dependente.date() #Entrada de aluno em Data 01/10/2023
                                
                                        if emissao_menos_mes < entrada_aluno_date:
                                            soma_valor_dependentes_prorata += float(dependente_studentAgreement_value)

                                            valor_calculo_prorata = calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia)
                                            valor_mensal_titular = float(titular_studentAgreement_value) + float(valor_calculo_prorata)

                                            dados_extrato.append([dependente_firstName, "DEPENDENTE", titular_cpf, valor_calculo_prorata, dependente_studentAgreement_value, valor_mensal_dependente])

                                        else:
                                            valor_mensal_dependente = dependente_studentAgreement_value
                                            
                                            dados_extrato.append([dependente_firstName, "DEPENDENTE", titular_cpf, "-", dependente_studentAgreement_value, valor_mensal_dependente])

                                        contagem_value_dependente += float(valor_mensal_dependente)

                            dados_relatorio.append(["Pró rata - Dependentes", contador_dependentes_prorata, soma_valor_dependentes_prorata])
                            dados_relatorio.append(["Mensalidade - Dependentes", contador_dependentes_empresa, soma_valor_mensalidade_dependentes])

                valor_boleto_empresa = float(empresa_value) + float(soma_valor_titulares_prorata) + float(soma_valor_mensalidade_titulares) + float(soma_valor_dependentes_prorata) + float(soma_valor_mensalidade_dependentes)
                valor_soma_total = float(soma_valor_titulares_prorata) + float(soma_valor_mensalidade_titulares) + float(soma_valor_dependentes_prorata) + float(soma_valor_mensalidade_dependentes)
                dados_relatorio.append(["Total", "", valor_soma_total])

                print(f"Competência: {competencia_mes_ano}")
                print(f"Data de Vencimento: {data_vencimento}")
                                        
                print(tabulate(dados_extrato, headers=cabecalhos_extrato, tablefmt="grid"))
                print(tabulate(dados_relatorio, headers=cabecalhos_relatorio, tablefmt="grid"))

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
                    criar_cobrancas(urlListarClientes, urlCriarCobranca, empresa_cnpj, valor_boleto_empresa, headers, data_vencimento)
                    print(f"Cobrança criada para {contador_empresas} empresas")
                else:
                    print(f"Erro ao listar os clientes. Status Code: {response.status_code}")
                    print(f"Resposta: {response.text}")
else:
    print(f"Erro na requisição. Código de Status: {respostaAllCompany.status_code}")
