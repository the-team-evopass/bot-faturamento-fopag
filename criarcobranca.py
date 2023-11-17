# CRIANDO COBRANÇA PARA TODOS OS CLIENTES DO ASAAS
import requests

#Api do asaas
api_key = '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNTg2MTM6OiRhYWNoXzU5ODI0NzYxLTBiNGQtNDQwNC1iZTAxLWM1OTAyOTQ2NGRlZg=='

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
            'billingType': 'BOLETO',  # Pode ser 'BOLETO' ou 'CREDIT_CARD'
            'value': 10,  # Valor da cobrança
            'dueDate': '2023-12-02',  # Data de vencimento
            'description': 'Cobrança para cliente',
        }

        #Criar a cobrança dos clientes
        invoice_response = requests.post(urlCriarCobranca, headers=headers, json=invoice_data)

        if invoice_response.status_code == 200:
            print(f"Cobrança criada com sucesso para o cliente ID: {customer_name}")
        else:
            print(f"Erro ao criar a cobrança para o cliente ID: {customer_name}")
else:
    print(f"Erro ao listar os clientes. Status Code: {response.status_code}")
    print(f"Resposta: {response.text}")
