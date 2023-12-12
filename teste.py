import requests

# URLs DAS APIs
urlAllCompany = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements'
urlAllStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student?expand=dependents%2CstudentContact%2CstudentAgreement%2CstudentAddress%2Ccompany'
urlAllDependent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/dependent?expand=student%2CdependentContact%2CdependentAgreement%2CdependentAddress'

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
    contagem_empresas = 0
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
        if empresa_companyStatus == "EM IMPLANTACAO":
            for valor in empresa_companyAgreements_value:
                empresa_value = valor['value']
            contagem_value_titular = 0
            contagem_value_dependente = 0
            contagem_empresas += 1

            # Loop para coletar dados dos Titulares
            for titular in listaTitulares:
                titular_firstName = titular['firstName']
                titular_status = titular['status']
                titular_startValidity = titular['startValidity']
                titular_cpf = titular['cpf']
                titular_agreement = titular['studentAgreement']
                titular_company = titular['company']
                if titular_status == True:
                    for companhia_titular in titular_company:
                        nome_empresa_titular = titular_company['tradeName']
                    for titular_agreement_value in titular_agreement:
                        titular_value = titular_agreement_value['value']
                    contagem_value_titular += float(titular_value)
                    
                    # Loop para coletar dados dos Dependentes dos titulares
                    for dependente in listaDependentes:
                        dependente_firstName = dependente['firstName']
                        dependente_status = dependente['status']
                        dependente_startValidity = dependente['startValidity']
                        dependente_cpf = dependente['cpf']
                        dependente_agreement = dependente['dependentAgreement']
                        dependente_student = dependente['student']['cpf']
                        if dependente_status == True:
                            contagem_dependentes_empresa += 1
                            for dependente_agreement_value in dependente_agreement:
                                dependente_value = dependente_agreement_value['value']
                                if dependente_student == titular_cpf:
                                    contagem_value_dependente += 1
                                    contagem_value_dependente += float(dependente_value)
                        else:
                            print(f"O dependente {dependente_firstName}, não está ATIVO")

                    print(f"A empresa {empresa_tradeName} pagará {empresa_value} por valor de vida, {contagem_value_titular} por titular e {contagem_value_dependente} por dependente.")
                    valor_total_empresa = float(empresa_value) + float(contagem_value_titular) + float(contagem_value_dependente)
                    print(valor_total_empresa)

                    

                else:
                    print(f"O titular {titular_firstName}, não está ATIVO")

            print(contagem_empresas)

        else:
            print(f"A empresa {empresa_tradeName}, não está em IMPLANTACAO")

else:
    print(f"Erro na requisição. Código de Status: {respostaAllCompany.status_code}")
