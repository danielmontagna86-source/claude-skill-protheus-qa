# MATA010 - Cadastro de Produtos

## Modulo

Estoque / Cadastros

## Objetivo funcional

Manter cadastro de produtos e servicos usados por compras, estoque, faturamento, fiscal, custos e demais processos do Protheus.

## Tabela principal

- SB1 - Produtos

## Tabelas relacionadas

- SB2 - Saldos
- SB5 - Complementos
- SA2/SA5 - Fornecedor e produto x fornecedor
- SF4 - TES quando usado em fluxos fiscais/comerciais
- SC1/SC7/SC6/SD1/SD2 conforme processo

## Campos criticos

- B1_COD
- B1_DESC
- B1_TIPO
- B1_UM
- B1_LOCPAD
- B1_GRUPO
- B1_POSIPI
- B1_ORIGEM
- B1_RASTRO
- B1_PESO
- B1_CONTA

## Tecnicas recomendadas

- FwModel/ExecAuto quando confirmados no ambiente para cadastro tecnico.
- TIR para validar tela, abas, mensagens, browse e campos visuais.
- PROBAT para regras isoladas de validacao de codigo, tipo, estoque, fiscal ou custo.
- Consulta em SB1/SB2/SB5 como evidencia.

## Cenarios minimos

### Positivos

1. Incluir produto valido com codigo, descricao, tipo e unidade.
2. Alterar descricao ou dados complementares permitidos.
3. Validar produto com armazem padrao.
4. Validar produto usado em compras e faturamento.

### Negativos

1. Produto sem codigo.
2. Produto sem descricao.
3. Tipo de produto invalido.
4. Unidade invalida.
5. Armazem padrao invalido.
6. Regra de rastreabilidade sem massa/parametro adequado.

### Regressao

1. Produto valido deve continuar gravando SB1.
2. Customizacao nao deve bloquear produtos legitimos.
3. Fluxos posteriores de compra, venda e estoque nao devem ser afetados indevidamente.

## Evidencias esperadas

- Registro criado ou nao criado em SB1.
- Complemento ou saldo criado quando aplicavel ao processo.
- Retorno do FwModel/ExecAuto, quando usado.
- Mensagem visual via TIR, quando aplicavel.

## Limitacoes

Confirmar campos obrigatorios, parametros MV_*, rotina automatica, modelo MVC e regras locais antes de gerar automacao definitiva.
