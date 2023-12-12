import requests
from coletadedados import relacao_ativos
from datavencimento import calcular_data_vencimento

def criar_cobrancas_para_clientes(api_key):
    # URLs do Asaas
    url_listar_clientes = 'https://sandbox.asaas.com/api/v3/customers'
    url_criar_cobranca = 'https://sandbox.asaas.com/api/v3/payments'

    # Cabeçalho
    headers = {
        'Content-Type': 'application/json',
        'access_token': api_key
    }

    # Obter lista de clientes
    response = requests.get(url_listar_clientes, headers=headers)
    
    if response.status_code != 200:
        print(f"Erro ao listar os clientes. Status Code: {response.status_code}")
        print(f"Resposta: {response.text}")
        return

    customers = response.json()['data']

    # Iterar sobre os clientes e criar cobranças
    valor = 0  # Substituir pelo valor no banco de dados
    for customer in customers:
        customer_id = customer['id']
        customer_name = customer['name']

        # Dados da cobrança
        invoice_data = {
            'customer': customer_id,
            'billingType': 'BOLETO',
            'value': valor,
            'dueDate': calcular_data_vencimento(),
            'description': 'Cobrança para cliente',
        }

        # Criar a cobrança
        invoice_response = requests.post(url_criar_cobranca, headers=headers, json=invoice_data)

        if invoice_response.status_code == 200:
            print(f"Cobrança criada com sucesso para o cliente ID: {customer_name}")
        else:
            print(f"Erro ao criar a cobrança para o cliente ID: {customer_name}")
            print(f"Status Code: {invoice_response.status_code}")
            print(f"Resposta: {invoice_response.text}")

if __name__ == "__main__":
    # Api do Asaas
    api_key = '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNTg2MTM6OiRhYWNoXzU5ODI0NzYxLTBiNGQtNDQwNC1iZTAxLWM1OTAyOTQ2NGRlZg=='
    
    # Chamar a função principal
    criar_cobrancas_para_clientes(api_key)
