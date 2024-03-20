import requests

def getAllCompanies (baseURL): 

    url = f'{baseURL}/company?include=holders,agreements,contacts,addresses'

    payload = {}
    headers = {}

    response = requests.request('GET', url, headers=headers, data=payload)

    if response.status_code != 200:
        print('Erro ao pegar lista de empresas ' + str(response.status_code) + ' || ' + response.text + ' (getAllCompanies)')

    return response.json()