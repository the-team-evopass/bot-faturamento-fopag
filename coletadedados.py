import requests
from datetime import datetime
from datavencimento import calcular_data_vencimento

# URLs DAS APIs
urlAllCompany = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements'
urlAllStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student?expand=dependents%2CstudentContact%2CstudentAgreement%2CstudentAddress'
urlAgreementStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student_agreement'
urlAllDependent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/dependent/'
urlAgreementDependent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/dependent_agreement'

#Obter a data atual
# dia_atual = datetime.now().day
dia_atual = 30

print(dia_atual)

# Listagem de Empresas e a data corte
respostaAllCompany = requests.get(urlAllCompany)
respostaAllStudents = requests.get(urlAllStudent)
if respostaAllCompany.status_code == 200 and respostaAllStudents.status_code == 200:
    companyJson = respostaAllCompany.json()
    listaEmpresas = companyJson['data']

    studentJson = respostaAllStudents.json()
    listaFuncionarios = studentJson['data']

    print("Lista de Empresas em Implantação:")
    contagem_empresas_implantacao = 0

    # Loop para coletar dados das empresas
    for empresa in listaEmpresas:
        empresa_cnpj = empresa['cnpj']
        empresa_tradeName = empresa['tradeName']
        empresa_companyStatus = empresa['companyStatus']
        empresa_cutoffDate = empresa['cutoffDate']
        empresa_companyAgreements_value = empresa['companyAgreements']['value']

        # Lógica para filtrar apenas as empresas que estão em implantação
        if empresa_companyStatus == "EM IMPLANTACAO":
            #print(f"CNPJ: {empresa_cnpj}    Nome: {empresa_tradeName}   Data corte:{empresa_cutoffDate}") 
            contagem_empresas_implantacao += 1
            
            #Filtro das empresas que tem a data corte igual ao dia atual
            if dia_atual == empresa_cutoffDate:
                print(f"A empresa {empresa_tradeName} tem a data corte igual a data atual.")

                #Filtro para verificar a quantidade de funcionarios ativos na empresa
                for funcionario in listaFuncionarios:
                    funcionario_id = funcionario['id']
                    funcionario_status = funcionario['status']
                    funcionario_companyCNPJ = funcionario['company']['cnpj']
                    funcionario_studentAgreement_type = funcionario['studentAgreement']['type']
                    contagem_funcionarios_empresa = 0

                    if funcionario_status == "true" and funcionario_studentAgreement_type == "F":
                        contagem_funcionarios_empresa += 1
                    else:
                        print("Sem funcionários Fopag ativos")

                    #Calcula a relação de ativos das empresas
                    relacao_ativos = contagem_funcionarios_empresa * empresa_companyAgreements_value

                    #Data de vencimento da cobrança
                    calcular_data_vencimento #data de vencimento (data corte + 10)

            
                    
                
    print("")

else:
    print(f"Erro na requisição. Código de Status: {respostaAllCompany.status_code}")


# # Listagem de funcionários Ativos por empresa
# respostaAllStudents = requests.get(urlAllStudent)
# respostaAgreementStudents = requests.get(urlAgreementStudent)

# if respostaAllStudents.status_code == 200:
#     allStudents = respostaAllStudents.json()

#     # Dict para armazenar a contagem de funcionários por empresa
#     contagem_por_empresa = {}

#     for student in allStudents:
#         status = student['status']
#         status = student['status']
#         funcionario_id = student['id']
#         empresa_id = student['id']

#         if status == "Ativo":
#             nome_empresa = next((empresa['tradeName'] for empresa in listaEmpresas if empresa['id'] == empresa_id), None)

#             if nome_empresa:
#                 # Atualizar a contagem para a empresa correspondente
#                 contagem_por_empresa[nome_empresa] = contagem_por_empresa.get(nome_empresa, 0) + 1

#     print("\nQuantidade de funcionários Ativo por empresa em implantação:")
#     if contagem_por_empresa:
#         for empresa, contagem in contagem_por_empresa.items():
#             print(f"{empresa}: {contagem} funcionário(s)")
#     else:
#         print("Nenhum funcionário Ativo encontrado nas empresas em implantação.")

# else:
#     print(f"Erro na requisição. Código de Status: {respostaAllStudents.status_code}, {respostaAllStudents.status_code}")


# # Listagem de dependentes Ativos por empresa
# respostaAllDependents = requests.get(urlAllDependent)
# respostaAgreementDependent = requests.get(urlAgreementDependent)

# if respostaAllDependents.status_code == 200:
#     allDependents = respostaAllDependents.json()

#     # Dict para armazenar a contagem de funcionários por empresa
#     contagem_por_empresa = {}

#     for dependent in allDependents:
#         statusReason = dependent['statusReason']
#         status = dependent['status']
#         dependente_id = dependent['id']
#         empresa_id = dependent['id']

#         if statusReason == "Ativo":
#             nome_empresa = next((empresa['tradeName'] for empresa in listaEmpresas if empresa['id'] == empresa_id), None)

#             if nome_empresa:
#                 # Atualizar a contagem para a empresa correspondente
#                 contagem_por_empresa[nome_empresa] = contagem_por_empresa.get(nome_empresa, 0) + 1

#     print("\nQuantidade de dependentes Ativo por empresa em implantação:")
#     if contagem_por_empresa:
#         for empresa, contagem in contagem_por_empresa.items():
#             print(f"{empresa}: {contagem} dependente(s)")
#     else:
#         print("Nenhum dependente Ativo encontrado nas empresas em implantação.")

# else:
#     print(f"Erro na requisição. Código de Status: {respostaAllDependents.status_code}, {respostaAllDependents.status_code}")

