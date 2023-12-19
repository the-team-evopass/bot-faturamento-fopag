import requests
import json

# Ao emitir uma NF, se atentar ao endereço da empresa... Se ele for da mesma cidade, devemos emitir a NF com o valor liquido (falar com o Felipe e a Carolina)

def generateIssueNf(payment, installment, service_description, observations, value, deductions, effective_date, external_reference, taxes, municipal_service_id, municipal_service_code, municipal_service_name, access_token, cookie):
    url = "https://sandbox.asaas.com/api/v3/invoices"

    payload = {
        "payment": payment,
        "installment": installment,
        "serviceDescription": service_description,
        "observations": observations,
        "value": value,
        "deductions": deductions,
        "effectiveDate": effective_date,
        "externalReference": external_reference,
        "taxes": taxes,
        "municipalServiceId": municipal_service_id,
        "municipalServiceCode": municipal_service_code,
        "municipalServiceName": municipal_service_name
    }

    headers = {
        'Content-Type': 'application/json',
        'access_token': access_token,
        'Cookie': cookie
    }

    payload_json = json.dumps(payload)

    response = requests.post(url, headers=headers, data=payload_json)

    return response.text

# # Exemplo de uso da função com os parâmetros da sua requisição
# payment = "pay_637959110194"
# installment = None
# service_description = "Nota fiscal da Fatura 101940. \nDescrição dos Serviços: ANÁLISE E DESENVOLVIMENTO DE SISTEMAS"
# observations = "Mensal referente aos trabalhos de Junho."
# value = 300
# deductions = 0
# effective_date = "2023-18-07"
# external_reference = None
# taxes = {
#     "retainIss": False,
#     "iss": 3,
#     "cofins": 3,
#     "csll": 1,
#     "inss": 0,
#     "ir": 1.5,
#     "pis": 0.65
# }
# municipal_service_id = None
# municipal_service_code = "1.01"
# municipal_service_name = "Análise e desenvolvimento de sistemas"
# access_token = "$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNTg2MTM6OiRhYWNoX2MyNWY5MmE2LWQ3ODUtNGYwNi1hOGRlLTE2M2FkMzY2MWJkOA=="
# cookie = 'AWSALB=ZvM9Dba3Pq5bnXoTd8Ayz+FJsIM5jIiIzG2wbKseyFq9NMkXGnfRwye0sL2eAPzQbs1ZB8c7kdXP1G6SYXxgjbgQ3yQO4k7/d5BlaDEr5YFHHujyIANA7naVdKHA; AWSALBCORS=ZvM9Dba3Pq5bnXoTd8Ayz+FJsIM5jIiIzG2wbKseyFq9NMkXGnfRwye0sL2eAPzQbs1ZB8c7kdXP1G6SYXxgjbgQ3yQO4k7/d5BlaDEr5YFHHujyIANA7naVdKHA; AWSALBTG=reK0dIV5liYvqnVf+WgnDlVQ4O58T8ENyqvUKeF7LZHsMThp03hOyAHNnNLgjF09VKdZxmEWn77DXr4A88VNQP+bSJ6IlSn5FRXZota6jFC+S7cxjB5AYoOC5kaKR5bRM93HGgAdZXbI43TGVL/2jEIbbVZDvuwvNdtoByRpy79P; AWSALBTGCORS=reK0dIV5liYvqnVf+WgnDlVQ4O58T8ENyqvUKeF7LZHsMThp03hOyAHNnNLgjF09VKdZxmEWn77DXr4A88VNQP+bSJ6IlSn5FRXZota6jFC+S7cxjB5AYoOC5kaKR5bRM93HGgAdZXbI43TGVL/2jEIbbVZDvuwvNdtoByRpy79P'

# result = create_invoice(payment, installment, service_description, observations, value, deductions, effective_date, external_reference, taxes, municipal_service_id, municipal_service_code, municipal_service_name, access_token, cookie)
# print(result)
