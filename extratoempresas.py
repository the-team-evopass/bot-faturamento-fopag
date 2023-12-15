import requests
from datetime import datetime, timedelta
from tabulate import tabulate
from datavencimento import calcular_data_vencimento
import json

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

# Dados Extrato
cabecalhos_extrato = ["Nome do Aluno", "Parentesco", "CPF", "Pró rata", "Valor", "Valor Total"] # Cabeçalhos das colunas
cabecalhos_relatorio = ["Referência", "Quantidade", "Valor"]# Cabeçalhos das colunas

dados_extrato = []
dados_relatorio = []

print(f"Testando como se o dia atual fosse {dia_emissao} ...")
print("")

# Listagem de Empresas e a data corte
respostaAllCompany = requests.get(urlAllCompany)
respostaAllStudents = requests.get(urlAllStudent)
respostaAllDependent = requests.get(urlAllDependent)

if respostaAllCompany.status_code == 200:
    companyJson = respostaAllCompany.json()
    listaEmpresas = companyJson['data']

    studentJson = respostaAllStudents.json()
    listaTitulares = studentJson

    dependentJson = respostaAllDependent.json()
    listaDependentes = dependentJson

    # Contador de empresas
    contagem_empresas_implantacao = 0

    # Loop para coletar dados das empresas
    for empresa in listaEmpresas:
        empresa_cnpj = empresa['cnpj'] # Cnpj da empresa
        empresa_tradeName = empresa['tradeName'] # Nome da empresa
        empresa_companyStatus = empresa['companyStatus'] # Status da empresa
        empresa_cutoffDate = empresa['cutoffDate'] # Data corte
        empresa_companyAgreements_value = empresa['companyAgreements'] #Valor que a empresa paga
        for valor in empresa_companyAgreements_value:
            empresa_value = valor['value']

        # Contador de titulares e dependentes
        contagem_titulares_empresa = 0
        contagem_dependentes_empresa = 0

        # Lógica para filtrar apenas as empresas ativas
        if empresa_companyStatus == "EM IMPLANTACAO":
            # print(f"CNPJ: {empresa_cnpj}    Nome: {empresa_tradeName}   Data corte:{empresa_cutoffDate}") 
            contagem_empresas_implantacao += 1
            
            # Filtro das empresas que tem a data corte igual ao dia atual
            if dia_emissao == empresa_cutoffDate:
                print(f"Relação de ativos da empresa {empresa_tradeName} .")

                contador_titulares_prorata = 0
                contador_titulares = 0
                contador_dependente_prorata = 0
                contador_dependente = 0

                soma_valores_prorata = 0
                soma_mensalidade_titular = 0
                soma_valor_total = 0
                soma_mensalidade_total = 0

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

                #Filtro para verificar a quantidade de titulares ativos na empresa
                for titular in listaTitulares:
                    titular_firstName = titular['firstName']
                    titular_status = titular['status']
                    titular_startValidity = titular['startValidity']
                    titular_cpf = titular['cpf']
                    titular_company = titular['company']
                    titular_companyCNPJ = titular['company']['cnpj']
                    titular_studentAgreement_value = titular['studentAgreement'][0]['value']
                    titular_studentAgreement_type = titular['studentAgreement'][0]['type']
                    titular_startValidity = titular['startValidity']
                    
                    entrada_titular = datetime.strptime(titular_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-10-01
                    entrada_titular_date = entrada_titular.date() #Entrada de aluno em Data 01/10/2023

                    valor_pro_rata = 0.0 #Contador float

                    # Comparar CNPJ da empresa atual com o da empresa do titular atual
                    if titular_companyCNPJ == empresa_cnpj:
                        if titular_status == True and titular_studentAgreement_type == "F":
                            contagem_titulares_empresa += 1 

                            total_dependentes_titular = 0

                            executado = False

                            # Loop para coletar dados dos Dependentes dos titulares
                            for dependente in listaDependentes:
                                dependente_firstName = dependente['firstName']
                                dependente_status = dependente['status']
                                dependente_startValidity = dependente['startValidity']
                                dependente_cpf = dependente['cpf']
                                dependente_agreement = dependente['dependentAgreement']
                                dependente_student = dependente['student']['cpf']

                                if dependente_status == True:
                                    for dependente_agreement_value in dependente_agreement:
                                        dependente_value = dependente_agreement_value['value']
                                        if dependente_student == titular_cpf:
                                            total_dependentes_titular += 1
                                    
                                    entrada_dependente = datetime.strptime(dependente_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-10-01
                                    entrada_dependente_date = entrada_dependente.date() #Entrada de aluno em Data 01/10/2023
                                    valor_pro_rata_dependente = 0.0 #Contador float

                                    #EXTRATO 03/10/2023 < 01/10/2023
                                    if emissao_menos_mes < entrada_titular_date:

                                        if executado == False:
                                            #Calculo extrato titulares
                                            dias_pro_rata_negativo = (data_emissao_date - entrada_titular_date).days
                                            dias_pro_rata = dias_pro_rata_negativo # X -1

                                            print(f"O {titular_firstName} tem {dias_pro_rata} dias pro rata")
                                            valor_pro_rata = dias_pro_rata * valor_por_dia     
                                            contador_titulares_prorata += 1
                                            contador_titulares += 1
                                        
                                            valor_total = valor_pro_rata + float(titular_studentAgreement_value)

                                            valor_referencia = titular_studentAgreement_value * contador_titulares_prorata

                                            soma_valores_prorata += valor_pro_rata
                                            soma_mensalidade_titular += float(titular_studentAgreement_value)

                                            soma_valor_total += valor_total

                                            soma_mensalidade_total = contador_titulares * float(titular_studentAgreement_value)

                                            # Adiciona os dados do titular à lista
                                            dados_extrato.append([titular_firstName, "TITULAR", titular_cpf, valor_pro_rata, titular_studentAgreement_value, valor_total])
                                            dados_relatorio.append(["Pro rata - Titulares", contador_titulares_prorata, soma_valor_total])

                                            executado = True

                                        #Calculo extrato dependentes
                                        dias_pro_rata_negativo_dependente = (data_emissao_date - entrada_dependente_date).days
                                        dias_pro_rata_dependente = dias_pro_rata_negativo_dependente # X -1

                                        print(f"O Dependente: {dependente_firstName} tem {dias_pro_rata_dependente} dias pro rata")
                                        valor_pro_rata_dependente = dias_pro_rata_dependente * valor_por_dia     
                                        contador_dependente_prorata += 1
                                        contador_dependente += 1
                                    
                                        valor_total_dependente = valor_pro_rata_dependente + float(dependente_agreement_value)

                                        valor_referencia_dependente = dependente_agreement_value * contador_dependente_prorata

                                        soma_valores_prorata_dependente += valor_pro_rata_dependente
                                        soma_mensalidade_dependente += float(dependente_agreement_value)

                                        total_coluna = soma_valores_prorata + soma_valores_prorata_dependente + soma_mensalidade_titular + soma_mensalidade_dependente

                                        soma_valor_total_dependente += valor_total_dependente

                                        soma_mensalidade_total = contador_titulares * float(titular_studentAgreement_value)
                                        # Adiciona os dados do dependente à lista
                                        dados_extrato.append([dependente_firstName, "DEPENDENTE", titular_cpf, valor_pro_rata_dependente, dependente_agreement_value, valor_total_dependente])
                                        dados_relatorio.append(["Pro rata - Dependentes", contador_dependente_prorata, soma_valor_total_dependente])
                                    else:
                                        if executado == False:
                                            print(f"O {titular_firstName} não tem pró rata.")
                                            valor_total = 0
                                            valor_pro_rata = 0
                                            contador_titulares += 1
                                            soma_mensalidade_total = contador_titulares * float(titular_studentAgreement_value)
                                            soma_valor_total += valor_total

                                            soma_total = float(soma_mensalidade_total) + float(soma_valor_total)
                                            # Adiciona os dados do titular à lista
                                            dados_extrato.append([titular_firstName, "TITULAR", titular_cpf, valor_pro_rata, titular_studentAgreement_value, valor_total])

                                            executado = True 
                                        
                                        
                                        valor_total_dependente = 0
                                        valor_pro_rata_dependente = 0
                                        contador_dependente += 1
                                        soma_mensalidade_total_dependente = contador_dependente * float(dependente_agreement_value)
                                        soma_valor_total_dependente += valor_total_dependente

                                        soma_valor_total_dependente = float(soma_mensalidade_total_dependente) + float(soma_valor_total_dependente)
                                        # Adiciona os dados do titular à lista
                                        dados_extrato.append([dependente_firstName, "DEPENDENTES", titular_cpf, valor_pro_rata_dependente, dependente_agreement_value, valor_total_dependente])
                        
                        total_dependentes_titular = 0

                        soma_valores_prorata = 0
                        soma_mensalidade_titular = 0
                        soma_valor_total = 0

                        soma_valores_prorata_dependente = 0
                        soma_mensalidade_dependente = 0
                        soma_valor_total_dependente = 0

                        if emissao_menos_mes < entrada_titular_date:
                            if executado == False:
                                #Calculo extrato titulares
                                dias_pro_rata_negativo = (data_emissao_date - entrada_titular_date).days
                                dias_pro_rata = dias_pro_rata_negativo # X -1

                                print(f"O {titular_firstName} tem {dias_pro_rata} dias pro rata")
                                valor_pro_rata = dias_pro_rata * valor_por_dia     
                                contador_titulares_prorata += 1
                                contador_titulares += 1
                            
                                valor_total = valor_pro_rata + float(titular_studentAgreement_value)

                                valor_referencia = titular_studentAgreement_value * contador_titulares_prorata

                                soma_valores_prorata += valor_pro_rata
                                soma_mensalidade_titular += float(titular_studentAgreement_value)

                                soma_valor_total += valor_total

                                soma_mensalidade_total = contador_titulares * float(titular_studentAgreement_value)

                                # Adiciona os dados do titular à lista
                                dados_extrato.append([titular_firstName, "TITULAR", titular_cpf, valor_pro_rata, titular_studentAgreement_value, valor_total])
                                dados_relatorio.append(["Pro rata - Titulares", contador_titulares_prorata, soma_valor_total])

                                executado = True
                        else:
                            if executado == False:
                                print(f"O {titular_firstName} não tem pro rata.")
                                valor_total = 0
                                valor_pro_rata = 0
                                contador_titulares += 1
                                soma_mensalidade_total = contador_titulares * float(titular_studentAgreement_value)

                                soma_total = float(soma_mensalidade_total) + float(soma_valor_total)
                                soma_valor_total += valor_total
                                # Adiciona os dados do titular à lista
                                dados_extrato.append([titular_firstName, "TITULAR", titular_cpf, valor_pro_rata, titular_studentAgreement_value, valor_total])

                                executado = True
                                
                            
                dados_relatorio.append(["Pro rata - Dependentes", contador_dependente_prorata, soma_valor_total_dependente])                
                soma_total = float(soma_mensalidade_total) + float(soma_valor_total) + float(soma_mensalidade_total_dependente) + float(soma_valor_total_dependente)

                dados_relatorio.append(["Mensalidade -  Titulares", contador_titulares, soma_mensalidade_total])
                dados_relatorio.append(["Mensalidade -  Dependentes", contador_dependente, soma_mensalidade_total_dependente])
                dados_relatorio.append(["TOTAL", "", soma_total])

                # Imprime a tabela
                print(tabulate(dados_extrato, headers=cabecalhos_extrato, tablefmt="grid"))
                print(tabulate(dados_relatorio, headers=cabecalhos_relatorio, tablefmt="grid"))

                relacao_ativos = (contagem_titulares_empresa + contagem_dependentes_empresa) * empresa_companyAgreements_value

            else:
                print(f"A empresa {empresa_tradeName}, não tem a data corte igual ao dia de hoje")

                # Data de vencimento da cobrança
            calcular_data_vencimento # Data de vencimento (data corte + 10)
        else:
            print(f"A empresa {empresa_tradeName}, não está ativa")
    print("")

    # Use tabulate para exibir a tabela
    print(tabulate(dados_extrato, headers=cabecalhos_extrato, tablefmt="grid"))
    print(tabulate(dados_relatorio, headers=cabecalhos_relatorio, tablefmt="grid"))

    # Converter os dados para estruturas compatíveis com JSON
    dados_json_extrato = {'dados_extrato': [dict(zip(cabecalhos_extrato, linha)) for linha in dados_extrato]}
    dados_json_relatorio = {'dados_relatorio': [dict(zip(cabecalhos_relatorio, linha)) for linha in dados_relatorio]}

    # Converter para JSON
    json_extrato = json.dumps(dados_json_extrato, indent=2)
    json_relatorio = json.dumps(dados_json_relatorio, indent=2)

    # Exibir o JSON
    print(json_extrato)
    print(json_relatorio)

else:

    print(f"Erro na requisição. Código de Status: {respostaAllCompany.status_code}")