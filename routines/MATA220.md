# MATA220 - Movimentações Internas de Estoque

## Contexto

Rotina usada para movimentações internas de estoque, transferências, ajustes e movimentações entre locais/armazéns, conforme configuração. Impacta saldo físico, custo, rastreabilidade, lote/série, localização e integrações operacionais.

## Objetivo de QA

Garantir que movimentações internas sejam incluídas, alteradas, canceladas ou rejeitadas corretamente, respeitando saldo, produto, armazém, local, lote/série, custo, filial, permissões e regras de estoque.

## Tabelas principais

| Tabela | Uso |
|---|---|
| SB1 | Cadastro de produtos |
| SB2 | Saldos por produto/armazém |
| SD3 | Movimentos internos |
| SB8/SBF | Lote, endereço ou rastreio, quando usado |
| SX3 | Campos e obrigatoriedade |
| SX7 | Gatilhos |
| SXB | Consultas padrão |

## Riscos

- Movimentação sem saldo disponível.
- Produto bloqueado movimentado.
- Armazém/local inválido.
- Lote/série ignorado.
- Custo divergente.
- Cancelamento sem estornar saldo.
- Movimento duplicado via integração.
- Falha de rollback em múltiplos itens.

## Cenários positivos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA220-POS-001 | Movimentar produto com saldo disponível | SD3 gerado e SB2 atualizado |
| MATA220-POS-002 | Transferir entre armazéns válidos | Origem reduzida e destino acrescido |
| MATA220-POS-003 | Movimentar produto com lote válido | Rastreio mantido |
| MATA220-POS-004 | Cancelar movimento permitido | Saldo revertido |
| MATA220-POS-005 | Movimento com múltiplos itens válidos | Todos os itens processados |

## Cenários negativos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA220-NEG-001 | Produto inexistente ou bloqueado | Bloqueia item |
| MATA220-NEG-002 | Quantidade zero ou negativa | Bloqueia gravação |
| MATA220-NEG-003 | Saldo insuficiente | Bloqueia movimentação |
| MATA220-NEG-004 | Armazém/local inválido | Rejeita movimento |
| MATA220-NEG-005 | Lote/série obrigatório ausente | Bloqueia gravação |
| MATA220-NEG-006 | Usuário sem permissão cancela movimento | Bloqueia cancelamento |
| MATA220-NEG-007 | Falha em item intermediário | Executa rollback consistente |

## Regressão

- Inclusão manual.
- Cancelamento/estorno.
- Transferência entre armazéns.
- Produto com e sem controle de lote.
- Produto com saldo insuficiente.
- Multi-filial.
- Integração/ExecAuto/FwModel.
- Validação de custo e saldo.

## Massa mínima

- Produto válido com saldo.
- Produto sem saldo.
- Produto bloqueado.
- Armazém/local válido e inválido.
- Produto com lote/série.
- Usuário autorizado e restrito.
- Movimento com múltiplos itens.

## PROBAT

Testar saldo, produto, quantidade, armazém/local, lote/série, custo, cancelamento e rollback.

## ExecAuto/FwModel

Validar inclusão automatizada, retorno de erro, rollback, geração SD3, atualização SB2 e aderência às regras da interface.

## TIR/WebApp

Validar tela, seleção de produto, origem/destino, mensagens, bloqueios, cancelamento e evidência visual.

## Evidências

- SB2 antes/depois.
- SD3 gerado ou estornado.
- Rastreio de lote/série, quando aplicável.
- Print/log de mensagem.
- Resultado PROBAT.
- Log ExecAuto/FwModel.
- Evidência TIR.

## Prompt exemplo

```text
Monte matriz de testes para MATA220 com customização que bloqueia movimentação sem saldo, exige lote quando obrigatório e valida rollback em movimento com múltiplos itens. Inclua cenários, massa, PROBAT, ExecAuto/FwModel, TIR e evidências.
```
