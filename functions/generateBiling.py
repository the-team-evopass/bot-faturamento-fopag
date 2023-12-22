import requests
import json

def generateBiling (invoiceData):

    url = "https://sandbox.asaas.com/api/v3/payments"

    payload = json.dumps(invoiceData)

    headers = {
        'Content-Type': 'application/json',
        'access_token': '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNTg2MTM6OiRhYWNoX2Q3ZDk0MDBhLThmYjAtNDZjNC1iNDMxLTZiMjYyYTJjMzFjMQ=='
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        print('Erro ao gerar boleto ' + str(response.status_code) + ' || ' + response.text + ' (generateBilling)')

    return json.loads(response.content)['invoiceUrl']