import requests
import json

def generateBiling (baseURL, token, invoiceData):

    url = f'{baseURL}/v3/payments'

    payload = json.dumps(invoiceData)

    headers = {
        'Content-Type': 'application/json',
        'access_token': token
    }
    
    response = requests.request('POST', url, headers=headers, data=payload)

    if response.status_code != 200:
        print('Erro ao gerar boleto ' + str(response.status_code) + ' || ' + response.text + ' (generateBilling)')

    return {
        'billingURL': json.loads(response.content)['invoiceUrl'],
        'billingID': json.loads(response.content)['id']
    }