import requests
from datetime import datetime, timedelta
from tabulate import tabulate
from datavencimento import calcular_data_vencimento

# URLs DAS APIs
urlAllCompany = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements'
urlAllStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student?expand=dependents%2CstudentContact%2CstudentAgreement%2CstudentAddress%2Ccompany'
urlAgreementStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student_agreement'
urlAllDependent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/dependent?expand=dependentAgreement'
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

        # Lógica para filtrar apenas as empresas ativas
        if empresa_companyStatus == "EM IMPLANTACAO":
            # print(f"CNPJ: {empresa_cnpj}    Nome: {empresa_tradeName}   Data corte:{empresa_cutoffDate}") 
            contagem_empresas_implantacao += 1
            
            # Filtro das empresas que tem a data corte igual ao dia atual
            if dia_emissao_teste == empresa_cutoffDate:
                print(f"Relação de ativos da empresa {empresa_tradeName} .")

                contador_titulares_prorata = 0
                contador_titulares = 0

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

                    

                    soma_valores_prorata = 0
                    soma_mensalidade_titular = 0
                    soma_valor_total = 0
                    soma_mensalidade_total = 0
                    
                    entrada_aluno = datetime.strptime(titular_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-10-01
                    entrada_aluno_date = entrada_aluno.date() #Entrada de aluno em Data 01/10/2023

                    valor_pro_rata = 0.0 #Contador float

                    # Dados Extrato
                    cabecalhos_extrato = ["Nome do Aluno", "Parentesco", "CPF", "Pró rata", "Valor", "Valor Total"] # Cabeçalhos das colunas
                    cabecalhos_relatorio = ["Referência", "Quantidade", "Valor"]# Cabeçalhos das colunas

                    # Comparar CNPJ da empresa atual com o da empresa do titular atual
                    if titular_companyCNPJ == empresa_cnpj:
                        if titular_status == True and titular_studentAgreement_type == "F":
                            contagem_titulares_empresa += 1

                            total_dependentes_titular = 0

                            for dependente in titular['dependents']:
                                dependente_status = dependente['status']
                                dependente_firstName = dependente['firstName']
                                dependente_cpf = dependente['cpf']

                                if dependente_status == True:
                                    total_dependentes_titular += 1 
                            
                            print(f"O {titular_firstName} tem {total_dependentes_titular} dependentes")
                            
                            #EXTRATO 03/10/2023 < 01/10/2023
                            if emissao_menos_mes < entrada_aluno_date: 
                                dias_pro_rata_negativo = (data_emissao_date - entrada_aluno_date).days
                                dias_pro_rata = dias_pro_rata_negativo # X -1

                                print(f"O {titular_firstName} tem {dias_pro_rata} dias pro rata")
                                valor_pro_rata = dias_pro_rata * valor_por_dia     
                                contador_titulares_prorata += 1
                                contador_titulares += 1
                            
                                valor_total = valor_pro_rata + float(titular_studentAgreement_value)

                                valor_referencia = titular_studentAgreement_value * contador_titulares_prorata

                                soma_valores_prorata += valor_pro_rata
                                soma_mensalidade_titular += float(titular_studentAgreement_value)

                                total_coluna = soma_valores_prorata + soma_mensalidade_titular

                                soma_valor_total += valor_total

                                soma_mensalidade_total = contador_titulares * float(titular_studentAgreement_value)

                                # Adiciona os dados do titular à lista
                                dados_extrato.append([titular_firstName, "TITULAR", titular_cpf, valor_pro_rata, titular_studentAgreement_value, valor_total])
                                dados_relatorio.append(["Pró rata - Titulares", contador_titulares_prorata, soma_valor_total])

                            else:
                                print(f"O {titular_firstName} não tem pró rata.")
                                valor_total = 0
                                valor_pro_rata = 0
                                contador_titulares += 1
                                soma_mensalidade_total = contador_titulares * float(titular_studentAgreement_value)
                                soma_valor_total += valor_total

                                soma_total = float(soma_mensalidade_total) + float(soma_valor_total)
                                # Adiciona os dados do titular à lista
                                dados_extrato.append([titular_firstName, "TITULAR", titular_cpf, valor_pro_rata, titular_studentAgreement_value, valor_total])
                
                soma_total = float(soma_mensalidade_total) + float(soma_valor_total)
                dados_relatorio.append(["Mensalidade -  Titulares", contador_titulares, soma_mensalidade_total])
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

else:
    print(f"Erro na requisição. Código de Status: {respostaAllCompany.status_code}")
