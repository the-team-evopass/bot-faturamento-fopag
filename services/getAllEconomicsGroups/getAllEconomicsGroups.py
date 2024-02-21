import json
import requests
import time

def getAllEconomicsGroups(baseURL):
    try:
        url = f'{baseURL}/economic_group/company'
        payload = {}
        headers = {}
        response = requests.request('GET', url, headers=headers, data=payload)

        if response.status_code != 200:
            print('Erro ao pegar lista de grupos econômicos ' + str(response.status_code) + ' || ' + response.text + ' (getAllEconomicsGroups)')

        return response.json()
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 500:
            print("Erro 500 - Tentando novamente...")
            time.sleep(1)
            return getAllEconomicsGroups(baseURL)
        else:
            print(f"Erro HTTP: {response.status_code} - {e}")

    except Exception as e:
        print(f"Erro: {e}")