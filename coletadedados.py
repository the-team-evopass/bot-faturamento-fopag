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
respostaAllDependent = requests.get(urlAllDependent)

if respostaAllCompany.status_code == 200 and respostaAllStudents.status_code == 200 and respostaAllDependent == 200:
    companyJson = respostaAllCompany.json()
    listaEmpresas = companyJson['data']

    studentJson = respostaAllStudents.json()
    listaTitulares = studentJson['data']

    dependentJson = respostaAllDependent.json()
    listaDependentes = dependentJson['data']

    # Contador de empresas
    contagem_empresas_implantacao = 0

    # Loop para coletar dados das empresas
    for empresa in listaEmpresas:
        empresa_cnpj = empresa['cnpj'] # Cnpj da empresa
        empresa_tradeName = empresa['tradeName'] # Nome da empresa
        empresa_companyStatus = empresa['companyStatus'] # Status da empresa
        empresa_cutoffDate = empresa['cutoffDate'] # Data corte
        empresa_companyAgreements_value = empresa['companyAgreements']['value'] #Valor que a empresa paga

        # Contador de titulares e dependentes
        contagem_titulares_empresa = 0
        contagem_dependentes_empresa = 0

        # Lógica para filtrar apenas as empresas ativas
        if empresa_companyStatus == "Ativo":
            # print(f"CNPJ: {empresa_cnpj}    Nome: {empresa_tradeName}   Data corte:{empresa_cutoffDate}") 
            contagem_empresas_implantacao += 1
            
            # Filtro das empresas que tem a data corte igual ao dia atual
            if dia_atual == empresa_cutoffDate:
                print(f"A empresa {empresa_tradeName} tem a data corte igual a data atual.")

                #Filtro para verificar a quantidade de titulares ativos na empresa
                for titular in listaTitulares:
                    titular_companyCNPJ = titular['company']['cnpj']
                    if titular_companyCNPJ == empresa_cnpj:
                        titular_status = titular['status']
                        titular_studentAgreement_type = titular['studentAgreement']['type']

                        if titular_status == "true" and titular_studentAgreement_type == "F":
                            contagem_titulares_empresa += 1
                        


                        for dependente in listaDependentes:
                            dependente_companyCNPJ = dependente['company']['cnpj']
                            if dependente_companyCNPJ == empresa_cnpj:
                                dependente_status = dependente['status']
                                dependente_dependentAgreement_type = dependente['dependentAgreement']['type']

                                if dependente_status == "true" and dependente_dependentAgreement_type == "F":
                                    contagem_dependentes_empresa += 1

                        # Calcula a relação de ativos das empresas
                        relacao_ativos = (contagem_titulares_empresa + contagem_dependentes_empresa) * empresa_companyAgreements_value

                

                # Data de vencimento da cobrança
                calcular_data_vencimento # Data de vencimento (data corte + 10)

            
                    
                
    print("")

else:
    print(f"Erro na requisição. Código de Status: {respostaAllCompany.status_code}")
