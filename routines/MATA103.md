# MATA103 - Documento de Entrada

## Contexto

Rotina crítica do ciclo de compras. Valida recebimento de nota, fornecedor, produto, TES, pedido de compras, estoque, fiscal, financeiro, custos e contabilidade.

## Objetivo de QA

Garantir que o documento de entrada seja incluído ou bloqueado corretamente, sem gerar inconsistência em SF1, SD1, SB2, SE2, custos ou integrações fiscais.

## Tabelas principais

| Tabela | Uso |
|---|---|
| SF1 | Cabeçalho da entrada |
| SD1 | Itens da entrada |
| SA2 | Fornecedor |
| SB1 | Produto |
| SB2 | Saldo de estoque |
| SF4 | TES |
| SE2 | Financeiro a pagar |
| SC7 | Pedido de compras |
| SX3/SX7/SXB | Dicionário, gatilhos e consultas |

## Riscos

| Risco | Impacto |
|---|---|
| TES incorreta | Erro fiscal, estoque ou financeiro |
| Divergência com pedido não bloqueada | Entrada fora da negociação |
| Estoque atualizado indevidamente | Saldo/custo incorreto |
| Financeiro gerado incorretamente | Título errado no contas a pagar |
| Falta de rollback | Documento parcial |

## Cenários positivos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA103-POS-001 | Entrada com fornecedor, produto, TES e valores válidos | Documento gravado |
| MATA103-POS-002 | Entrada vinculada ao pedido sem divergência | Pedido atualizado |
| MATA103-POS-003 | Entrada que atualiza estoque | Saldo atualizado corretamente |
| MATA103-POS-004 | Entrada que gera financeiro | SE2 criado corretamente |

## Cenários negativos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA103-NEG-001 | Fornecedor bloqueado | Bloqueia gravação |
| MATA103-NEG-002 | Produto bloqueado | Rejeita item |
| MATA103-NEG-003 | TES inválida | Bloqueia operação |
| MATA103-NEG-004 | Quantidade acima da tolerância do pedido | Bloqueia ou exige aprovação |
| MATA103-NEG-005 | Preço acima da tolerância | Bloqueia ou exige aprovação |
| MATA103-NEG-006 | Documento duplicado | Impede duplicidade |

## Regressão

- Inclusão manual.
- Inclusão por ExecAuto/FwModel.
- Entrada com pedido.
- Entrada sem pedido, se permitida.
- Atualização de estoque.
- Geração de financeiro.
- Cálculo fiscal.
- Cálculo de custo.
- Multi-filial/armazém.

## Massa mínima

- Fornecedor válido e bloqueado.
- Produto válido e bloqueado.
- TES válida e inválida.
- Pedido pendente de recebimento.
- Pedido com divergência de preço/quantidade.
- Documento duplicado.
- Usuário fiscal/compras e usuário restrito.

## PROBAT

Testar regras isoladas de tolerância, duplicidade, TES, fornecedor, produto, estoque e geração financeira.

```text
Crie um teste PROBAT para validar bloqueio na MATA103 quando quantidade ou preço excedem a tolerância do pedido de compras.
```

## ExecAuto/FwModel

Validar retorno de sucesso/erro, rollback, gravação SF1/SD1, atualização SB2, geração SE2 e aderência à regra da interface.

## TIR/WebApp

Validar preenchimento, vínculo com pedido, mensagens de bloqueio, gravação válida e evidência visual dos cálculos.

## Evidências

- SF1/SD1 gerado ou bloqueado.
- SB2 antes/depois.
- SE2 gerado ou não.
- Print/log da mensagem.
- Resultado PROBAT.
- Log ExecAuto/FwModel.
- Evidência TIR.

## Prompt exemplo

```text
Monte matriz de testes para MATA103 com customização que bloqueia entrada quando preço ou quantidade divergem do pedido acima de 5%. Inclua positivos, negativos, regressão, massa, PROBAT, ExecAuto/FwModel, TIR e evidências.
```
