import requests
import json

url = "https://sandbox.asaas.com/api/v3/customers"
access_token = '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNTg2MTM6OiRhYWNoX2QyMGQ0MGYwLWYwZTEtNDI5NS1iYmRlLTIyNzFjMTZlNjZhNw=='

empresas = [
    {
      "Nome": "Ipsis Gráfica e Editora",
      "Email": "ti@evopass.app.br",
      "CNPJ": "61407078000110"
    },
    {
      "Nome": "A L ALUMINIO UNIPESSOAL LTDA FILIAL ALUMINIO",
      "Email": "ti@evopass.app.br",
      "CNPJ": "43413067000241"
    },
    {
      "Nome": "PAES E DOCES SABOR DO PAO LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "61695466000143"
    },
    {
      "Nome": "COMERCIAL OSWALDO CRUZ LIMITADA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "59276790000185"
    },
    {
      "Nome": "EFATHA SOLUCOES TECNOLOGICAS E EQUIPAMENTOS DE INFORMATICA LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "15292079000149"
    },
    {
      "Nome": "SOUSA GESTAO DE NEGOCIOS LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "06096266000166"
    },
    {
      "Nome": "SIANFER FERRO E ACO LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "54094768000109"
    },
    {
      "Nome": "RECUPER IDENTIFICACAO E REMOCAO DE VEICULOS LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "07514830000186"
    },
    {
      "Nome": "MODERNA TREINAMENTO E SERVICOS ADMINISTRATIVOS LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "22228090000105"
    },
    {
      "Nome": "DUDA AUTO CENTER LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "16808233000236"
    },
    {
      "Nome": "NOVEMP INDUSTRIA E COMERCIO LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "04753102000210"
    },
    {
      "Nome": "R. LUZ CONSULTORIA E ASSESSORIA CONTABIL LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "10899502000150"
    },
    {
      "Nome": "A L INDUSTRIA, COMERCIO, IMPORTACAO E EXPORTACAO DE ACESSORIOS PARA VIDRO, ALUMINIO E MATERIAIS DE CONSTRUCAO UNIPESSOAL LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "09406784000127"
    },
    {
      "Nome": "BOA HORA CENTRAL DE TRATAMENTO DE RESIDUOS LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "58757725000109"
    },
    {
      "Nome": "GERENCIAMENTO AMBIENTAL TECH-LIX LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "04902653000117"
    },
    {
      "Nome": "SOMERLOG LOGISTICA E TRANSPORTES LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "14878453000200"
    },
    {
      "Nome": "GF SERVICOS ESPECIALIZADOS LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "12358619000151"
    },
    {
      "Nome": "SANCHES BLANES S/A INDUSTRIA DE MAQUINAS E FERRAMENTAS",
      "Email": "ti@evopass.app.br",
      "CNPJ": "57482887000119"
    },
    {
      "Nome": "REBRACIL INDUSTRIA DE EMBALAGENS E REQUALIFICADORA LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "17193367000171"
    },
    {
      "Nome": "MECANICA INDUSTRIAL CENTRO LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "64877996000109"
    },
    {
      "Nome": "A L ALUMINIO UNIPESSOAL LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "43413067000160"
    },
    {
      "Nome": "J J REPAIR MANUTENCAO DE APARELHOS ELETRONICOS LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "42496457000189"
    },
    {
      "Nome": "IPCAN COMERCIO DE PRODUTOS DE SEGURANCA E INFORMATICA LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "13753746000118"
    },
    {
      "Nome": "ARZ - SERVICOS DE LOCACAO LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "34426978000131"
    },
    {
      "Nome": "MARRO MAQUINAS OPERATRIZES LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "66080656000170"
    },
    {
      "Nome": "INDUSTRIA AGRO-QUIMICA BRAIDO LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "59274167000193"
    },
    {
      "Nome": "BRASMEG TRANSPORTES LTDA",
      "Email": "ti@evopass.app.br",
      "CNPJ": "13520755000169"
    }
]

headers = {
    'Content-Type': 'application/json',
    'access_token': access_token
}

for empresa in empresas:
    payload = json.dumps({
        "name": empresa["Nome"],
        "email": empresa["Email"],
        "cpfCnpj": empresa["CNPJ"]
    })

    response = requests.post(url, headers=headers, data=payload)

    print(f"Empresa {empresa['Nome']} cadastrada. Status code: {response}")
    print(response.text)
