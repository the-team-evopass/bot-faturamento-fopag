import requests
from datetime import datetime, timedelta
from tabulate import tabulate
from datavencimento import calcular_data_vencimento

# URLs DAS APIs
urlAllCompany = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements'
urlAllStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student?expand=dependents%2CstudentContact%2CstudentAgreement%2CstudentAddress%2Ccompany'
urlAgreementStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student_agreement'
urlAllDependent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/dependent'
urlAgreementDependent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/dependent_agreement'

#Obter a data atual
dia_emissao_teste = 2 #teste com 18
data_atual = datetime.now()

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
        empresa_companyAgreements_value = empresa['companyAgreements'],['value'] #Valor que a empresa paga

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

                #Filtro para verificar quem são os Ativos
                for ativos in listaTitulares + listaDependentes:
                    ativos_id = ativos['id']
                    ativos_status = ativos['status']
                    ativos_firstName = ativos['firstName']
                    ativos_cpf = ativos['cpf']
                    if ativos_status == True:
                        ativos_firstName
                    else:
                        print("Sem ativos")

                #Filtro para listagem completa
                for titular in listaTitulares:
                    titular_firstName = titular['firstName']
                    print(f"Títular: {titular_firstName}")

                for dependente in listaDependentes:
                    dependente_firstName = dependente['firstName']
                    print(f"Dependente: {dependente_firstName}")

                #Titular/dependente
                for ativos in listaTitulares + listaDependentes:
                    ativos_id = ativos['id']
                    ativos_status = ativos['status']
                    ativos_firstName = ativos['firstName']
                    ativos_cpf = ativos['cpf']
                    if ativos_status == True:
                        ativos_firstName
                    else:
                        print("Sem ativos")

        else:
            print(f"A empresa {empresa_tradeName}, não está ativa")
    print("")

else:
    print(f"Erro na requisição. Código de Status: {respostaAllCompany.status_code}")
