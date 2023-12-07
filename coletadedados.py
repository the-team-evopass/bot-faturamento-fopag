import requests

# URLs DAS APIs
urlAllCompany = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements'
urlAllStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student?expand=dependents%2CstudentContact%2CstudentAgreement%2CstudentAddress%2Ccompany'
urlAllDependent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/dependent?expand=dependentAgreement'

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
    # Contador de titulares e dependentes
    contagem_titulares_empresa = 0
    contagem_dependentes_empresa = 0

    # Loop para coletar dados das empresas
    for empresa in listaEmpresas:
        empresa_cnpj = empresa['cnpj']  # Cnpj da empresa
        empresa_tradeName = empresa['tradeName']  # Nome da empresa
        empresa_companyStatus = empresa['companyStatus']  # Status da empresa
        empresa_cutoffDate = empresa['cutoffDate']  # Data corte
        empresa_companyAgreements_value = empresa['companyAgreements']  # Valor que a empresa paga
        for valor in empresa_companyAgreements_value:
            empresa_value = valor['value']
        print(f"Empresa: {empresa_tradeName}")

    # Loop para coletar dados dos Titulares
    for titular in listaTitulares:
        titular_firstName = titular['firstName']
        titular_status = titular['status']
        titular_startValidity = titular['startValidity']
        titular_cpf = titular['cpf']
        titular_dependents = titular['dependents']
        titular_company = titular['company']
        for companhia_titular in titular_company:
            nome_empresa_titular = titular_company['tradeName']

        print(f"O titular {titular_firstName} pertence a empresa {nome_empresa_titular}")

        # Loop para coletar dados dos Dependentes dos titulares
        for dependente in titular_dependents:
            dependente_firstName = dependente['firstName']
            dependente_status = dependente['status']
            dependente_startValidity = dependente['startValidity']
            dependente_cpf = dependente['cpf']
            contagem_dependentes_empresa += 1 
            print(f"O dependente: {dependente_firstName} pertence ao titular {titular_firstName}")    

else:
    print(f"Erro na requisição. Código de Status: {respostaAllCompany.status_code}")
