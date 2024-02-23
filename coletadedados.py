from calendar import month
import json
from os import replace
from termcolor import colored
from functions.calculation.calculoprorata import calcular_prorata
from functions.calculation.datavencimento import calcular_data_vencimento
from datetime import datetime, timedelta
from functions.calculation.porcentagem import Abatimento_Imposto
from functions.generateInvoicing import GenerateInvoicing
from middleware import runGetAllDependents, runGetAllEconomicsGroups, runGetAllHolders
from functions.render import render_html
from functions.sendemail import send_email

from middleware import runGetAllCompanies

def FaturarEmpresas(dia_emissao, data_atual):
    dados_extrato = []
    dados_relatorio = []
    
    listaGruposEconomicos = runGetAllEconomicsGroups()
    respostaAllCompany = runGetAllCompanies()
    listaEmpresas = respostaAllCompany['data']
    listaTitulares = runGetAllHolders()
    listaDependentes = runGetAllDependents()

    # Contador de empresas
    contador_empresas = 0

    # Grupos Economicos
    for grupo in listaGruposEconomicos:
        grupo_cnpj = grupo['cnpj']
        grupo_billingType = grupo['billingType']
        grupo_companies = grupo['companies']

        boleto_grupo = 0
        contador_empresas_grupo = 0

        if grupo_billingType == "UNIFICADO":
            dados_extrato = []
            dados_relatorio = []    

        qnt_empresas = len(grupo_companies)

        for empresa in grupo_companies:
            cnpj_empresa_grupo = empresa['cnpj']

            for empresa in listaEmpresas:
                empresa_id = empresa['id']
                empresa_cnpj = empresa['cnpj']  # Cnpj da empresa
                empresa_tradeName = empresa['tradeName']  # Nome da empresa
                empresa_companyStatus = empresa['companyStatus']  # Status da empresa
                empresa_cutoffDate = empresa['cutoffDate']  # Data corte
                empresa_students = empresa['students']
                empresa_agreement = empresa['companyAgreements']
                for agreements in empresa_agreement:
                    empresa_value = agreements['value']
                
                if grupo_billingType == "APARTADO":
                    dados_extrato = []
                    dados_relatorio = []

                if empresa_cnpj in cnpj_empresa_grupo:
                    if empresa_cnpj == grupo_cnpj:
                        id_temp = empresa_id
                        name_temp = empresa_tradeName
                        
                        
                    # Filtro das empresas que têm a data de corte igual ao dia atual
                    if empresa_companyStatus == "EM IMPLANTACAO" and dia_emissao == empresa_cutoffDate and empresa_id not in [2214, 2314, 2454, 2464 ]:
                        contagem_value_titular, contagem_value_dependente = 0, 0
                        contagem_value_titular_prorata, contagem_value_dependente_prorata = 0, 0
                        contador_titulares_empresa, contador_titulares_prorata = 0, 0

                        contador_empresas_grupo += 1
                        contador_empresas += 1
                        
                        print(colored(f"Faturamento da empresa {empresa_tradeName} - {grupo_billingType}.", 'blue'))
                        
                        data_atual = datetime.now()
                        data_emissao = datetime(data_atual.year, data_atual.month, empresa_cutoffDate)
                        data_emissao_date = data_emissao.date()
                        
                        emissao_menos_mes = (data_emissao_date.replace(year=data_emissao_date.year - 1, month=12) if data_emissao_date.month == 1 else data_emissao_date.replace(month=data_emissao_date.month - 1))

                        dias_adicionais = 10

                        # Data de vencimento da cobrança
                        data_vencimento = calcular_data_vencimento(empresa_cutoffDate, dias_adicionais)

                        competencia_mes_ano = data_emissao_date.strftime('%B de %Y')

                        contador_dependentes_prorata = 0
                        contador_dependentes_empresa = 0

                        # Loop para coletar dados dos Titulares
                        if empresa_students != []:
                            for titular in listaTitulares:
                                titular_firstName = titular['firstName'].upper()
                                titular_lastName = titular['lastName'].upper()
                                titular_status = titular['status']
                                titular_startValidity = titular['startValidity']
                                titular_cpf = titular['cpf']
                                titular_companyCNPJ = titular['company']['cnpj']
                                titular_studentAgreement_value = titular['studentAgreement'][-1]['value']
                                titular_studentAgreement_type = titular['studentAgreement'][-1]['type']

                                valor_por_dia = float(titular_studentAgreement_value) / float(30.0)  # valor cobrado por dia
                                    
                                if titular_status == True and titular_studentAgreement_type == "FOLHA DE PAGAMENTO":
                                    if titular_companyCNPJ == empresa_cnpj:
                                        entrada_titular = datetime.strptime(titular_startValidity, '%Y-%m-%dT%H:%M:%S.%fZ')
                                        entrada_aluno_date = entrada_titular.date()
                                                                                
                                        if emissao_menos_mes < entrada_aluno_date:
                                            valor_calculo_prorata = calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia)

                                            if valor_calculo_prorata > 0:
                                                titular_studentAgreement_value = 0

                                            valor_mensal_titular_prorata = float(valor_calculo_prorata)
                                            contador_titulares_prorata += 1
                                            
                                            dados_extrato.append({"name": titular_firstName + " " + titular_lastName,"relationship": "TITULAR","cpf": titular_cpf,"proRata": float(valor_calculo_prorata),
                                                    "value":  float(titular_studentAgreement_value),"totalValue": float(valor_mensal_titular_prorata)})
                                            
                                            contagem_value_titular_prorata += float(valor_mensal_titular_prorata)

                                        else:
                                            contador_titulares_empresa += 1
                                            
                                            valor_mensal_titular = titular_studentAgreement_value
                                            
                                            dados_extrato.append({"name": titular_firstName + " " + titular_lastName,"relationship": "TITULAR","cpf": titular_cpf,"proRata": 0,
                                                    "value":  float(titular_studentAgreement_value),"totalValue": float(valor_mensal_titular)})

                                            contagem_value_titular += float(valor_mensal_titular)
                                        
                                        # Loop para coletar dados dos Dependentes dos titulares
                                        for dependente in listaDependentes:
                                            dependente_firstName = dependente['firstName'].upper()
                                            dependente_lastName = dependente['lastName'].upper()
                                            dependente_status = dependente['status']
                                            dependente_startValidity = dependente['startValidity']
                                            dependente_student_cpf = dependente['student']['cpf']
                                            dependente_studentAgreement_value = dependente['dependentAgreement'][-1]['value']
                                            dependente_studentAgreement_type = dependente['dependentAgreement'][-1]['type']
                                            dependente_startValidity = dependente['startValidity']

                                            valor_por_dia = float(dependente_studentAgreement_value) / float(30.0)  # valor cobrado por dia

                                            if dependente_status == True and dependente_studentAgreement_type == "FOLHA DE PAGAMENTO":
                                                if dependente_student_cpf == titular_cpf:
                                                    entrada_dependente = datetime.strptime(dependente_startValidity, '%Y-%m-%dT%H:%M:%S.%fZ') #Data que o aluno iniciou na empresa | 2023-10-01
                                                    entrada_aluno_date = entrada_dependente.date() #Entrada de aluno em Data 01/10/2023
                                            
                                                    if emissao_menos_mes < entrada_aluno_date:
                                                        valor_calculo_prorata = calcular_prorata(data_emissao_date, entrada_aluno_date, valor_por_dia)
                                                        if valor_calculo_prorata > 0:
                                                            dependente_studentAgreement_value = 0
                                                            
                                                        contador_dependentes_prorata += 1
                                                        valor_mensal_dependente_prorata = float(valor_calculo_prorata)
                                                        contagem_value_dependente_prorata += float(valor_mensal_dependente_prorata)
                                                        
                                                        try:
                                                            dados_extrato.append({"name": dependente_firstName + " " + dependente_lastName, "relationship": "DEPENDENTE", "cpf": titular_cpf, "proRata": float(valor_calculo_prorata),
                                                                "value":  float(dependente_studentAgreement_value), "totalValue": float(valor_mensal_dependente_prorata)})
                                                        except:
                                                            print(dependente_firstName)

                                                    else:
                                                        contador_dependentes_empresa += 1
                                                        
                                                        valor_mensal_dependente = dependente_studentAgreement_value
                                                        
                                                        dados_extrato.append({"name": dependente_firstName + " " + dependente_lastName, "relationship": "DEPENDENTE", "cpf": titular_cpf, "proRata": 0,
                                                            "value":  float(dependente_studentAgreement_value), "totalValue": float(valor_mensal_dependente)})

                                                        contagem_value_dependente += float(valor_mensal_dependente)

                        if dados_relatorio == []:  
                            dados_relatorio.append({"reference": "Pro rata - Titulares", "quantity": float(contador_titulares_prorata), "value": float(contagem_value_titular_prorata)})
                            dados_relatorio.append({"reference": "Mensalidade  - Titulares", "quantity": float(contador_titulares_empresa), "value": float(contagem_value_titular)})
                            dados_relatorio.append({"reference": "Pro rata - Dependentes", "quantity": float(contador_dependentes_prorata), "value": float(contagem_value_dependente_prorata)})
                            dados_relatorio.append({"reference": "Mensalidade - Dependentes", "quantity": float(contador_dependentes_empresa),"value": float(contagem_value_dependente)})
                        else:
                            # OBJ PRORATA TITULARES
                            dados_relatorio[0]['quantity'] = dados_relatorio[0]['quantity'] + float(contador_titulares_prorata)
                            dados_relatorio[0]['value'] = dados_relatorio[0]['value'] + float(contagem_value_titular_prorata)
                            # OBJ MENSALIDADE TITULARES
                            dados_relatorio[1]['quantity'] = dados_relatorio[1]['quantity'] + float(contador_titulares_empresa)
                            dados_relatorio[1]['value'] = dados_relatorio[1]['value'] + float(contagem_value_titular)
                            # OBJ PRORATA DEPENDENTES
                            dados_relatorio[2]['quantity'] = dados_relatorio[2]['quantity'] + float(contador_dependentes_prorata)
                            dados_relatorio[2]['value'] = dados_relatorio[2]['value'] + float(contagem_value_dependente_prorata)
                            # OBJ MENSALIDADE DEPENDENTES
                            dados_relatorio[3]['quantity'] = dados_relatorio[3]['quantity'] + float(contador_dependentes_empresa)
                            dados_relatorio[3]['value'] = dados_relatorio[3]['value'] + float(contagem_value_dependente)

                        boleto_empresa = float(empresa_value) + float(contagem_value_titular_prorata) + float(contagem_value_titular) + float(contagem_value_dependente_prorata) + float(contagem_value_dependente)
                        # print(f"Valor de Vida: {empresa_value}, Valor Prorata Titular: {contagem_value_titular_prorata}, Valor Mensal Titular: {contagem_value_titular}, 
                        #       Valor Prorata Dependentes:{contagem_value_dependente_prorata}, Valor Mensal Dependente{contagem_value_dependente}")

                        valor_soma_total = float(contagem_value_titular_prorata) + float(contagem_value_titular) + float(contagem_value_dependente_prorata) + float(contagem_value_dependente)
                        # print(boleto_empresa)
                        
                        if empresa_id == 2254:
                            imposto = 0.025
                            resultado = Abatimento_Imposto(boleto_empresa, imposto)
                            boleto_empresa = resultado
                        
                        lista = {"Extrato": dados_extrato,"Relatorio": dados_relatorio}
                        lista_json = json.dumps(lista, indent=2)

                        if grupo_billingType == 'APARTADO' and empresa_id != 2494:
                            # print(empresa_tradeName, empresa_id)
                            # print(colored(f"ID: {id_temp} | Nome: {name_temp} | PDF:\n{lista_json}", "yellow"))
                            # print(colored(f'Valor do boleto do grupo apartado: {boleto_empresa}\n', 'green'))
                            GenerateInvoicing(boleto_empresa, empresa_cnpj, data_vencimento,competencia_mes_ano,dados_extrato,dados_relatorio,valor_soma_total,empresa_id,empresa_tradeName)

                        elif grupo_billingType == 'UNIFICADO':
                            boleto_grupo += boleto_empresa
                            
                            if qnt_empresas == contador_empresas_grupo:
                                boleto_empresa = boleto_grupo
                                # print(colored(f"ID: {id_temp} | Nome: {name_temp} | PDF:\n{lista_json}", "yellow"))
                                # print(colored(f'Valor do boleto do grupo unificado: {boleto_grupo}\n', 'green'))
                                GenerateInvoicing(boleto_empresa, grupo_cnpj, data_vencimento,competencia_mes_ano,dados_extrato,dados_relatorio,valor_soma_total,id_temp,name_temp)
           