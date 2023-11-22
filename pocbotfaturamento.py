import requests

urlListagemEmpresas = 'https://us-central1-api-evopass-d943e.cloudfunctions.net/prod/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements'
urlListaFuncionarios = 'https://us-central1-api-evopass-d943e.cloudfunctions.net/prod/student?expand=dependents%2CstudentContact%2CstudentAgreement%2CstudentAddress'


def ListaEmpresas(urlListagemEmpresas):
    try:
        respostaListagemEmpresas = requests.get(urlListagemEmpresas)

        if respostaListagemEmpresas.status_code == 200:
            empresas = respostaListagemEmpresas.json()
            listaEmpresas = empresas['data']
            print("Lista de Empresas:")

            for empresa in listaEmpresas:
                empresa_tradeName = empresa['tradeName']
                empresa_id = empresa['id']
                print(empresa_id, empresa_tradeName)
            return listaEmpresas

        else:
            print(f"Erro na requisição. Código de Status: {respostaListagemEmpresas.status_code}")
            return []

    except Exception as e:
        print(f"Erro: {e}")
        return []

def ListaFuncionarios(urlListaFuncionarios):
    try:
        respostaListagemFuncionarios = requests.get(urlListaFuncionarios)

        if respostaListagemFuncionarios.status_code == 200:
            funcionarios = respostaListagemFuncionarios.json()
            empresas = ListaEmpresas(urlListagemEmpresas)
            print("")
            print("Lista de funcionários por empresas:")
            for funcionariosFiltrados in funcionarios:
                funcionariosFiltrados_statusReason = funcionariosFiltrados['statusReason']

                if funcionariosFiltrados_statusReason == "ATIVO":
                    funcionariosFiltrados_Id = funcionariosFiltrados['id']

                    empresasCorrespondentes = [empresa for empresa in empresas if empresa['id'] == funcionariosFiltrados_Id]
                    
                    if empresasCorrespondentes:
                        for empresaCorrespondente in empresasCorrespondentes:
                            nomeEmpresaCorrespondente = empresaCorrespondente['tradeName']
                            funcionariosFiltrados_firstName = funcionariosFiltrados['firstName']
                            print(f"Funcionários da empresa {nomeEmpresaCorrespondente}: {funcionariosFiltrados_firstName}")
                    else:
                        print(f"O funcionário {funcionariosFiltrados['firstName']} não está cadastrado em uma empresa.")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    ListaFuncionarios(urlListaFuncionarios)
