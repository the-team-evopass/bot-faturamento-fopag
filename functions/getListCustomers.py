import requests

def getListCustomers (): 

    url = "https://sandbox.asaas.com/api/v3/customers?limit=100"

    payload = ""
    headers = {
        'access_token': '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNTg2MTM6OiRhYWNoX2Q3ZDk0MDBhLThmYjAtNDZjNC1iNDMxLTZiMjYyYTJjMzFjMQ==',
        'Cookie': 'AWSALB=37ZS/gFEN7Jqw5HPoTYExFw1qeT85ciDIPIEtWl4/ziKL+pUOlrjxrJCUbK4oWqhDaRD+0sRADgnDR9XbFdruOve6J+0t4snKR1DjfcGrRdjCQU3zrVwWxwTGZ2D; AWSALBCORS=37ZS/gFEN7Jqw5HPoTYExFw1qeT85ciDIPIEtWl4/ziKL+pUOlrjxrJCUbK4oWqhDaRD+0sRADgnDR9XbFdruOve6J+0t4snKR1DjfcGrRdjCQU3zrVwWxwTGZ2D; AWSALBTG=Ti5PskdC+Hzf2yc7FLjttBij8QotfR01R6PZFtWbSR3N4ZOWsZJ8PjCnTPmQMBL3mmy5xwqeVjEmg9zhgS8nIY+s8ty0yUvfFPC9KcJo+Ys3rmE6yko6tEL5feeUH+EJRkAOXrle9DLkIuy6TtKrs+6VAhTNrXdWOfqzxtE8q5oQ; AWSALBTGCORS=Ti5PskdC+Hzf2yc7FLjttBij8QotfR01R6PZFtWbSR3N4ZOWsZJ8PjCnTPmQMBL3mmy5xwqeVjEmg9zhgS8nIY+s8ty0yUvfFPC9KcJo+Ys3rmE6yko6tEL5feeUH+EJRkAOXrle9DLkIuy6TtKrs+6VAhTNrXdWOfqzxtE8q5oQ'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code != 200:
        print('Erro ao pegar lista de clientes do asaas ' + str(response.status_code) + ' || ' + response.text + ' (getListCustumers)')

    return response.json()['data']