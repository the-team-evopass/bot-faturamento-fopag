from webbrowser import get
from termcolor import colored

from environment.environmentAccess import getEnvironmentVar
from services.baseURL.getBaseURL import getBaseURL

from functions.asaas.getCustomersList import getCustomersList
from functions.asaas.generateBiling import generateBiling
from functions.issueNf import generateIssueNf
from functions.asaas.generateExtract import generateExtractRequest


# services
from services.getAllCompanies.getAllCompanies import getAllCompanies
from services.getAllDependents.getAllDependents import getAllDependents
from services.getAllHolders.getAllHolders import getAllHolders

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

def runGetAllCompanies ():
    return getAllCompanies(configEnvironmentVars()['baseURL']['evopass'])

def runGetAllHolders ():
    return getAllHolders(configEnvironmentVars()['baseURL']['evopass'])

def runGetAllDependents ():
    return getAllDependents(configEnvironmentVars()['baseURL']['evopass'])