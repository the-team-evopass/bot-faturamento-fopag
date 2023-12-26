def findIdCustumerByCNPJ(clientes, cpf_cnpj_pesquisado):

    for cliente in clientes:
        if cliente.get('cpfCnpj') == cpf_cnpj_pesquisado:
            return cliente.get('id')
    return False