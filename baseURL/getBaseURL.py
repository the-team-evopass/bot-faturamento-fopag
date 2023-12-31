def getBaseURL(myAmbient):
    ambient = myAmbient
    
    if ambient == 'prod':
        return 'https://api.asaas.com'
    elif ambient == 'dev':
        return 'https://sandbox.asaas.com/api'
    else:
        return 'https://api.asaas.com'