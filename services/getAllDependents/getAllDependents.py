import requests

def getAllDependents (baseURL): 

    url = f'{baseURL}/dependent?include=contacts,agreements,holder,companies,addresses'

    payload = {}
    headers = {}

    response = requests.request('GET', url, headers=headers, data=payload)

    if response.status_code != 200:
        print('Erro ao pegar lista de dependentes ' + str(response.status_code) + ' || ' + response.text + ' (getAllDependents)')

    return response.json()