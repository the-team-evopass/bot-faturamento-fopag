import requests
from datetime import datetime, timedelta
from datavencimento import calcular_data_vencimento

# URLs DAS APIs
urlAllCompany = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements'
urlAllStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student?expand=dependents%2CstudentContact%2CstudentAgreement%2CstudentAddress%2Ccompany'
urlAgreementStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student_agreement'
urlAllDependent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/dependent/'
urlAgreementDependent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/dependent_agreement'

#Obter a data atual
dia_emissao_teste = 2 #teste com 18
data_atual = datetime.now()

print(f"Testando como se o dia autal fosse {dia_emissao_teste}")
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

                contador_titulares = 0

                #Filtro para verificar a quantidade de titulares ativos na empresa
                for titular in listaTitulares:
                        titular_firstName = titular['firstName']
                        titular_cpf = titular['cpf']
                        titular_startValidity = titular['startValidity']
                        titular_studentAgreement_value = titular['studentAgreement'][0]['value']
                        
                        # Colocar laço de repetição para verificar se há contrato ativo...

                        titular_studentAgreement_type = titular['studentAgreement'][0]['type']
                        titular_companyCNPJ = titular['company']['cnpj']
                        titular_status = titular['status']

                        if titular_companyCNPJ == empresa_cnpj: # Comparar CNPJ da empresa atual com o da empresa do titular atual
                            if titular_status == True and titular_studentAgreement_type == "F":
                                contagem_titulares_empresa += 1

                                data_emissao = datetime(data_atual.year, data_atual.month, empresa_cutoffDate) #Data Emissão do Boleto | 2023-10-30
                                entrada_aluno = datetime.strptime(titular_startValidity, '%Y-%m-%d') #Data que o aluno iniciou na empresa | 2023-10-01
                                data_emissao_date = data_emissao.date() #Emissão em Data
                                entrada_aluno_date = entrada_aluno.date() #Entrada de aluno em Data

                                valor_por_dia=2.663 #valor cobrado por dia
                                data_corte = empresa_cutoffDate # Data Corte
                                emissao_menos_mes = data_emissao_date - timedelta(days=30) #Emissão de boleto - 30 dias
                                valor_pro_rata = 0.0 #Contador float
                                
                                #EXTRATO
                                if emissao_menos_mes < entrada_aluno_date: 
                                    dias_pro_rata = (data_emissao - entrada_aluno).days
                                    valor_pro_rata = dias_pro_rata * valor_por_dia                                                                                                                    
                                else:
                                    print("A data de emissão não está dentro do período pró-rata.")
                                
                                valor_total = valor_pro_rata + float(titular_studentAgreement_value)   

                                print(f"Nome do Aluno: {titular_firstName}, Parentesco: TITULAR, CPF: {titular_cpf}, Pró rata: {valor_pro_rata}, Valor: {titular_studentAgreement_value}, Valor Total: {valor_total}")
                                contador_titulares += 1

                                valor_referencia = titular_studentAgreement_value * contador_titulares

                                #REFERÊNCIA
                                print('')
                                print(f"Pró rata - Titulares, Quantidade: {contador_titulares}, valor: {valor_referencia}")
                                print('')


                            #Filtro para verificar a quantidade de dependentes ativos na empresa 
                            # for dependente in listaDependentes:
                            #     dependente_companyCNPJ = dependente['company']['cnpj']
                            #     if dependente_companyCNPJ == empresa_cnpj:
                            #         dependente_status = dependente['status']
                            #         dependente_dependentAgreement_type = dependente['dependentAgreement']['type']

                            #         if dependente_status == "true" and dependente_dependentAgreement_type == "F":
                            #             contagem_dependentes_empresa += 1

                            # Calcula a relação de ativos das empresas
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
