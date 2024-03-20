def getBaseURL(myAmbient):

    ambient = myAmbient
    
    if ambient == 'prod':
        return {
            'asaas': 'https://api.asaas.com',
            'evopass': 'https://us-central1-api-evopass-d943e.cloudfunctions.net/v2'
        }
    elif ambient == 'dev':

        return {
            'asaas': 'https://sandbox.asaas.com/api',
            'evopass': 'https://us-central1-api-evopass-d943e.cloudfunctions.net/v2'
        } 
    
    else:
        
        return {
            'asaas': 'https://sandbox.asaas.com/api',
            'evopass': 'https://us-central1-api-evoppass-dev.cloudfunctions.net/v2'
        }