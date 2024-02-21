import requests

def getAllEconomicsGroups(baseURL):
        url = f'{baseURL}/economic_group/company'
        payload = {}
        headers = {}
        response = requests.request('GET', url, headers=headers, data=payload)

        if response.status_code != 200:
            print('Erro ao pegar lista de grupos econômicos ' + str(response.status_code) + ' || ' + response.text + ' (getAllEconomicsGroups)')

        return response.json()