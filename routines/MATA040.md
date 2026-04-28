# MATA040 - Cadastro de Clientes

## Contexto

Rotina base para cadastro e manutenção de clientes. Impacta pedido de venda, faturamento, contas a receber, crédito, cobrança, fiscal, expedição e integrações comerciais.

## Objetivo de QA

Garantir que clientes sejam cadastrados, alterados, bloqueados ou rejeitados corretamente, respeitando campos obrigatórios, validações fiscais, limite de crédito, duplicidade e permissões.

## Tabelas principais

| Tabela | Uso |
|---|---|
| SA1 | Cadastro de clientes |
| SC5/SC6 | Pedidos de venda relacionados |
| SF2/SD2 | Documentos de saída relacionados |
| SE1 | Títulos a receber |
| SX3 | Campos e obrigatoriedade |
| SX7 | Gatilhos |
| SXB | Consultas padrão |

## Riscos

- Cliente duplicado.
- CNPJ/CPF inválido aceito.
- Limite de crédito incorreto.
- Cliente bloqueado vendido/faturado indevidamente.
- Dados fiscais ausentes.
- Alteração indevida por usuário sem permissão.
- Integração cadastral ignorando validações.

## Cenários positivos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA040-POS-001 | Incluir cliente com dados válidos | SA1 gravado |
| MATA040-POS-002 | Alterar contato/endereço permitido | Alteração gravada |
| MATA040-POS-003 | Gatilho preenche dados fiscais/comerciais | Campos preenchidos |
| MATA040-POS-004 | Cliente apto para venda | Pode ser usado em pedido |

## Cenários negativos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA040-NEG-001 | CNPJ/CPF inválido | Bloqueia gravação |
| MATA040-NEG-002 | Cliente duplicado | Impede duplicidade |
| MATA040-NEG-003 | Campo fiscal obrigatório vazio | Bloqueia cadastro |
| MATA040-NEG-004 | Limite de crédito inválido | Rejeita alteração |
| MATA040-NEG-005 | Usuário sem permissão altera crédito/bloqueio | Bloqueia alteração |
| MATA040-NEG-006 | Cliente bloqueado usado em venda | Bloqueia fluxo posterior |

## Regressão

- Inclusão manual.
- Alteração de cliente existente.
- Validação de CNPJ/CPF.
- Duplicidade.
- Limite de crédito.
- Gatilhos SX7.
- Consulta padrão SXB.
- Uso em MATA410/MATA460A/FINA070.
- Integração/ExecAuto/FwModel.

## Massa mínima

- Cliente válido.
- Cliente duplicado.
- CNPJ/CPF inválido.
- Cliente bloqueado.
- Limite de crédito válido e inválido.
- Usuário administrador, comercial e restrito.

## PROBAT

Testar validações isoladas de documento, duplicidade, limite de crédito, bloqueio, campos fiscais e permissões.

## ExecAuto/FwModel

Validar inclusão/alteração automatizada, retorno de erro, rollback, gravação SA1 e aderência à interface.

## TIR/WebApp

Validar tela, preenchimento, gatilhos, mensagens de erro e evidência visual.

## Evidências

- Registro SA1 criado, alterado ou bloqueado.
- Print/log de mensagem.
- Resultado PROBAT.
- Log ExecAuto/FwModel.
- Evidência TIR.

## Prompt exemplo

```text
Monte matriz de testes para MATA040 com customização que bloqueia cliente duplicado, exige dados fiscais e impede alteração de limite de crédito por usuário sem permissão.
```
