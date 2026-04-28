# MATA120 - Pedido de Compras

## Modulo

Compras

## Objetivo funcional

Registrar pedido formal de compra com fornecedor, produto, quantidade, preco, condicao de pagamento, entrega e regras de aprovacao quando existirem.

## Tabela principal

- SC7 - Pedido de compras

## Tabelas relacionadas

- SA2 - Fornecedores
- SB1 - Produtos
- SC1 - Solicitacoes de compra
- SD1/SF1 - Documento de entrada, quando recebido
- SE2 - Titulos a pagar, quando financeiro for gerado
- SF4 - TES

## Campos criticos

- C7_EMISSAO
- C7_FORNECE
- C7_LOJA
- C7_COND
- C7_FILENT
- C7_PRODUTO
- C7_QUANT
- C7_PRECO
- C7_TOTAL
- C7_CC
- C7_CONTA

## Tecnicas recomendadas

- ExecAuto para inclusao, alteracao e exclusao tecnica quando confirmado no ambiente.
- TIR para validar tela, grids, mensagens e aprovacoes visuais.
- PROBAT para regras isoladas de validacao de comprador, centro de custo, limite ou fornecedor.
- Consulta em SC7 como evidencia principal.

## Cenarios minimos

### Positivos

1. Incluir pedido valido com fornecedor, produto, quantidade e preco.
2. Incluir pedido com condicao de pagamento valida.
3. Incluir pedido com centro de custo quando aplicavel.
4. Validar pedido com aprovacao quando existir alçada.

### Negativos

1. Fornecedor inexistente ou bloqueado.
2. Produto inexistente ou inativo.
3. Quantidade zerada ou invalida.
4. Preco zerado ou fora de regra customizada.
5. Centro de custo invalido quando obrigatorio.

### Regressao

1. Pedido valido deve continuar gravando SC7.
2. Regras customizadas nao devem bloquear compras legitimas.
3. Integracao posterior com entrada nao deve ser afetada indevidamente.

## Evidencias esperadas

- Registro criado ou nao criado em SC7.
- Retorno do ExecAuto/FwModel, quando usado.
- Mensagem visual via TIR, quando aplicavel.
- Log da regra customizada, quando existir.

## Limitacoes

Confirmar campos obrigatorios, assinatura de rotina automatica, regras de alçada, pontos de entrada e parametros no ambiente antes de gerar automacao definitiva.
