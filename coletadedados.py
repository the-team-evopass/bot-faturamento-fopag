from termcolor import colored
from functions.calculation.calculoprorata import calcular_prorata
from functions.calculation.datavencimento import calcular_data_vencimento
from datetime import datetime, timedelta
from functions.generateInvoicing import GenerateInvoicing
from middleware import runGetAllDependents, runGetAllEconomicsGroups, runGetAllHolders
from functions.render import render_html
from functions.sendemail import send_email

from middleware import runGetAllCompanies

def FaturarEmpresas(dia_emissao, data_atual):
    dados_extrato = []
    dados_relatorio = []
    
    listaGruposEconomicos = runGetAllEconomicsGroups()
    respostaAllCompany = runGetAllCompanies()
    listaEmpresas = respostaAllCompany['data']
    listaTitulares = runGetAllHolders()
    listaDependentes = runGetAllDependents()

    # Contador de empresas
    contador_empresas = 0

    # Grupos Economicos
    for grupo in listaGruposEconomicos:
        valor_boleto_grupo = 0
        contador_empresas_grupo = 0
        
        grupo_cnpj = grupo['cnpj']
        grupo_name = grupo['name']
        grupo_billingType = grupo['billingType']
        grupo_companies = grupo['companies']

        qnt_empresas = len(grupo_companies)

        # print(colored(f"Faturamento do grupo {grupo_name} - {grupo_billingType} - {qnt_empresas} empresas.", 'cyan'))

        for empresa in grupo_companies:
            cnpj_empresa_grupo = empresa['cnpj']
            tradeName_empresa_grupo = empresa['tradeName']

            for empresa in listaEmpresas:
                empresa_id = empresa['id']
                empresa_cnpj = empresa['cnpj']  # Cnpj da empresa
                empresa_tradeName = empresa['tradeName']  # Nome da empresa
                empresa_companyStatus = empresa['companyStatus']  # Status da empresa
                empresa_cutoffDate = empresa['cutoffDate']  # Data corte
                empresa_student = empresa['students']
                empresa_agreement = empresa['companyAgreements']
                for agreements in empresa_agreement:
                    empresa_value = agreements['value']
                dados_extrato = []
                dados_relatorio = []

                if empresa_cnpj in cnpj_empresa_grupo:
                    if empresa_cnpj == grupo_cnpj:
                        id_temp = empresa_id
                        name_temp = empresa_tradeName

                    if empresa_companyStatus == "EM IMPLANTACAO" and dia_emissao == empresa_cutoffDate:
                        contagem_value_titular, contagem_value_dependente = 0, 0

                        contador_empresas_grupo += 1

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
                                titular_lastName = titular['lastName']
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
                                                    "name": titular_firstName + " " + titular_lastName,"relationship": "TITULAR","cpf": titular_cpf,"proRata": float(valor_calculo_prorata),
                                                    "value":  float(titular_studentAgreement_value),"totalValue": float(valor_mensal_titular)
                                                })

                                        else:
                                            valor_mensal_titular = titular_studentAgreement_value
                                            dados_extrato.append({
                                                    "name": titular_firstName + " " + titular_lastName,"relationship": "TITULAR","cpf": titular_cpf,"proRata": 0,
                                                    "value":  float(titular_studentAgreement_value),"totalValue": float(valor_mensal_titular)
                                                })

                                        contagem_value_titular += float(valor_mensal_titular)
                                        
                                        # Loop para coletar dados dos Dependentes dos titulares
                                        for dependente in listaDependentes:
                                            dependente_firstName = dependente['firstName']
                                            dependente_lastName = dependente['lastName']
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
                                                        try:
                                                            dados_extrato.append({
                                                                "name": dependente_firstName + " " + dependente_lastName, "relationship": "DEPENDENTE", "cpf": titular_cpf, "proRata": float(valor_calculo_prorata),
                                                                "value":  float(dependente_studentAgreement_value), "totalValue": float(valor_mensal_dependente)
                                                            })
                                                        except:
                                                            print(dependente_firstName)

                                                    else:
                                                        valor_mensal_dependente = dependente_studentAgreement_value
                                                        
                                                        dados_extrato.append({
                                                            "name": dependente_firstName + " " + dependente_lastName, "relationship": "DEPENDENTE", "cpf": titular_cpf, "proRata": 0,
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
                        # print(valor_boleto_empresa)

                        if grupo_billingType == 'APARTADO':
                            print(f"Valor do boleto apartado: {valor_boleto_empresa}")
                            GenerateInvoicing(valor_boleto_empresa, empresa_cnpj, data_vencimento,competencia_mes_ano,dados_extrato,dados_relatorio,valor_soma_total,empresa_id,empresa_tradeName)

                        elif grupo_billingType == 'UNIFICADO':
                            print(f"Valor do boleto unificado: {valor_boleto_empresa}")
                            valor_boleto_grupo += (valor_boleto_empresa)
                            print(f"Valor do boleto unificado: {valor_boleto_grupo}")

                            if qnt_empresas == contador_empresas_grupo:
                                print(f'valor do boleto do grupo unificado: { valor_boleto_grupo}\n')
                                print(f"O id do boleto é {id_temp}")
                                print(f"O nome do boleto é {name_temp}")
                                GenerateInvoicing(valor_boleto_empresa, grupo_cnpj, data_vencimento,competencia_mes_ano,dados_extrato,dados_relatorio,valor_soma_total,id_temp,name_temp)
           