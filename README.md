# Bot de faturamento para cobranças B2B

Esse projeto é responsáve pela emissão de:
- Boleto
- Relação de ativos
- Nota fiscal

Para cada faturamento realizado, ele envia um email com as informações de cobrança.

## Fluxo de funcionamento e configuração

### Variaveis de ambiente

Esse projeto faz uso das variaveis de ambiente. a variavel myEnv é usada para desenpenhar apenas uma funcionalidade, informar se o ambiente é de produção ou desenvolvimento

- Para rodar o projeto em sua máquina com a variavel de ambinete, basta replicar o código abaixo:

Desenvolvimento:
```bash
   export MY_AMBIENT_VAR='dev'; python coletadedados.py
```

Produção:-
```bash
   export MY_AMBIENT_VAR='prod'; python coletadedados.py
```

**Atenção:**
<br>
Caso a variavel de ambinete não seja informada, a aplicação será iniciada no ambinete de produção.

Depois da MY_AMBIENT_VAR, temos mais duas variaveis. O objetivo delas é armazenar os seguintes tokens:

- Token de autenticação para a API de produção do Asaas
   - Nome: ASAAS_TOKEN

- Token de autenticação para a API de desenvolvimento
   - Nome: ASAAS_SANDBOX_TOKEN

As variaveis descritas acima, devem ficar declaradas dentro do arquivo ".env" conforme explicado.

### Fluxo de funcionamento

Para visualizar o fluxo de funcionamento da aplicação, basta acessar este [link](https://miro.com/app/live-embed/uXjVMsBAMo8=/?moveToViewport=20291,1806,9695,4691&embedId=125589149693).