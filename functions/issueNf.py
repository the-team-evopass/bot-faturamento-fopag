from asyncio.windows_events import NULL
from email.mime import base
import requests
import json

# Ao emitir uma NF, se atentar ao endereço da empresa... Se ele for da mesma cidade, devemos emitir a NF com o valor liquido (falar com o Felipe e a Carolina)

def generateIssueNf(baseURL, token, payment, value, effectiveDate):

    # consfigurado para prod
    url = f'{baseURL}/v3/invoices'

    payload = {
        'payment': payment,
        'serviceDescription': 'mocar valor',
        'observations': 'mocar valor',
        'value': value,
        'deductions': 0,
        'effectiveDate': effectiveDate,
        'taxes': {
            'retainIss': False,
            'iss': 2.5,
            'cofins': 0,
            'csll': 0,
            'inss': 0,
            'ir': 0,
            'pis': 0
        },
        'municipalServiceId': '82271',
        'municipalServiceCode': NULL,
        'municipalServiceName': '3370170 | 10.05 - INTERMEDIACAO DE NEGOCIOS'
    }

    headers = {
        'Content-Type': 'application/json',
        'access_token': token,
    }

    payload_json = json.dumps(payload)

    response = requests.post(url, headers=headers, data=payload_json)

    if response.status_code != 200:
        print('Erro ao emitir nota fiscal no asaas ' + str(response.status_code) + ' || ' + response.text + ' (issueNF)')

    print('NF emitida para o boleto de id: ' + str(payment))

    return response.text