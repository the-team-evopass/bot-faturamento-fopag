from xmlrpc.client import ResponseError
import requests
import json

def generateExtractRequest(competence, due_date, students, summary, total_amount, idCompany, instructions, invoiceUrl, tradeName, cnpj):
    url = f"https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/generate_pdf/?id={idCompany}"

    payload = json.dumps({
        "competence": competence,
        "dueDate": due_date,
        "students": students,
        "summary": summary,
        "totalAmount": total_amount,
        "instructions": instructions,
        'invoiceUrl': invoiceUrl,
        "tradeName": tradeName,
        "cnpj": cnpj
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)

    print(response.content)

    return response.text