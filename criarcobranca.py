from functions.getListCustomers import getListCustomers
from functions.searchCustumer import findIdCustumerByCNPJ
from functions.generateBiling import generateBiling

def criar_cobrancas(empresa_cnpj, valor_total_empresa, data_vencimento):

    try:
        # Obter a lista de clientes
        listCustumers = getListCustomers()
        resultOffFindIdCustumerByCNPJ = findIdCustumerByCNPJ(listCustumers, empresa_cnpj)

        if resultOffFindIdCustumerByCNPJ != False:
            # Criar uma cobrança para o cliente
            customer_id = resultOffFindIdCustumerByCNPJ
            invoice_data = {
                'customer': customer_id,
                'billingType': 'BOLETO',
                'value': valor_total_empresa,
                'dueDate': data_vencimento,
                'description': 'Melhorar essa descrição'
            }

            res = generateBiling(invoice_data)
            return res

        else:
            print('Erro ao encontrar o idCustumer na base de clientes do asaas!!')

    except Exception as e:
        print(f"Erro inesperado: {str(e)}")


# def criar_cobrancas(urlListarClientes, urlCriarCobranca, empresa_cnpj, valor_total_empresa, headers, data_vencimento):
#     try:
#         # Obter a lista de clientes
#         response = requests.get(urlListarClientes, headers=headers)
#         if response.status_code != 200:
#             print(f"Erro ao obter a lista de clientes. Código de status: {response.status_code}")
#             return
#         response_json = response.json()
#         response_data = response_json.get('data', [])

#         for customer in response_data:
#             response_data_cpfCnpj = customer.get('cpfCnpj', '')

#             if response_data_cpfCnpj == empresa_cnpj:
#                 # Criar uma cobrança para o cliente
#                 customer_id = customer.get('id', '')
#                 customer_name = customer.get('name', '')
#                 invoice_data = {
#                     'customer': customer_id,
#                     'billingType': 'BOLETO',
#                     'value': valor_total_empresa,
#                     'dueDate': data_vencimento,
#                     'description': 'Cobrança para cliente'
#                 }
                
#                 # Criar a cobrança para o cliente
#                 invoice_response = requests.post(urlCriarCobranca, headers=headers, json=invoice_data)

#                 if invoice_response.status_code == 200:
#                     print('Response da minha emissão de boleto---------------------------------')
#                     print(f"Cobrança criada com sucesso para o cliente ID: {customer_name}")
#                     return json.loads(invoice_response.content)['invoiceUrl']
#                 else:
#                     print(f"Erro ao criar a cobrança para o cliente ID: {customer_name}, CNPJ/CPF: {response_data_cpfCnpj}, erro: {invoice_response.status_code}")
                    
#                 break      
#             else:
#                 # Este bloco será executado se o loop for concluído sem o break (ou seja, se response_data_cpfCnpj não for encontrado)
#                 print(f"Cliente com CNPJ/CPF {empresa_cnpj} não encontrado.")

#     except Exception as e:
#         print(f"Erro inesperado: {str(e)}")