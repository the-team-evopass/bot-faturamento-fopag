import requests
from datetime import datetime, timedelta
from tabulate import tabulate
from datavencimento import calcular_data_vencimento

# URLs DAS APIs
urlAllCompany = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements'
urlAllStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student?expand=dependents%2CstudentContact%2CstudentAgreement%2CstudentAddress%2Ccompany'
urlAgreementStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student_agreement'
urlAllDependent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/dependent?expand=dependentContact%2CdependentAgreement%2CdependentAddress'
urlAgreementDependent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/dependent_agreement'

#Obter a data atual
dia_emissao_teste = 2 #teste com 18
data_atual = datetime.now()

print(f"Testando como se o dia atual fosse {dia_emissao_teste} ...")
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

        soma_valores_prorata_titulares = 0
        soma_mensalidade_titular = 0
        soma_valor_total_titular = 0
        soma_mensalidade_total_titular = 0

        soma_valores_prorata_dependente = 0
        soma_mensalidade_dependente = 0
        soma_valor_total_dependente = 0
        soma_mensalidade_total_dependente = 0

        # Lógica para filtrar apenas as empresas ativas
        if empresa_companyStatus == "EM IMPLANTACAO":
            # print(f"CNPJ: {empresa_cnpj}    Nome: {empresa_tradeName}   Data corte:{empresa_cutoffDate}") 
            contagem_empresas_implantacao += 1
            
            # Filtro das empresas que tem a data corte igual ao dia atual
            if dia_emissao_teste == empresa_cutoffDate:
                print(f"Relação de ativos da empresa {empresa_tradeName} .")

                contador_titulares_prorata = 0
                contador_titulares = 0

                contador_dependentes_prorata = 0
                contador_dependentes = 0

                #Tratamento de dados das datas de emissão de boleto e data start do aluno 
                data_emissao = datetime(data_atual.year, data_atual.month, empresa_cutoffDate) #Data Emissão do Boleto | 2023-10-30
                
                data_emissao_date = data_emissao.date() #Emissão em Data 02/10/2023

                #Tratamento de dados dos valores
                valor_por_dia = 2.663 #valor cobrado por dia
                data_corte = empresa_cutoffDate # Data Corte
                emissao_menos_mes = data_emissao_date - timedelta(days=30) #Emissão de boleto - 30 dias

                # Data de vencimento da cobrança
                calcular_data_vencimento
                data_vencimento = calcular_data_vencimento # Data de vencimento (data corte + 10)

                competencia_mes_ano = data_emissao_date.strftime('%B de %Y')
                print(f"Competência: {competencia_mes_ano}")
                #print(f"Data de vencimento: {data_vencimento}")

                dados_extrato = []
                dados_relatorio = []

                #Filtro para verificar a quantidade de titulares ativos na empresa
                for titular in listaTitulares:
                    titular_id = titular['id']
                    titular_firstName = titular['firstName']
                    titular_cpf = titular['cpf']
                    titular_startValidity = titular['startValidity']
                    titular_studentAgreement_value = titular['studentAgreement'][0]['value']
                    # Colocar laço de repetição para verificar se há contrato ativo...
                    titular_studentAgreement_type = titular['studentAgreement'][0]['type']
                    titular_companyCNPJ = titular['company']['cnpj']
                    titular_status = titular['status']

                    # Comparar CNPJ da empresa atual com o da empresa do titular atual
                    if titular_companyCNPJ == empresa_cnpj:
                        if titular_status == True and titular_studentAgreement_type == "F":
                            contagem_titulares_empresa += 1

                            total_dependentes_titular = 0
                            
                            valor_pro_rata_titular = 0.0 #Contador float

                            for dependente_titular in titular['dependents']:
                                dependente_titular_status = dependente_titular['status']
                                dependente_titular_firstName = dependente_titular['firstName']
                                dependente_titular_cpf = dependente_titular['cpf']

                                if dependente_titular_status == True:
                                    total_dependentes_titular += 1 
                                    print(f"O {titular_firstName} tem {total_dependentes_titular} dependentes")

                                for dependente in listaDependentes:
                                    dependente_status = dependente['status']
                                    dependente_firstName = dependente['firstName']
                                    dependente_cpf = dependente['cpf']
                                    dependente_startValidity = dependente['startValidity']
                                    dependente_dependentAgreement_value = dependente['dependentAgreement'][0]['value']
                                    dependente_studentAgreement_type = dependente['dependentAgreement'][0]['type']

                                    entrada_titular = datetime.strptime(titular_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-10-01
                                    entrada_titular_date = entrada_titular.date() #Entrada de aluno em Data 01/10/2023

                                    entrada_dependente = datetime.strptime(dependente_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-10-01
                                    entrada_dependente_date = entrada_dependente.date() #Entrada de aluno em Data 01/10/2023

                                    # Dados Extrato
                                    cabecalhos_extrato = ["Nome do Aluno", "Parentesco", "CPF", "Pró rata", "Valor", "Valor Total"] # Cabeçalhos das colunas
                                    # cabecalhos_relatorio = ["Referência", "Quantidade", "Valor"]# Cabeçalhos das colunas

                                    for dependente_titular in titular['dependents']:
                                        if dependente_titular_status == True and dependente_studentAgreement_type == "F":
                                            total_dependentes_titular += 1 

                                            for dependente in listaDependentes:
                                                if dependente_cpf == dependente_titular_cpf:
                                                    
                                                    #EXTRATO 03/10/2023 < 01/10/2023
                                                    if emissao_menos_mes < entrada_titular_date: 
                                                        
                                                        dias_pro_rata_titular = (data_emissao_date - entrada_titular_date).days
                                                        print(f"O {titular_firstName} tem {dias_pro_rata_titular} dias pro rata")

                                                        #TITULARES VALORES PRO RATA
                                                        valor_pro_rata_titular = dias_pro_rata_titular * valor_por_dia     
                                                        contador_titulares_prorata += 1
                                                        contador_titulares += 1
                                                    
                                                        valor_total_titular = valor_pro_rata_titular + float(titular_studentAgreement_value)

                                                        valor_referencia = titular_studentAgreement_value * contador_titulares_prorata

                                                        soma_valores_prorata_titulares += valor_pro_rata_titular
                                                        soma_mensalidade_titular += float(titular_studentAgreement_value)

                                                        total_coluna_titular = soma_valores_prorata_titulares + soma_mensalidade_titular

                                                        soma_valor_total_titular += valor_total_titular

                                                        soma_mensalidade_total_titular = contador_titulares * float(titular_studentAgreement_value)
                                                        
                                                        if emissao_menos_mes < entrada_titular_date:
                                                    
                                                            #DEPENDENTES VALORES PRO RATA
                                                            dias_pro_rata_dependente = (data_emissao_date - entrada_titular_date).days
                                                            valor_pro_rata_dependente = dias_pro_rata_dependente * valor_por_dia     
                                                            contador_dependentes_prorata += 1
                                                            contador_dependentes += 1
                                                        
                                                            valor_total_dependente = valor_pro_rata_dependente + float(dependente_dependentAgreement_value)

                                                            valor_referencia = titular_studentAgreement_value * contador_dependentes_prorata

                                                            soma_valor_total_dependente += valor_pro_rata_dependente
                                                            soma_mensalidade_dependente += float(dependente_dependentAgreement_value)

                                                            total_coluna_dependente = soma_valores_prorata_titulares + soma_mensalidade_titular

                                                            soma_valor_total_dependente += valor_total_dependente

                                                            soma_mensalidade_total_dependente = contador_dependentes * float(dependente_dependentAgreement_value)

                                                            # Adiciona os dados do titular à lista
                                                            dados_extrato.append([titular_firstName, "TITULAR", titular_cpf, valor_pro_rata_titular, titular_studentAgreement_value, valor_total_titular])
                                                            dados_extrato.append([dependente_firstName, "DEPENDENTE", titular_cpf, valor_pro_rata_dependente, dependente_dependentAgreement_value, valor_total_dependente])
                                                            dados_relatorio.append(["Pró rata - Titulares", contador_titulares_prorata, soma_valor_total_titular])
                                                            dados_relatorio.append(["Pró rata - Dependente", contador_dependentes_prorata, soma_valor_total_dependente])

                                                        else:
                                                            print(f"O {titular_firstName} não tem pró rata.")
                                                            #TITULAR
                                                            valor_total_titular = 0
                                                            valor_pro_rata_titular = 0
                                                            contador_titulares += 1
                                                            soma_mensalidade_total_titular = contador_titulares * float(titular_studentAgreement_value)
                                                            soma_valor_total_titular += valor_total_titular

                                                            #DEPENDENTE
                                                            valor_total_dependente = 0
                                                            valor_pro_rata_dependente = 0
                                                            contador_dependentes += 1
                                                            soma_mensalidade_total_dependente = contador_dependentes * float(dependente_dependentAgreement_value)
                                                            soma_valor_total_dependente += valor_total_dependente

                                                        soma_total = float(soma_mensalidade_total_dependente) + float(soma_valor_total_titular) + float(soma_mensalidade_total_dependente) + float(soma_valor_total_dependente)
                                                        # Adiciona os dados do titular à lista
                                                        dados_extrato.append([titular_firstName, "TITULAR", titular_cpf, valor_pro_rata_titular, titular_studentAgreement_value, valor_total_titular])
                                                        dados_extrato.append([dependente_firstName, "DEPENDENTE", titular_cpf, valor_pro_rata_dependente, dependente_dependentAgreement_value, valor_total_dependente])

                            

                                        # dados_extrato.append([dependente_firstName, "DEPENDENTE", titular_cpf, valor_pro_rata_titular, titular_studentAgreement_value, valor_total_titular])
                
                # soma_total = float(soma_mensalidade_total_titular) + float(soma_valor_total_titular)
                # dados_relatorio.append(["Mensalidade -  Titulares", contador_titulares, soma_mensalidade_total_titular])
                # dados_relatorio.append(["Mensalidade -  Dependentes", contador_dependentes, soma_mensalidade_total])
                # dados_relatorio.append(["TOTAL", "", soma_total])


                # Imprime a tabela
                print(tabulate(dados_extrato, headers=cabecalhos_extrato, tablefmt="grid"))
                # print(tabulate(dados_relatorio, headers=cabecalhos_relatorio, tablefmt="grid"))

                relacao_ativos = (contagem_titulares_empresa + contagem_dependentes_empresa) * empresa_companyAgreements_value


            else:
                print(f"A empresa {empresa_tradeName}, não tem a data corte igual ao dia de hoje")

                # Data de vencimento da cobrança
            calcular_data_vencimento # Data de vencimento (data corte + 10)
        else:
            print(f"A empresa {empresa_tradeName}, não está ativa")
    print("")

else:
    print(f"Erro na requisição. Código de Status: {respostaAllCompany.status_code}")