from xmlrpc.client import ResponseError
import requests
import json

def generateExtractRequest(competence, due_date, students, summary, total_amount, idCompany, instructions):
    url = f"https://us-central1-api-evoppass-dev.cloudfunctions.net/v1/generate_pdf/?id={idCompany}"

    payload = json.dumps({
        "competence": competence,
        "dueDate": due_date,
        "students": students,
        "summary": summary,
        "totalAmount": total_amount,
        "instructions": instructions
    })

    headers = {
        'Content-Type': 'application/json'
    }

    # payload_json = payload
    print(payload)

    response = requests.post(url, headers=headers, data=payload)
    print(response)

    return response.text