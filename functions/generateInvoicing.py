from datetime import datetime, timedelta
from termcolor import colored
from functions.asaas.criarCobranca import criar_cobranca
from middleware import runGenerateExtractRequest, runGenerateIssueNf


def GenerateInvoicing(valor_boleto_empresa, empresa_cnpj, data_vencimento,competencia_mes_ano,dados_extrato,dados_relatorio,valor_soma_total,empresa_id,empresa_tradeName):
    if valor_boleto_empresa != 0:
        billingResponse = criar_cobranca(empresa_cnpj, valor_boleto_empresa, data_vencimento)
        
        print(colored(billingResponse['billingURL'], 'green'))

        extractObservation = '''
            Prezado(a) cliente,
            Para visualizar e efetuar o pagamento do boleto, acesse o link fornecido.
            Qualquer problema ou dificuldade, entre em contato conosco.
            Agradecemos pela sua atenção.
        '''

        # Função para emissão de NF
        runGenerateIssueNf(billingResponse['billingID'], valor_boleto_empresa, datetime.now().strftime('%Y-%m-%d'))

        #Estou gerando o PDF aqui
        runGenerateExtractRequest(competencia_mes_ano, data_vencimento, dados_extrato, dados_relatorio, valor_soma_total, empresa_id, extractObservation, billingResponse['billingURL'], empresa_tradeName, empresa_cnpj)
        
        # myContentEmail = render_html(empresa_tradeName, competencia_mes_ano, str(valor_soma_total), billingResponse['billingURL'], 'inv_000006811891')
        # send_email('Teste do bot de faturamento', 'felipe@evopass.app.br', myContentEmail)

        print(colored('-------------------------------------------------------------------------------', 'yellow', 'on_green', ['underline']))

    else:
        print('Erro ao gerar cobrança, valor do boleto igual a 0 (coletadedados) ou empresa não tem titulares ativos')
        print('-------------------------------------------------------------------------------')
