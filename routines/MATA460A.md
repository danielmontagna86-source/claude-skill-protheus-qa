# MATA460A - Documento de Saída / Faturamento

## Contexto

Rotina de faturamento/documento de saída. Fecha o ciclo de venda e impacta pedido, cliente, produto, TES, estoque, fiscal, financeiro e contabilidade.

## Objetivo de QA

Validar se o documento de saída é gerado, bloqueado ou rejeitado corretamente, mantendo consistência entre pedido de venda, cliente, produto, estoque, impostos e contas a receber.

## Tabelas principais

| Tabela | Uso |
|---|---|
| SF2 | Cabeçalho da saída |
| SD2 | Itens da saída |
| SC5/SC6 | Pedido de venda |
| SA1 | Cliente |
| SB1 | Produto |
| SB2 | Estoque |
| SF4 | TES |
| SE1 | Contas a receber |
| SX3/SX7/SXB | Dicionário, gatilhos e consultas |

## Riscos

- TES incorreta.
- Estoque baixado indevidamente.
- Financeiro não gerado.
- Documento duplicado.
- Imposto divergente.
- Pedido bloqueado faturado.
- Falta de rollback em integração.

## Cenários positivos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA460A-POS-001 | Faturar pedido liberado com dados válidos | SF2/SD2 gerados |
| MATA460A-POS-002 | Documento baixa estoque | SB2 atualizado |
| MATA460A-POS-003 | Documento gera financeiro | SE1 criado |
| MATA460A-POS-004 | Cálculo fiscal válido | Impostos coerentes |
| MATA460A-POS-005 | Faturamento parcial permitido | Saldo do pedido ajustado |

## Cenários negativos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA460A-NEG-001 | Pedido bloqueado | Impede faturamento |
| MATA460A-NEG-002 | Cliente bloqueado | Bloqueia documento |
| MATA460A-NEG-003 | Produto bloqueado | Rejeita item |
| MATA460A-NEG-004 | TES inválida | Bloqueia operação |
| MATA460A-NEG-005 | Estoque insuficiente | Bloqueia ou exige liberação |
| MATA460A-NEG-006 | Documento duplicado | Impede duplicidade |

## Regressão

- Faturamento total.
- Faturamento parcial.
- Geração por pedido de venda.
- Integração/ExecAuto/FwModel.
- Baixa de estoque.
- Geração de SE1.
- Cálculo fiscal.
- Documento duplicado.
- Multi-filial e armazém.

## Massa mínima

- Cliente válido e bloqueado.
- Produto válido e bloqueado.
- Pedido liberado e bloqueado.
- TES válida e inválida.
- Estoque suficiente e insuficiente.
- Documento duplicado.
- Usuário faturamento e usuário restrito.

## PROBAT

Testar pedido bloqueado, cliente, produto, TES, duplicidade, estoque, cálculo fiscal e geração financeira.

## ExecAuto/FwModel

Validar geração automatizada, retorno de erro, rollback, gravação SF2/SD2, baixa SB2, geração SE1 e aderência às regras da interface.

## TIR/WebApp

Validar tela, seleção do pedido, cenário inválido, mensagem de bloqueio, geração válida e evidência visual.

## Evidências

- SF2/SD2 gerado ou bloqueado.
- SB2 antes/depois.
- SE1 gerado ou não.
- Print/log da mensagem.
- Resultado PROBAT.
- Log ExecAuto/FwModel.
- Evidência TIR.

## Prompt exemplo

```text
Monte matriz de testes para MATA460A com customização que bloqueia faturamento quando o pedido está bloqueado, a TES é inválida ou o estoque é insuficiente. Inclua cenários, massa, PROBAT, ExecAuto/FwModel, TIR e evidências.
```
