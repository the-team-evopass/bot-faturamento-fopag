import requests

def criar_cobrancas(urlListarClientes, urlCriarCobranca, empresa_cnpj, valor_total_empresa, headers, data_vencimento):
    try:
        # Obter a lista de clientes
        response = requests.get(urlListarClientes, headers=headers)
        if response.status_code != 200:
            print(f"Erro ao obter a lista de clientes. Código de status: {response.status_code}")
            return
        response_json = response.json()
        response_data = response_json.get('data', [])
        
        cnpj_priocurado = empresa_cnpj

        for customer in response_data:
            response_data_cpfCnpj = customer.get('cpfCnpj', '')

            # if response_data_cpfCnpj == "18313310000121":
            #     print(f"Empresa Asaas: {response_data_cpfCnpj}")

            if response_data_cpfCnpj == empresa_cnpj:
                # Criar uma cobrança para o cliente
                customer_id = customer.get('id', '')
                customer_name = customer.get('name', '')
                invoice_data = {
                    'customer': customer_id,
                    'billingType': 'BOLETO',
                    'value': valor_total_empresa,
                    'dueDate': data_vencimento,
                    'description': 'Cobrança para cliente'
                }
                
                # Criar a cobrança para o cliente
                invoice_response = requests.post(urlCriarCobranca, headers=headers, json=invoice_data)

                if invoice_response.status_code == 200:
                    print(f"Cobrança criada com sucesso para o cliente ID: {customer_name}")
                else:
                    print(f"Erro ao criar a cobrança para o cliente ID: {customer_name}, CNPJ/CPF: {response_data_cpfCnpj}, erro: {invoice_response.status_code}")
                    
                break      
        else:
            # Este bloco será executado se o loop for concluído sem o break (ou seja, se response_data_cpfCnpj não for encontrado)
            print(f"Cliente com CNPJ/CPF {empresa_cnpj} não encontrado.")

    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
