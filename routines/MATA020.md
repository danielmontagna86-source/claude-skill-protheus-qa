# MATA020 - Cadastro de Fornecedores

## Contexto

Rotina base para cadastro e manutenção de fornecedores. Impacta compras, documento de entrada, contas a pagar, fiscal, retenções, pagamentos, banco, integração cadastral e auditoria.

## Objetivo de QA

Garantir que fornecedores sejam cadastrados, alterados, bloqueados ou rejeitados corretamente, respeitando campos obrigatórios, validações fiscais, regras financeiras, duplicidade e permissões.

## Tabelas principais

| Tabela | Uso |
|---|---|
| SA2 | Cadastro de fornecedores |
| SE2 | Títulos a pagar relacionados |
| SF1/SD1 | Documentos de entrada relacionados |
| SX3 | Campos e obrigatoriedade |
| SX7 | Gatilhos |
| SXB | Consultas padrão |

## Riscos

- Fornecedor duplicado.
- CNPJ/CPF inválido aceito.
- Dados fiscais ausentes.
- Banco/agência/conta incorretos.
- Fornecedor bloqueado usado em compras ou pagamentos.
- Alteração indevida por usuário sem permissão.
- Integração cadastral sem validação.

## Cenários positivos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA020-POS-001 | Incluir fornecedor com dados válidos | SA2 gravado |
| MATA020-POS-002 | Alterar endereço ou contato permitido | Alteração gravada |
| MATA020-POS-003 | Gatilho preenche dados fiscais/financeiros | Campos preenchidos |
| MATA020-POS-004 | Fornecedor apto para compras | Pode ser usado em fluxo posterior |

## Cenários negativos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA020-NEG-001 | CNPJ/CPF inválido | Bloqueia gravação |
| MATA020-NEG-002 | Fornecedor duplicado | Impede duplicidade |
| MATA020-NEG-003 | Campo fiscal obrigatório vazio | Bloqueia cadastro |
| MATA020-NEG-004 | Banco inválido | Rejeita dados financeiros |
| MATA020-NEG-005 | Usuário sem permissão altera campo crítico | Bloqueia alteração |
| MATA020-NEG-006 | Fornecedor bloqueado usado em compra | Bloqueia fluxo posterior |

## Regressão

- Inclusão manual.
- Alteração de fornecedor existente.
- Validação de CNPJ/CPF.
- Duplicidade.
- Gatilhos SX7.
- Consulta padrão SXB.
- Uso em MATA120/MATA103/FINA050.
- Integração/ExecAuto/FwModel.

## Massa mínima

- Fornecedor válido.
- Fornecedor duplicado.
- CNPJ/CPF inválido.
- Fornecedor bloqueado.
- Dados bancários válidos e inválidos.
- Usuário administrador e restrito.

## PROBAT

Testar validações isoladas de documento, duplicidade, campos fiscais, banco, bloqueio e permissões.

## ExecAuto/FwModel

Validar inclusão/alteração automatizada, retorno de erro, rollback, gravação SA2 e aderência à interface.

## TIR/WebApp

Validar tela, preenchimento, gatilhos, mensagens de erro e evidência visual.

## Evidências

- Registro SA2 criado, alterado ou bloqueado.
- Print/log de mensagem.
- Resultado PROBAT.
- Log ExecAuto/FwModel.
- Evidência TIR.

## Prompt exemplo

```text
Monte matriz de testes para MATA020 com customização que bloqueia fornecedor duplicado, exige dados fiscais e impede alteração de banco por usuário sem permissão.
```
