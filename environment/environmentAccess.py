import os
from dotenv import load_dotenv

load_dotenv()

def getEnvironmentVar(type) :

    if type == 'ambient' :
      
        return os.environ.get('MY_AMBIENT_VAR')

    elif type == 'devAccessToken' :

        return os.environ.get('ASAAS_SANDBOX_TOKEN')

    elif type == 'prodAccessToken' :

        return os.environ.get('ASAAS_TOKEN')
    
    else :
        print(f'Erro ao acessar a variável de ambiente do tipo: {type} || (environmentAccess)')