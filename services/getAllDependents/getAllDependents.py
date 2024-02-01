import json
import requests

def getAllDependents (baseURL): 

    url = f'{baseURL}/dependent?expand=student%2CdependentContact%2CdependentAgreement%2CdependentAddress'

    payload = {}
    headers = {}

    response = requests.request('GET', url, headers=headers, data=payload)

    if response.status_code != 200:
        print('Erro ao pegar lista de empresas ' + str(response.status_code) + ' || ' + response.text + ' (getAllHolders)')

    return response.json()