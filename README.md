# Bot de faturamento para cobranças em boletos

Esse projeto é responsáve pela emissão de:
- Boleto
- Relação de ativos
- Nota fiscal

Para cada faturamento realizado, ele envia um email com as informações de cobrança.

## Explicando fluxo de funcionamento e configuração

### Variaveis de ambiente

Esse projeto faz uso das variaveis de ambiente. a variavel myEnv é usada para desenpenhar apenas uma funcionalidade, informar se o ambiente é de produção ou desenvolvimento

- Para rodar o projeto em sua máquina com a variavel de ambinete, basta replicar o código abaixo:

Para rodar em desenvolvimento:
```bash
   export myEnv='dev'; python functions/environment/environmentAccess.py
```

Para rodar em produção:
```bash

   export myEnv='dev'; python functions/environment/environmentAccess.py
   
```

Atenção!
Caso a variavel de ambinete não seja informada, a aplicação será iniciada no ambinete de produção.

### Fluxo de funcionamento

Para visualizar o fluxo de funcionamento da aplicação, basta acessar este [link](https://miro.com/app/live-embed/uXjVMsBAMo8=/?moveToViewport=20291,1806,9695,4691&embedId=125589149693).
