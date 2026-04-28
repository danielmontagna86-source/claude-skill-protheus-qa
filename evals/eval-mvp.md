# Evals MVP - Claude Skill Protheus QA

Use estes cenarios para validar se a skill responde como especialista QA Protheus.

## Eval 1 - FINA050

### Prompt

Crie testes para uma customizacao na FINA050 que bloqueia titulo a pagar sem natureza financeira.

### Esperado

A resposta deve:

- identificar Financeiro / FINA050;
- usar SE2 como tabela principal;
- recomendar ExecAuto como tecnica principal quando confirmado no ambiente;
- recomendar PROBAT apenas se a regra estiver isolada;
- recomendar TIR apenas para mensagem visual;
- gerar cenarios positivos, negativos e regressao;
- definir massa com fornecedor, natureza, emissao, vencimento e valor;
- definir evidencia em SE2 e log/retorno.

## Eval 2 - MATA410

### Prompt

Monte QA para customizacao na MATA410 que bloqueia pedido de venda com preco abaixo do minimo.

### Esperado

A resposta deve:

- identificar Faturamento / MATA410;
- usar SC5 e SC6;
- sugerir ExecAuto/FwModel para fluxo tecnico;
- sugerir PROBAT para regra isolada de preco minimo;
- usar TIR apenas para validar mensagem ou tela;
- incluir cenarios com preco acima, igual, abaixo, multiplos itens e excecao comercial.

## Eval 3 - MATA120

### Prompt

Crie cenarios para Pedido de Compras MATA120 com validacao de centro de custo obrigatorio.

### Esperado

A resposta deve:

- identificar Compras / MATA120;
- usar SC7;
- considerar fornecedor, produto, quantidade, preco e centro de custo;
- gerar cenarios positivo, negativo e regressivo;
- recomendar ExecAuto quando confirmado;
- definir evidencia em SC7.

## Eval 4 - MATA010

### Prompt

Crie um roteiro de testes para produto MATA010 com validacao de unidade de medida e armazem padrao.

### Esperado

A resposta deve:

- identificar Estoque/Cadastros / MATA010;
- usar SB1;
- considerar SB2/SB5 quando aplicavel;
- recomendar FwModel/ExecAuto se confirmado no ambiente;
- recomendar TIR para tela e mensagens;
- recomendar PROBAT para regra isolada;
- definir evidencias em SB1 e mensagens quando visual.

## Falhas que indicam problema

- usar TIR como primeira opcao para tudo;
- usar PROBAT para interface;
- inventar ponto de entrada sem fonte;
- nao definir massa;
- nao definir evidencia;
- ignorar tabela principal.
