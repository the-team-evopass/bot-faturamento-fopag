def Abatimento_Imposto(valor_boleto_empresa, imposto):
    resultado = valor_boleto_empresa - (valor_boleto_empresa * imposto)
    return resultado
