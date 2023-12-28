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

            print(customer_id)

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