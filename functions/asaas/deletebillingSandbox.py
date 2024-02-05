import requests

def DeleteBilling(id_cobranca):
    url = f'https://sandbox.asaas.com/api/v3/payments/{id_cobranca}'
    headers = {
        "accept": "application/json",
        "access_token": "$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNTg2MTM6OiRhYWNoXzk5ZDg3ZGJlLWM2NmYtNGFjMS1hNTdmLWM5YjlhYmVlNDVmNA==" 
    }
    resposta_delete_cobranca = requests.delete(url, headers=headers)

    if resposta_delete_cobranca.status_code == 200:
        print(f"A cobrança do id {id_cobranca} foi apagada")
    else:
        print(f"Falha ao apagar a cobrança do id {id_cobranca}")

def ListAndDeleteBilling():
    url = 'https://sandbox.asaas.com/api/v3/payments'
    headers = {
        "accept": "application/json",
        "access_token": "$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNTg2MTM6OiRhYWNoXzk5ZDg3ZGJlLWM2NmYtNGFjMS1hNTdmLWM5YjlhYmVlNDVmNA=="  
    }

    limite_pag = 100
    offset = 0

    while True:
        params = {
            'limit': limite_pag,
            'offset': offset
        }
        response_list = requests.get(url, headers=headers, params=params)

        if response_list.status_code == 200:
            data = response_list.json()['data']
            if not data:
                print('Sem cobranças no Asaas Sandbox')
                break
            for cobranca in data:
                id_cobranca = cobranca['id']
                DeleteBilling(id_cobranca)
            offset += limite_pag
        else:
            print("Falha ao obter a lista de cobranças")
            break

ListAndDeleteBilling()