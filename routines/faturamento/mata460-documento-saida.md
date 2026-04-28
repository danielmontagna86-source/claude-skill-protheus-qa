# MATA460 - Documento de Saida / Faturamento

## Modulo

Faturamento

## Objetivo funcional

Executar a geracao do documento de saida a partir de pedidos liberados ou operacoes comerciais/fiscais permitidas no ambiente, validando integracao com fiscal, estoque e financeiro.

## Tabelas principais

- SF2 - Cabecalho do documento de saida
- SD2 - Itens do documento de saida

## Tabelas relacionadas

- SC5 - Cabecalho do pedido de venda
- SC6 - Itens do pedido de venda
- SA1 - Clientes
- SB1 - Produtos
- SF4 - TES
- SE1 - Titulos a receber, quando gera financeiro
- SB2 - Saldos de estoque, quando movimenta estoque

## Campos criticos

- F2_DOC
- F2_SERIE
- F2_CLIENTE
- F2_LOJA
- F2_EMISSAO
- D2_DOC
- D2_SERIE
- D2_CLIENTE
- D2_LOJA
- D2_COD
- D2_QUANT
- D2_PRCVEN
- D2_TOTAL
- D2_TES

## Tecnicas recomendadas

- ExecAuto/FwModel apenas quando a assinatura e operacao estiverem confirmadas no ambiente.
- TIR para validar tela, parametros, mensagens e fluxo visual de faturamento.
- PROBAT para regras isoladas de validacao fiscal, comercial, estoque ou financeiro.
- Consulta em SF2/SD2/SE1/SB2 como evidencia.

## Cenarios minimos

### Positivos

1. Gerar documento de saida para pedido valido e liberado.
2. Gerar documento com TES que atualiza estoque, fiscal e financeiro conforme parametrizacao.
3. Validar geracao de titulo em SE1 quando a TES/condicao exigir.
4. Validar baixa de saldo em SB2 quando movimentar estoque.

### Negativos

1. Bloquear faturamento de pedido com cliente invalido ou restrito.
2. Bloquear item sem TES valida.
3. Bloquear pedido com saldo insuficiente, quando controle de estoque exigir.
4. Bloquear geracao fiscal quando parametro/cadastro estiver inconsistente.
5. Bloquear documento com produto invalido ou inativo.

### Regressao

1. Pedido valido deve continuar gerando SF2/SD2.
2. Customizacao nao deve impedir faturamento legitimo.
3. Integracao com SE1 e estoque deve permanecer coerente quando aplicavel.

## Customizacoes comuns

- Validacao de TES.
- Validacao fiscal por cliente/produto.
- Bloqueio comercial antes de faturar.
- Regras de estoque.
- Mensagens especificas no faturamento.
- Integracao com financeiro.

## Evidencias esperadas

- Documento criado ou bloqueado em SF2/SD2.
- Titulo criado ou nao criado em SE1 conforme regra.
- Saldo atualizado ou preservado em SB2 conforme cenario.
- Mensagem visual via TIR quando aplicavel.
- Log da customizacao quando existir.

## Limitacoes

Confirmar no ambiente se a rotina usada e MATA460, MATA460A ou outra variante do processo de documento de saida. Confirmar assinatura de automacao, campos obrigatorios, parametros fiscais e regras locais antes de gerar automacao definitiva.
