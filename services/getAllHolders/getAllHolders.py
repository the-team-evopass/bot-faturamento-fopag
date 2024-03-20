import requests

def getAllHolders (baseURL): 

    url = f'{baseURL}/holder?include=dependents,contacts,agreements,addresses,companies'

    payload = {}
    headers = {}

    response = requests.request('GET', url, headers=headers, data=payload)

    if response.status_code != 200:
        print('Erro ao pegar lista de titulares ' + str(response.status_code) + ' || ' + response.text + ' (getAllHolders)')

    return response.json()