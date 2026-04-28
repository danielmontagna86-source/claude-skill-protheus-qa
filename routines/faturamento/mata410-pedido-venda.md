# MATA410 - Pedido de Venda

## Modulo

Faturamento

## Objetivo funcional

Formalizar pedidos de venda com cliente, itens, preco, desconto, condicao de pagamento, TES e integracao posterior com documento de saida e financeiro.

## Tabelas principais

- SC5 - Cabecalho do pedido
- SC6 - Itens do pedido

## Tabelas relacionadas

- SA1 - Clientes
- SB1 - Produtos
- SF4 - TES
- SE4 - Condicoes de pagamento
- SE1 - Titulos a receber, quando faturado
- SD2/SF2 - Documento de saida, quando faturado

## Campos criticos

- C5_NUM
- C5_CLIENTE
- C5_LOJACLI
- C5_CONDPAG
- C5_TIPO
- C6_PRODUTO
- C6_QTDVEN
- C6_PRCVEN
- C6_VALOR
- C6_TES

## Tecnicas recomendadas

- ExecAuto para inclusao, alteracao e exclusao tecnica do pedido, quando confirmado no ambiente.
- FwModel quando houver modelo MVC aplicavel.
- PROBAT para regras isoladas como preco minimo, desconto, comissao ou validacao comercial.
- TIR para validar tela, mensagem, browse, botoes e experiencia visual.
- Consulta em SC5/SC6 como evidencia principal.

## Cenarios minimos

### Positivos

1. Incluir pedido valido com cliente, produto, TES, condicao e preco.
2. Incluir pedido com multiplos itens validos.
3. Validar regra de preco quando existir customizacao.
4. Validar fluxo posterior quando houver faturamento completo.

### Negativos

1. Cliente invalido ou com restricao comercial.
2. Produto inexistente ou inativo.
3. Item sem TES quando TES for obrigatoria.
4. Preco fora da regra customizada.
5. Condicao de pagamento invalida.

### Regressao

1. Pedido valido deve continuar gravando SC5/SC6.
2. Customizacao nao deve afetar pedidos legitimos.
3. Fluxo posterior de faturamento nao deve ser impactado indevidamente.

## Customizacoes comuns

- Validacao de preco minimo.
- Validacao por cliente.
- Validacao de TES.
- Manipulacao de parcelas.
- Regra de comissao.
- Integracao com financeiro ou analise comercial.

## Evidencias esperadas

- SC5 criado ou nao criado conforme cenario.
- SC6 criado ou nao criado conforme cenario.
- Retorno do ExecAuto/FwModel.
- Mensagem visual via TIR quando aplicavel.
- Log da customizacao quando existir.

## Limitacoes

Confirmar pontos de entrada, assinatura de ExecAuto, campos obrigatorios, parametros e regras comerciais no ambiente antes de gerar automacao definitiva.
