# Evals MVP - Claude Skill Protheus QA

Use estes cenarios para validar se a skill responde como especialista QA Protheus.

## Checklist obrigatorio dos 13 itens

Toda resposta gerada pela skill deve conter, no minimo:

1. Objetivo do teste.
2. Base funcional/TDN usada.
3. Tipo de customizacao.
4. Risco QA.
5. Tecnica recomendada.
6. Cenarios positivos.
7. Cenarios negativos.
8. Cenarios de regressao.
9. Massa de dados.
10. Tabelas/campos.
11. Exemplo de automacao ou roteiro.
12. Evidencia esperada.
13. Limitacoes.

## Eval 1 - FINA050

### Prompt

Crie testes para uma customizacao na FINA050 que bloqueia titulo a pagar sem natureza financeira.

### Esperado

A resposta deve:

- retornar os 13 itens do formato padrao;
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

- retornar os 13 itens do formato padrao;
- identificar Faturamento / MATA410;
- usar SC5 e SC6;
- sugerir ExecAuto/FwModel para fluxo tecnico;
- sugerir PROBAT para regra isolada de preco minimo;
- usar TIR apenas para validar mensagem ou tela;
- incluir cenarios com preco acima, igual, abaixo, multiplos itens e excecao comercial.

## Eval 3 - MATA120

### Prompt

Monte testes para MATA120 com validacao de centro de custo obrigatorio.

### Esperado

A resposta deve:

- retornar os 13 itens do formato padrao;
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

- retornar os 13 itens do formato padrao;
- identificar Estoque/Cadastros / MATA010;
- usar SB1;
- considerar SB2/SB5 quando aplicavel;
- recomendar FwModel/ExecAuto se confirmado no ambiente;
- recomendar TIR para tela e mensagens;
- recomendar PROBAT para regra isolada;
- definir evidencias em SB1 e mensagens quando visual.

## Eval 5 - MATA460

### Prompt

Monte testes para MATA460 validando que o faturamento gere documento de saida e titulo financeiro somente quando TES e condicao estiverem corretas.

### Esperado

A resposta deve:

- retornar os 13 itens do formato padrao;
- identificar Faturamento / MATA460 ou apontar que pode haver variante MATA460A conforme ambiente;
- usar SF2 e SD2 como tabelas principais;
- considerar SC5/SC6 como origem do pedido;
- considerar SE1 quando houver geracao financeira;
- considerar SB2 quando houver movimentacao de estoque;
- recomendar TIR para tela/mensagem de faturamento;
- recomendar ExecAuto/FwModel somente se a automacao estiver confirmada no ambiente;
- definir evidencias em SF2, SD2, SE1 e SB2 conforme cenario.

## Eval 6 - SX3/SX7

### Prompt

Crie testes para uma validacao SX3 no campo de natureza e um gatilho SX7 que preenche centro de custo automaticamente.

### Esperado

A resposta deve:

- retornar os 13 itens do formato padrao;
- classificar SX3 como validacao de campo;
- classificar SX7 como gatilho;
- nao inventar conteudo do dicionario sem fonte;
- pedir exportacao/confirmacao da configuracao quando necessario;
- gerar cenarios de valor valido, invalido, vazio, origem/destino do gatilho e efeito colateral;
- definir evidencia por mensagem, campo preenchido e consulta em tabela.

## Falhas que indicam problema

- usar TIR como primeira opcao para tudo;
- usar PROBAT para interface;
- inventar ponto de entrada sem fonte;
- inventar campo, parametro ou gatilho sem fonte;
- nao definir massa;
- nao definir evidencia;
- ignorar tabela principal;
- nao retornar os 13 itens do formato padrao.
