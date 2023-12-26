from asyncio.windows_events import NULL
import requests
import json

# Ao emitir uma NF, se atentar ao endereço da empresa... Se ele for da mesma cidade, devemos emitir a NF com o valor liquido (falar com o Felipe e a Carolina)

def generateIssueNf(payment, value, effective_date):

    # consfigurado para prod
    url = "https://api.asaas.com/v3/invoices"

    payload = {
        "payment": payment,
        "serviceDescription": 'mocar valor',
        "observations": 'mocar valor',
        "value": value,
        "deductions": 0,
        "effectiveDate": effective_date,
        "taxes": {
            "retainIss": False,
            "iss": 2.5,
            "cofins": 0,
            "csll": 0,
            "inss": 0,
            "ir": 0,
            "pis": 0
        },
        "municipalServiceId": "82271",
        "municipalServiceCode": NULL,
        "municipalServiceName": "3370170 | 10.05 - INTERMEDIACAO DE NEGOCIOS"
    }

    headers = {
        'Content-Type': 'application/json',
        # configurado para prod
        'access_token': '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAzNzY1NDY6OiRhYWNoX2E3ZWMwNzlmLTUzMjktNDNlMi05YTU5LTFiYTExODExOGY5NA==',
    }

    payload_json = json.dumps(payload)

    response = requests.post(url, headers=headers, data=payload_json)

    if response.status_code != 200:
        print('Erro ao emitir nota fiscal no asaas ' + str(response.status_code) + ' || ' + response.text + ' (issueNF)')

    print(json.loads(response.content))

    return response.text


generateIssueNf('pay_4308258900251291', 10, '2023-12-23')