import requests

def getCustomersList (base, token): 

    url = f'{base}/v3/customers?limit=100'

    payload = ''
    headers = {
        'Content-Type': 'application/json',
        'access_token': token
    }

    response = requests.request('GET', url, headers=headers, data=payload)

    if response.status_code != 200:
        print('Erro ao pegar lista de clientes do asaas ' + str(response.status_code) + ' || ' + response.text + ' (getListCustumers)')

    return response.json()['data']