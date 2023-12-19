import requests
import json

def generateExtractRequest(competence, due_date, students, summary, total_amount, instructions):
    url = "https://us-central1-api-evopass-d943e.cloudfunctions.net/v1/generate_pdf/?id=4"

    payload = {
        "competence": competence,
        "dueDate": due_date,
        "students": students,
        "summary": summary,
        "totalAmount": total_amount,
        "instructions": instructions
    }

    headers = {
        'Content-Type': 'application/json'
    }

    payload_json = json.dumps(payload)

    response = requests.post(url, headers=headers, data=payload_json)
    print(response.text)

    return response.text

# # Exemplo de uso da função com os parâmetros do seu payload
# competence = "202312"
# due_date = "2023-12-31"
# students = [
#     {
#         "name": "John Doe",
#         "relationship": "Parent",
#         "cpf": "123.456.789-01",
#         "proRata": "50%",
#         "value": "100.00",
#         "totalValue": "50.00"
#     },
#     {
#         "name": "John Doe",
#         "relationship": "Parent",
#         "cpf": "123.456.789-01",
#         "proRata": "50%",
#         "value": "100.00",
#         "totalValue": "50.00"
#     }
# ]
# summary = [
#     {
#         "reference": "Item 1",
#         "quantity": "2",
#         "value": "30.00"
#     },
#     {
#         "reference": "Item 1",
#         "quantity": "2",
#         "value": "30.00"
#     },
#     {
#         "reference": "Item 1",
#         "quantity": "2",
#         "value": "30.00"
#     }
# ]
# total_amount = "80.00"
# instructions = "Pay by the due date."

# result = generateExtractRequest(competence, due_date, students, summary, total_amount, instructions)
# print(result)