import json

# Suponha que você tenha uma tabela representada como um dicionário
tabela = {
    'nome': ['Alice', 'Bob', 'Charlie'],
    'idade': [25, 30, 22],
    'cidade': ['CidadeA', 'CidadeB', 'CidadeC']
}

# Use o módulo json para converter o dicionário em uma string JSON
json_string = json.dumps(tabela, indent=2)  # indent é opcional e adiciona espaços para melhor legibilidade

# Exiba a string JSON resultante
print(json_string)