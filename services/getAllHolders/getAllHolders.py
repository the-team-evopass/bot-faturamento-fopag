import json
import requests

def getAllHolders (baseURL): 

    url = f'{baseURL}/student?expand=dependents%2CstudentContact%2CstudentAgreement%2CstudentAddress%2Ccompany'

    payload = {}
    headers = {}

    response = requests.request('GET', url, headers=headers, data=payload)

    if response.status_code != 200:
        print('Erro ao pegar lista de empresas ' + str(response.status_code) + ' || ' + response.text + ' (getAllHolders)')

    return response.json()