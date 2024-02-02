from termcolor import colored
from functions.calculation.calculoprorata import calcular_prorata
from functions.calculation.datavencimento import calcular_data_vencimento
from datetime import datetime, timedelta
from functions.asaas.criarCobranca import criar_cobranca
from middleware import runGenerateIssueNf, runGetAllDependents, runGetAllHolders
from middleware import runGenerateExtractRequest
from functions.render import render_html
from functions.sendemail import send_email

from middleware import runGetAllCompanies

def FaturarEmpresas(dia_emissao, data_atual):
    dados_extrato = []
    dados_relatorio = []
    
    respostaAllCompany = runGetAllCompanies()
    listaEmpresas = respostaAllCompany['data']
    listaTitulares = runGetAllHolders()
    listaDependentes = runGetAllDependents()

    # Contador de empresas
    contador_empresas = 0

    for empresa in listaEmpresas:
        empresa_id = empresa['id']
        empresa_cnpj = empresa['cnpj']  # Cnpj da empresa
        empresa_tradeName = empresa['tradeName']  # Nome da empresa
        empresa_companyStatus = empresa['companyStatus']  # Status da empresa
        empresa_cutoffDate = empresa['cutoffDate']  # Data corte
        empresa_student = empresa['students']
        if empresa_id != 2204 and empresa_id != 2234 and empresa_id != 2384:

            try: 
                empresa_value = empresa['companyAgreements'][-1]['value']  # Valor que a empresa paga se ela tem apenas um contrato
            except:
                print("Erro ao buscar dados da empresa com id ", empresa_id)
            dados_extrato = []
            dados_relatorio = []

            if empresa_companyStatus == "EM IMPLANTACAO" and dia_emissao == empresa_cutoffDate:
                contagem_value_titular, contagem_value_dependente = 0, 0

                # Contador de titulares
                contador_titulares_empresa = 0
                contador_empresas += 1
                contador_titulares_prorata = 0

                soma_valor_titulares_prorata, soma_valor_dependentes_prorata, soma_valor_mensalidade_titulares, soma_valor_mensalidade_dependentes = 0, 0, 0, 0

                # Filtro das empresas que têm a data de corte igual ao dia atual
                print(colored(f"Faturamento da empresa {empresa_tradeName}.", 'blue'))

                # Tratamento de dados das datas de emissão de boleto e data start do aluno
                data_atual = datetime.now()
                data_emissao = datetime(data_atual.year, data_atual.month, empresa_cutoffDate)  # Data Emissão do Boleto | 2023-10-30
                data_emissao_date = data_emissao.date()  # Emissão em Data 02/10/2023

                emissao_menos_mes = data_emissao_date - timedelta(days=30)  # Emissão de boleto - 30 dias

                dias_adicionais = 10

                # Data de vencimento da cobrança
                data_vencimento = calcular_data_vencimento(empresa_cutoffDate, dias_adicionais)

                competencia_mes_ano = data_emissao_date.strftime('%B de %Y')

                contador_dependentes_prorata = 0
                contador_dependentes_empresa = 0

                # Loop para coletar dados dos Titulares
                if empresa_student != []:
                    for titular in listaTitulares:
                        titular_firstName = titular['firstName']
                        titular_status = titular['status']
                        titular_startValidity = titular['startValidity']
                        titular_cpf = titular['cpf']
                        titular_company = titular['company']
                        titular_companyCNPJ = titular['company']['cnpj']
                        titular_studentAgreement_value = titular['studentAgreement'][-1]['value']
                        titular_studentAgreement_type = titular['studentAgreement'][-1]['type']

                        valor_por_dia = float(titular_studentAgreement_value) / float(30.0)  # valor cobrado por dia
                            
                        if titular_status == True and titular_studentAgreement_type == "FOLHA DE PAGAMENTO":
                            if titular_companyCNPJ == empresa_cnpj:
                                entrada_titular = datetime.strptime(titular_startValidity, '%Y-%m-%dT%H:%M:%S.%fZ') #Data que o aluno iniciou na empresa | 2023-12-05
                                entrada_aluno_date = entrada_titular.date() #Entrada de aluno em Data 05/12/2023
                                contador_titulares_empresa += 1
                                soma_valor_mensalidade_titulares += float(titular_studentAgreement_value)
                                # print(titular_status, titular_studentAgreement_value)
                                
                                if emissao_menos_mes < entrada_aluno_date:
                                    valor_calculo_prorata = calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia)
                                    valor_mensal_titular = float(titular_studentAgreement_value) + float(valor_calculo_prorata)
                                    contador_titulares_prorata += 1
                                    soma_valor_titulares_prorata += float(titular_studentAgreement_value)
                                    print(soma_valor_titulares_prorata)
                                    
                                    dados_extrato.append({
                                            "name": titular_firstName,"relationship": "TITULAR","cpf": titular_cpf,"proRata": float(valor_calculo_prorata),
                                            "value":  float(titular_studentAgreement_value),"totalValue": float(valor_mensal_titular)
                                        })

                                else:
                                    valor_mensal_titular = titular_studentAgreement_value
                                    dados_extrato.append({
                                            "name": titular_firstName,"relationship": "TITULAR","cpf": titular_cpf,"proRata": 0,
                                            "value":  float(titular_studentAgreement_value),"totalValue": float(valor_mensal_titular)
                                        })

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

                                    valor_por_dia = float(dependente_studentAgreement_value) / float(30.0)  # valor cobrado por dia

                                    if dependente_status == True and dependente_studentAgreement_type == "FOLHA DE PAGAMENTO":
                                        if dependente_student_cpf == titular_cpf:
                                            contador_dependentes_empresa += 1
                                            soma_valor_mensalidade_dependentes += float(dependente_studentAgreement_value)

                                            entrada_dependente = datetime.strptime(dependente_startValidity, '%Y-%m-%dT%H:%M:%S.%fZ') #Data que o aluno iniciou na empresa | 2023-10-01
                                            entrada_aluno_date = entrada_dependente.date() #Entrada de aluno em Data 01/10/2023
                                    
                                            if emissao_menos_mes < entrada_aluno_date:
                                                soma_valor_dependentes_prorata += float(dependente_studentAgreement_value)
                                                contador_dependentes_prorata += 1
                                                valor_calculo_prorata = calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia)
                                                valor_mensal_titular = float(titular_studentAgreement_value) + float(valor_calculo_prorata)

                                                dados_extrato.append({
                                                        "name": dependente_firstName, "relationship": "DEPENDENTE", "cpf": titular_cpf, "proRata": float(valor_calculo_prorata),
                                                        "value":  float(dependente_studentAgreement_value), "totalValue": float(valor_mensal_dependente)
                                                    })

                                            else:
                                                valor_mensal_dependente = dependente_studentAgreement_value
                                                
                                                dados_extrato.append({
                                                        "name": dependente_firstName, "relationship": "DEPENDENTE", "cpf": titular_cpf, "proRata": 0,
                                                        "value":  float(dependente_studentAgreement_value), "totalValue": float(valor_mensal_dependente)
                                                    })

                                            contagem_value_dependente += float(valor_mensal_dependente)

                dados_relatorio.append({
                    "reference": "Pro rata - Titulares", "quantity": float(contador_titulares_prorata), "value": float(soma_valor_titulares_prorata)
                })
                dados_relatorio.append({
                    "reference": "Mensalidade  - Titulares", "quantity": float(contador_titulares_empresa), "value": float(soma_valor_mensalidade_titulares)
                })
                dados_relatorio.append({
                    "reference": "Pro rata - Dependentes", "quantity": float(contador_dependentes_prorata), "value": float(soma_valor_dependentes_prorata)
                })
                dados_relatorio.append({
                    "reference": "Mensalidade - Dependentes", "quantity": float(contador_dependentes_empresa),"value": float(soma_valor_mensalidade_dependentes)
                })

                valor_boleto_empresa = float(empresa_value) + float(soma_valor_titulares_prorata) + float(soma_valor_mensalidade_titulares) + float(soma_valor_dependentes_prorata) + float(soma_valor_mensalidade_dependentes)
                valor_soma_total = float(soma_valor_titulares_prorata) + float(soma_valor_mensalidade_titulares) + float(soma_valor_dependentes_prorata) + float(soma_valor_mensalidade_dependentes)

                if valor_boleto_empresa != 0:

                    billingResponse = criar_cobranca(empresa_cnpj, valor_boleto_empresa, data_vencimento)
                    
                    print(colored(billingResponse['billingURL'], 'green'))

                    extractObservation = '''
                        Prezado(a) cliente,
                        Para visualizar e efetuar o pagamento do boleto, acesse o link fornecido.
                        Qualquer problema ou dificuldade, entre em contato conosco.
                        Agradecemos pela sua atenção.
                    '''

                    # Função para emissão de NF
                    runGenerateIssueNf(billingResponse['billingID'], valor_boleto_empresa, datetime.now().strftime('%Y-%m-%d'))

                    #Estou gerando o PDF aqui
                    runGenerateExtractRequest(competencia_mes_ano, data_vencimento, dados_extrato, dados_relatorio, valor_soma_total, empresa_id, extractObservation, billingResponse['billingURL'], empresa_tradeName, empresa_cnpj)
                    
                    # myContentEmail = render_html(empresa_tradeName, competencia_mes_ano, str(valor_soma_total), billingResponse['billingURL'], 'inv_000006811891')
                    # send_email('Teste do bot de faturamento', 'felipe@evopass.app.br', myContentEmail)

                    print(colored('-------------------------------------------------------------------------------', 'yellow', 'on_green', ['underline']))

                else:
                    print('Erro ao gerar cobrança, valor do boleto igual a 0 (coletadedados) ou empresa não tem titulares')
                    print('-------------------------------------------------------------------------------')
        else:
            print(f"A empresa {empresa_tradeName} não foi faturada")
    else:
        print('Não entrou no if - seleção de empresas (coletadedados)')            
                