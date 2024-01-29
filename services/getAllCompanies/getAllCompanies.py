import json
import requests

def getAllCompanies (baseURL): 

    url = f'{baseURL}/company?expand=companyContacts%2CcompanyAddress%2CcompanyAgreements%2Cstudents'

    payload = {}
    headers = {}

    response = requests.request('GET', url, headers=headers, data=payload)

    if response.status_code != 200:
        print('Erro ao pegar lista de empresas ' + str(response.status_code) + ' || ' + response.text + ' (getAllCompanies)')

    return response.json()