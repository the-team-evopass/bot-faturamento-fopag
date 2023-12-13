# CRIANDO COBRANÇA PARA TODOS OS CLIENTES DO ASAAS
import requests
from coletadedados import relacao_ativos
from datavencimento import calcular_data_vencimento

#Api do asaas
api_key = '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNTg2MTM6OiRhYWNoX2QyMGQ0MGYwLWYwZTEtNDI5NS1iYmRlLTIyNzFjMTZlNjZhNw=='

#URLs do asaas
urlListarClientes = 'https://sandbox.asaas.com/api/v3/customers'
urlCriarCobranca = 'https://sandbox.asaas.com/api/v3/payments'

#Cabeçalho
headers = {
    'Content-Type': 'application/json',
    'access_token': api_key
}

#Listar clientes
response = requests.get(urlListarClientes, headers=headers)

if response.status_code == 200:
    print("Lista de clientes obtida com sucesso:")
    response_data = response.json()

    #Identificar os clientes de cada 'data' e criar uma cobrança para cada cliente
    for customer in response_data['data']:
        customer_id = customer['id']
        customer_name = customer['name']
        invoice_data = {
            'customer': customer_id,  # ID do cliente
            'billingType': 'BOLETO',  #BOLETO = FOPAG
            'value': relacao_ativos,  # Valor da cobrança            (Substituir pelo valor no banco de dados)
            'dueDate': calcular_data_vencimento(),  # Data de vencimento  (Substituir pelo valor no banco de dados)
            'description': 'Cobrança para cliente',
        }

        #Criar a cobrança para os clientes
        invoice_response = requests.post(urlCriarCobranca, headers=headers, json=invoice_data)

        if invoice_response.status_code == 200:
            print(f"Cobrança criada com sucesso para o cliente ID: {customer_name}")
        else:
            print(f"Erro ao criar a cobrança para o cliente ID: {customer_name}")
else:
    print(f"Erro ao listar os clientes. Status Code: {response.status_code}")
    print(f"Resposta: {response.text}")