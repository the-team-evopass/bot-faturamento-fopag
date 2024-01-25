import requests
import json

def uploadContract (idCompany) :

    url = "https://us-central1-api-evopass-d943e.cloudfunctions.net/v1/company_agreement/"

    payload = json.dumps({
    "companyAgreement": {
        "company": idCompany,
        "companyIdDocument": 1,
        "status": True,
        "plan": "PADRÃO",
        "conditions": "NULL",
        "value": 79.9
    }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# Array de IDs
ids = [
    2194, 2384, 2184, 2204, 2224, 2234, 2244, 2264, 2284, 2304, 
    2324, 2334, 2354, 2364, 2374, 2394, 2214, 2254, 2314, 2454, 
    2464, 2274, 2344, 2294
]


# Loop "for each" para percorrer cada ID e chamar a função
for id in ids:
    uploadContract(id)