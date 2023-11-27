import requests

# URLs DAS APIs
urlListagemCompany = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements'
urlListagemStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student?expand=dependents%2CstudentContact%2CstudentAgreement%2CstudentAddress'
urlListagemAgreementStudent = 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/student_agreement'

# FUNÇÃO DE LISTAGEM DE EMPRESA
def ListagemEmpresas(urlListagemCompany):
    try:
        respostaListagemEmpresas = requests.get(urlListagemCompany)
        if respostaListagemEmpresas.status_code == 200:
            empresasJson = respostaListagemEmpresas.json()
            listaEmpresas = empresasJson['data']
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
            return listaEmpresas
        
        else:
            print(f"Erro na requisição. Código de Status: {respostaListagemEmpresas.status_code}")
            return []

    except Exception as e:
        print(f"Erro: {e}")
        return []

# FUNÇÃO DE LISTAGEM DE FUNCIONÁRIOS
def ListagemFuncionarios(urlListagemStudent, empresas):
    try:
        respostaListagemFuncionarios = requests.get(urlListagemStudent)

        if respostaListagemFuncionarios.status_code == 200:
            funcionarios = respostaListagemFuncionarios.json()

            # Dict para armazenar a contagem de funcionários por empresa
            contagem_por_empresa = {}

            for funcionario in funcionarios:
                statusReason = funcionario['statusReason']

                if statusReason == "Ativo":
                    funcionario_id = funcionario['id']
                    empresa_id = funcionario['id']

                    # Procurar a empresa correspondente
                    empresa_correspondente = next((empresa for empresa in empresas if empresa['id'] == empresa_id), None)

                    if empresa_correspondente:
                        nome_empresa = empresa_correspondente['tradeName']

                        # Atualizar a contagem para a empresa correspondente
                        contagem_por_empresa[nome_empresa] = contagem_por_empresa.get(nome_empresa, 0) + 1

            print("\nQuantidade de funcionários por empresa em implantação:")
            if contagem_por_empresa:
                for empresa, contagem in contagem_por_empresa.items():
                    print(f"{empresa}: {contagem} funcionário(s)")
            else:
                print("Nenhum funcionário ativo encontrado nas empresas em implantação.")

        else:
            print(f"Erro na requisição. Código de Status: {respostaListagemFuncionarios.status_code}")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    empresas_em_implantacao = ListagemEmpresas(urlListagemCompany)
    ListagemFuncionarios(urlListagemStudent, empresas_em_implantacao)
