import os

def getEnvironmentVar(type) :

    if type == 'ambient' :

        valorVariavelAmbiente = os.environ.get('MY_AMBIENT_VAR')

        if valorVariavelAmbiente:
            print(f'Rodando em : {valorVariavelAmbiente}')
            return 'dev'
        else:
            valorVariavelAmbiente = 'prod'
            print('Valor da variavel de ambiente não configurada, prod como default.')
            return 'prod'
        
    elif type == 'devAccessToken' :

        print('Pegar token de produção')

    elif type == 'devAccessToken' :

        print('Pegar token de desenvolvimento')

getEnvironmentVar('ambient')