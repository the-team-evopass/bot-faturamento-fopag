import os

valorVariavelAmbiente = os.environ.get('myEnv')

if valorVariavelAmbiente:
    print(f'Rodando em : {valorVariavelAmbiente}')
else:
    valorVariavelAmbiente = 'prod'
    print('Valor da variavel de ambiente não configurada, prod como default.')