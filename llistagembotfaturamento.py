import requests

#URLS DAS APIS
urlListagemCompany = 'https://us-central1-api-evopass-d943e.cloudfunctions.net/prod/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements'
urlListagemStudent = 'https://us-central1-api-evopass-d943e.cloudfunctions.net/prod/student?expand=dependents%2CstudentContact%2CstudentAgreement%2CstudentAddress'
urlListagemDependent = 'https://us-central1-api-evopass-d943e.cloudfunctions.net/prod/dependent/'

#FUNÇÃO DE LISTAGEM DE EMPRESA
def ListagemEmpresas(urlListagemCompany):
    try:
        respostaListagemEmpresas = requests.get(urlListagemCompany)
        if respostaListagemEmpresas.status_code == 200:
            empresasJson = respostaListagemEmpresas.json()
            listaEmpresas = empresasJson['data']
            print("Lista de Empresas em Implantação:")
            contagem_empresas_implantacao = 0
            
            #Loop para coletar dados das empresas
            for empresa in listaEmpresas:
                empresa_cnpj = empresa['cnpj']
                empresa_tradeName = empresa['tradeName']
                empresa_companyStatus = empresa['companyStatus']
                
                #Logica para filtrar apenas as empresas que estão em implantacao
                if empresa_companyStatus == "EM IMPLANTACAO":
                    print(empresa_cnpj, empresa_tradeName)
                    contagem_empresas_implantacao += 1
            
            print("")
            print(f"Total de empresas em implantação: {contagem_empresas_implantacao}")
            return listaEmpresas
        
        else:
            print(f"Erro na requisição. Código de Status: {respostaListagemEmpresas.status_code}")
            return []
        

    except Exception as e:
        print(f"Erro: {e}")
        return []

#FUNÇÃO DE LISTAGEM DE FUNCIONARIOS
def ListagemFuncionarios(urlListagemStudent, urlListagemCompany):
    try:
        respostaListagemFuncionarios = requests.get(urlListagemStudent)

        if respostaListagemFuncionarios.status_code == 200:
            funcionarios = respostaListagemFuncionarios.json()
            empresas = ListagemEmpresas(urlListagemCompany)
            
            #Dict para armazenar a contagem de funcionários por empresa
            contagem_por_empresa = {}
            
            for funcionario in funcionarios:
                statusReason = funcionario['statusReason']

                if statusReason == "ATIVO":
                    funcionario_id = funcionario['id']
                    
                    #Filtro empresas correspondentes ao funcionário
                    empresas_correspondentes = [empresa for empresa in empresas if empresa['id'] == funcionario_id]
                    
                    if empresas_correspondentes:
                        for empresa_correspondente in empresas_correspondentes:
                            nome_empresa = empresa_correspondente['tradeName']
                            
                            #Atualiza a contagem para a empresa correspondente
                            contagem_por_empresa[nome_empresa] = contagem_por_empresa.get(nome_empresa, 0) + 1
            
            print("")
            print("")
            print("\nQuantidade de funcionários por empresa em implantação:")
            for empresa, contagem in contagem_por_empresa.items():
                print(f"{empresa}: {contagem}")
            
        else:
            print(f"Erro na requisição. Código de Status: {respostaListagemFuncionarios.status_code}")

    except Exception as e:
        print(f"Erro: {e}")

#FUNÇÃO DE LISTAGEM DE DEPENDENTES
def ListagemDependentes(urlListagemCompany, urlListagemStudent, urlListagemDependent):
    try:
        respostaListagemDependentes = requests.get(urlListagemDependent)
        print("")
        print("")
        if respostaListagemDependentes.status_code == 200:
            dependentes = respostaListagemDependentes.json()
            empresas = ListagemEmpresas(urlListagemCompany)
            
            contagem_por_empresa = {}
            
            for dependente in dependentes:
                statusReason = dependente['statusReason']

                if statusReason == "ATIVO":
                    dependente_id = dependente['id']
                    
                    #Filtro empresas correspondentes ao dependente
                    empresas_correspondentes = [empresa for empresa in empresas if empresa['id'] == dependente_id]
                    
                    if empresas_correspondentes:
                        for empresa_correspondente in empresas_correspondentes:
                            nome_empresa = empresa_correspondente['tradeName']
                            
                            #Atualiza a contagem para a empresa correspondente
                            contagem_por_empresa[nome_empresa] = contagem_por_empresa.get(nome_empresa, 0) + 1
            
            print("\nQuantidade de dependentes por empresa em implantação:")
            for empresa, contagem in contagem_por_empresa.items():
                print(f"{empresa}: {contagem}")
            
        else:
            print(f"Erro na requisição. Código de Status: {respostaListagemDependentes.status_code}")

    except Exception as e:
        print(f"Erro: {e}") 

if __name__ == "__main__":
    ListagemDependentes(urlListagemCompany, urlListagemStudent, urlListagemDependent)
