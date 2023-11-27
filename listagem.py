import requests

# URLs DAS APIs
urlAllCompany = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements'
urlAllStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student?expand=dependents%2CstudentContact%2CstudentAgreement%2CstudentAddress'
urlAgreementStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student_agreement'

# Listagem de Empresas
respostaAllCompany = requests.get(urlAllCompany)
if respostaAllCompany.status_code == 200:
    companyJson = respostaAllCompany.json()
    listaEmpresas = companyJson['data']
    print("Lista de Empresas em Implantação:")
    contagem_empresas_implantacao = 0

    # Loop para coletar dados das empresas
    for empresa in listaEmpresas:
        empresa_cnpj = empresa['cnpj']
        empresa_tradeName = empresa['tradeName']
        empresa_companyStatus = empresa['companyStatus']

        # Lógica para filtrar apenas as empresas que estão em implantação
        if empresa_companyStatus == "EM IMPLANTACAO":
            print(f"CNPJ: {empresa_cnpj}    Nome: {empresa_tradeName}")
            contagem_empresas_implantacao += 1

    print("")
    print(f"Total de empresas em implantação: {contagem_empresas_implantacao}")

else:
    print(f"Erro na requisição. Código de Status: {respostaAllCompany.status_code}")

# Listagem de funcionários Ativos por empresa
respostaAllStudents = requests.get(urlAllStudent)
respostaAgreementStudents = requests.get(urlAgreementStudent)

if respostaAllStudents.status_code == 200:
    allStudents = respostaAllStudents.json()

    # Dict para armazenar a contagem de funcionários por empresa
    contagem_por_empresa = {}

    for student in allStudents:
        statusReason = student['statusReason']
        status = student['status']
        funcionario_id = student['id']
        empresa_id = student['id']
        student_status = student['status']

        if statusReason == "Ativo":
            nome_empresa = next((empresa['tradeName'] for empresa in listaEmpresas if empresa['id'] == empresa_id), None)

            if nome_empresa:
                
                # Atualizar a contagem para a empresa correspondente
                contagem_por_empresa[nome_empresa] = contagem_por_empresa.get(nome_empresa, 0) + 1

    print("\nQuantidade de funcionários Ativo por empresa em implantação:")
    if contagem_por_empresa:
        for empresa, contagem in contagem_por_empresa.items():
            print(f"{empresa}: {contagem} funcionário(s)")
    else:
        print("Nenhum funcionário Ativo encontrado nas empresas em implantação.")

else:
    print(f"Erro na requisição. Código de Status: {respostaAllStudents.status_code}, {respostaAgreementStudents.status_code}")
