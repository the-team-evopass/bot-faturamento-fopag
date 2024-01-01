from termcolor import colored

from middleware import runGetCustomersList
from middleware import runGenerateBiling
from functions.searchCustumer import findIdCustumerByCNPJ

def criar_cobranca(empresa_cnpj, valor_total_empresa, data_vencimento):

    try:

        listCustumers = runGetCustomersList()
        resultOffFindIdCustumerByCNPJ = findIdCustumerByCNPJ(listCustumers, empresa_cnpj)

        if resultOffFindIdCustumerByCNPJ != False:

            customer_id = resultOffFindIdCustumerByCNPJ

            print(colored(customer_id, 'green'))

            invoice_data = {
                'customer': customer_id,
                'billingType': 'BOLETO',
                'value': valor_total_empresa,
                'dueDate': data_vencimento,
                'description': 'Parcela 1 de 1'
            }

            res = runGenerateBiling(invoice_data)
            return res

        else:
            print('Erro ao encontrar o idCustumer na base de clientes do asaas!!')

    except Exception as e:
        print(f"Erro inesperado: {str(e)}")