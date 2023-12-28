import requests
import json

def generateBiling (invoiceData):

    url = "https://api.asaas.com/v3/payments"

    payload = json.dumps(invoiceData)

    headers = {
        'Content-Type': 'application/json',
        'access_token': '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAzNzY1NDY6OiRhYWNoX2E3ZWMwNzlmLTUzMjktNDNlMi05YTU5LTFiYTExODExOGY5NA=='
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        print('Erro ao gerar boleto ' + str(response.status_code) + ' || ' + response.text + ' (generateBilling)')

    print('NF emitida para o boleto de id: ' + str(json.loads(response.content)['id']))

    return {
        'billingURL': json.loads(response.content)['invoiceUrl'],
        'billingID': json.loads(response.content)['id']
    }