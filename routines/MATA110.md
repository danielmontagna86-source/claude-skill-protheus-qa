# MATA110 - Solicitação de Compras

## Contexto

Rotina para criação e manutenção de solicitações de compra. Pode ser a origem do ciclo de compras e impacta aprovação, pedido de compra, estoque, orçamento, centro de custo e alçadas.

## Objetivo de QA

Garantir que solicitações sejam criadas, alteradas, aprovadas, bloqueadas ou rejeitadas corretamente, respeitando produto, quantidade, centro de custo, alçada, status e fluxo posterior para pedido de compra.

## Tabelas principais

| Tabela | Uso |
|---|---|
| SC1 | Solicitações de compra |
| SB1 | Produto |
| SB2 | Saldos/necessidade de estoque |
| SC7 | Pedido de compra gerado posteriormente |
| SA2 | Fornecedor em etapas posteriores |
| SX3/SX7/SXB | Dicionário, gatilhos e consultas |

## Riscos

- Solicitação sem aprovação gerar pedido.
- Produto inválido ou bloqueado.
- Quantidade incorreta.
- Centro de custo inválido.
- Alçada ignorada.
- Solicitação duplicada.
- Integração sem validar status.

## Cenários positivos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA110-POS-001 | Incluir solicitação com produto e quantidade válidos | SC1 gravado |
| MATA110-POS-002 | Solicitação com centro de custo válido | Centro/rateio mantido |
| MATA110-POS-003 | Solicitação aprovada segue para pedido | Fluxo posterior habilitado |
| MATA110-POS-004 | Alteração permitida antes da aprovação | Alteração gravada |

## Cenários negativos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA110-NEG-001 | Produto bloqueado | Rejeita item |
| MATA110-NEG-002 | Quantidade zero ou negativa | Bloqueia gravação |
| MATA110-NEG-003 | Centro de custo inválido | Bloqueia solicitação |
| MATA110-NEG-004 | Usuário sem alçada aprova/libera | Bloqueia ação |
| MATA110-NEG-005 | Solicitação duplicada | Sinaliza ou bloqueia |
| MATA110-NEG-006 | Alterar solicitação aprovada sem permissão | Bloqueia alteração |

## Regressão

- Inclusão manual.
- Alteração de solicitação.
- Aprovação e reprovação.
- Cancelamento.
- Geração de pedido MATA120.
- Integração/ExecAuto/FwModel.
- Multi-filial e centro de custo.

## Massa mínima

- Produto válido e bloqueado.
- Centro de custo válido e inválido.
- Usuário solicitante, aprovador e restrito.
- Solicitação pendente, aprovada e cancelada.
- Solicitação duplicada.

## PROBAT

Testar produto, quantidade, centro de custo, alçada, duplicidade e status da solicitação.

## ExecAuto/FwModel

Validar inclusão/alteração automatizada, retorno de erro, rollback, gravação SC1 e aderência às regras da interface.

## TIR/WebApp

Validar tela, preenchimento, aprovação, bloqueios, mensagens e evidência visual.

## Evidências

- Registro SC1 criado, alterado ou bloqueado.
- Status da solicitação.
- Print/log da mensagem.
- Resultado PROBAT.
- Log ExecAuto/FwModel.
- Evidência TIR.

## Prompt exemplo

```text
Monte matriz de testes para MATA110 com customização que exige centro de custo e bloqueia geração de pedido quando a solicitação não está aprovada. Inclua cenários, massa, PROBAT, ExecAuto/FwModel, TIR e evidências.
```
