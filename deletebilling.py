import requests

url = 'https://sandbox.asaas.com/api/v3/payments'

headers = {
    "accept": "application/json",
    "access_token": "$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNTg2MTM6OiRhYWNoXzk5ZDg3ZGJlLWM2NmYtNGFjMS1hNTdmLWM5YjlhYmVlNDVmNA=="
}

resposta_lista_cobrancas = requests.get(url, headers=headers)

json_listacobranca = resposta_lista_cobrancas.json()
listaCobranca = json_listacobranca['data']
if listaCobranca != []:

    def DeleteBilling(id_cobranca):
        url = f'https://sandbox.asaas.com/api/v3/payments/{id_cobranca}'

        headers = {
        "accept": "application/json",
        "access_token": "$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNTg2MTM6OiRhYWNoXzk5ZDg3ZGJlLWM2NmYtNGFjMS1hNTdmLWM5YjlhYmVlNDVmNA=="
        }

        resposta_delete_cobranca = requests.delete(url, headers=headers)

        return print(f"A cobrança do id {id_cobranca} foi apagada")

    for cobranca in listaCobranca:
        id_cobranca = cobranca['id']
        DeleteBilling(id_cobranca)

else:
    print("Sem cobranças no Asaas Sandbox")


