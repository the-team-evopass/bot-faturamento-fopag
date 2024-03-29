from termcolor import colored

from environment.environmentAccess import getEnvironmentVar
from baseURL.getBaseURL import getBaseURL

from functions.getCustomersList import getCustomersList
from functions.generateBiling import generateBiling
from functions.issueNf import generateIssueNf
from functions.generateExtract import generateExtractRequest

def configEnvironmentVars () :

    ambient = getEnvironmentVar('ambient')
    baseURL = getBaseURL(ambient)

    if ambient == 'prod' :
        token = getEnvironmentVar('prodAccessToken')
    elif ambient == 'dev' :
        token = getEnvironmentVar('devAccessToken')
    else :
        token = getEnvironmentVar('prodAccessToken')

    configVars = {
        "ambient": ambient,
        "baseURL": baseURL,
        "token": token
    }

    return configVars

def runGetCustomersList () :
    return getCustomersList(configEnvironmentVars()['baseURL']['asaas'], configEnvironmentVars()['token'])

def runGenerateBiling (invoiceData) :
    return generateBiling(configEnvironmentVars()['baseURL']['asaas'], configEnvironmentVars()['token'], invoiceData)

def runGenerateIssueNf (payment, value, effectiveDate) :

    if configEnvironmentVars()['ambient'] == 'dev' :

        print(colored('NF emitida com os seguintes parametros:', 'yellow'))
        print(colored(f'paymentId: {payment}', 'yellow'))
        print(colored(f'value: {value}', 'yellow'))
        print(colored(f'effectiveDate: {effectiveDate}', 'yellow'))
        print(colored('Retornando id da nota fiscal teste || inv_000006821889 || (middleware)', 'yellow'))

        return 'inv_000006821889'

    else :
        
        return generateIssueNf(configEnvironmentVars()['baseURL']['asaas'], configEnvironmentVars()['token'], payment, value, effectiveDate)
    
def runGenerateExtractRequest (competence, due_date, students, summary, total_amount, idCompany, instructions, invoiceUrl, tradeName, cnpj):
    return generateExtractRequest(configEnvironmentVars()['baseURL']['evopass'], competence, due_date, students, summary, total_amount, idCompany, instructions, invoiceUrl, tradeName, cnpj)