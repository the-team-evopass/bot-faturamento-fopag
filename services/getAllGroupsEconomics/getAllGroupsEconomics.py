import requests

def getAllGroupsEconomics (baseURL): 

    url = f'{baseURL}//economic_group?include=companies'

    payload = {}
    headers = {}

    response = requests.request('GET', url, headers=headers, data=payload)

    if response.status_code != 200:
        print('Erro ao pegar lista de grupos economicos ' + str(response.status_code) + ' || ' + response.text + ' (getAllGroupsEconomics)')

    return response.json()