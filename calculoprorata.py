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

def calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia):
    dias_pro_rata = (data_emissao_date - entrada_aluno_date).days  # dias pro rata é igual a data de emissão menos a entrada do titular
    valor_pro_rata = dias_pro_rata * valor_por_dia  # Valor prorata é igual ao dias pro rata vezes o valor por dia
    return dias_pro_rata, valor_pro_rata

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

        # Lógica para filtrar apenas as empresas ativas
        if empresa_companyStatus == "EM IMPLANTACAO":
            # print(f"CNPJ: {empresa_cnpj}    Nome: {empresa_tradeName}   Data corte:{empresa_cutoffDate}") 
            contagem_empresas_implantacao += 1
            
            # Filtro das empresas que tem a data corte igual ao dia atual
            if dia_emissao_teste == empresa_cutoffDate:
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
                    
                    entrada_titular = datetime.strptime(titular_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-10-01
                    entrada_titular_date = entrada_titular.date() #Entrada de aluno em Data 01/10/2023

                    valor_pro_rata = 0.0 #Contador float


                    # Dados Extrato
                    cabecalhos_extrato = ["Nome do Aluno", "Parentesco", "CPF", "Pró rata", "Valor", "Valor Total"] # Cabeçalhos das colunas
                    cabecalhos_relatorio = ["Referência", "Quantidade", "Valor"]# Cabeçalhos das colunas

                    # Comparar CNPJ da empresa atual com o da empresa do titular atual
                    if titular_companyCNPJ == empresa_cnpj:
                        if titular_status == True and titular_studentAgreement_type == "F":
                            executado = False
                            for dependente_Agreement in listaDependentes:
                                dependente_Agreement_all = dependente_Agreement['dependentAgreement']
                            for dependente_value in dependente_Agreement_all:
                                dependente_agreement_value = dependente_value['value']
                                for dependente in titular['dependents']:
                                    dependente_status = dependente['status']
                                    dependente_firstName = dependente['firstName']
                                    dependente_cpf = dependente['cpf']
                                    dependente_startValidity = dependente['startValidity']

                                    if dependente_status == True:
                                        entrada_dependente = datetime.strptime(dependente_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-10-01
                                        entrada_dependente_date = entrada_dependente.date() #Entrada de aluno em Data 01/10/2023
                                        valor_pro_rata_dependente = 0.0 #Contador float

                                        #EXTRATO 03/10/2023 < 01/10/2023
                                        if emissao_menos_mes < entrada_titular_date:
                                            if executado == False:
                                                #Calculo extrato titulares
                                                dias_pro_rata = (data_emissao_date - entrada_titular_date).days
                                                valor_pro_rata = dias_pro_rata * valor_por_dia
                                                valor_total_titular = valor_pro_rata + float(titular_studentAgreement_value)
                                                print(f"O titular {titular_firstName} deve pagar {valor_total_titular}")
                                                executado = True

                                            #Calculo extrato dependentes
                                            dias_pro_rata_dependente = (data_emissao_date - entrada_dependente_date).days
                                            valor_pro_rata_dependente = dias_pro_rata_dependente * valor_por_dia
                                            valor_total_dependente = valor_pro_rata_dependente + float(dependente_agreement_value)
                                            print(f"O dependente {dependente_firstName} deve pagar {valor_total_dependente}")
            else:
                print(f"A empresa {empresa_tradeName}, não tem a data corte igual ao dia de hoje")

                # Data de vencimento da cobrança
            calcular_data_vencimento # Data de vencimento (data corte + 10)
        else:
            print(f"A empresa {empresa_tradeName}, não está ativa")
    print("")
else:

    print(f"Erro na requisição. Código de Status: {respostaAllCompany.status_code}")