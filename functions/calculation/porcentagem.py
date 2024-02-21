def Abatimento_Imposto(valor_boleto_empresa, imposto):
    valor_imposto = valor_boleto_empresa * imposto
    resultado = valor_boleto_empresa - valor_imposto
    return resultado
