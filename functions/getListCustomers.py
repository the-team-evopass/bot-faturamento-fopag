import requests

def getListCustomers (): 

    url = "https://api.asaas.com/v3/customers?limit=100"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'access_token': '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAzNzY1NDY6OiRhYWNoX2E3ZWMwNzlmLTUzMjktNDNlMi05YTU5LTFiYTExODExOGY5NA=='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code != 200:
        print('Erro ao pegar lista de clientes do asaas ' + str(response.status_code) + ' || ' + response.text + ' (getListCustumers)')

    return response.json()['data']