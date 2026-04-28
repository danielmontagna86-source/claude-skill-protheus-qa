# MATA030 - Cadastro de Produtos

## Contexto

Rotina base para cadastro e manutenção de produtos. Impacta compras, vendas, estoque, fiscal, custos, PCP, faturamento e integrações.

## Objetivo de QA

Garantir que o produto seja cadastrado ou bloqueado conforme regras de negócio, dicionário SX3, gatilhos SX7, validações fiscais e campos obrigatórios do cliente.

## Tabelas principais

| Tabela | Uso |
|---|---|
| SB1 | Cadastro de produtos |
| SB2 | Saldos por filial/armazém, quando aplicável |
| SF4 | TES relacionada em fluxos posteriores |
| SX3 | Campos e obrigatoriedade |
| SX7 | Gatilhos |
| SXB | Consultas padrão e fórmulas |

## Riscos

| Risco | Impacto |
|---|---|
| Produto sem NCM/grupo/unidade válida | Erro fiscal ou operacional |
| Campo obrigatório não validado | Cadastro inconsistente |
| Gatilho SX7 não testado | Preenchimento automático incorreto |
| Produto duplicado | Divergência de estoque/compras/vendas |
| Bloqueio mal definido | Produto vendido/comprado indevidamente |

## Cenários positivos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA030-POS-001 | Incluir produto com dados obrigatórios válidos | Produto gravado na SB1 |
| MATA030-POS-002 | Alterar descrição ou grupo conforme permissão | Alteração gravada |
| MATA030-POS-003 | Gatilho preenche campo fiscal/estoque | Campo preenchido corretamente |
| MATA030-POS-004 | Produto com controle de estoque válido | Cadastro aceito |

## Cenários negativos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA030-NEG-001 | Produto sem descrição | Bloqueia gravação |
| MATA030-NEG-002 | Unidade inválida | Rejeita cadastro |
| MATA030-NEG-003 | NCM obrigatório não informado | Bloqueia gravação |
| MATA030-NEG-004 | Grupo inválido | Bloqueia cadastro |
| MATA030-NEG-005 | Código duplicado | Impede duplicidade |
| MATA030-NEG-006 | Usuário sem permissão altera campo crítico | Bloqueia alteração |

## Regressão

- Inclusão manual.
- Alteração de produto existente.
- Validação SX3.
- Gatilhos SX7.
- Consulta padrão SXB.
- Produto ativo/inativo.
- Produto com estoque.
- Produto usado em compras/vendas.
- Usuário com e sem permissão.

## Massa mínima

- Produto novo válido.
- Produto duplicado.
- Unidade válida e inválida.
- Grupo válido e inválido.
- NCM válido e vazio.
- Usuário administrador e restrito.
- Produto com saldo em estoque.

## PROBAT

Testar validações isoladas de campos obrigatórios, duplicidade, NCM, unidade, grupo, bloqueio e permissões.

```text
Crie um teste PROBAT para validar que o cadastro MATA030 bloqueia produto sem NCM quando o grupo exige classificação fiscal obrigatória.
```

## ExecAuto/FwModel

Validar inclusão/alteração automatizada, retorno de erro, rollback, gravação SB1 e aderência às mesmas regras da interface.

## TIR/WebApp

Validar tela, preenchimento, gatilhos, mensagens de erro, gravação válida e evidência visual.

## Evidências

- Registro SB1 criado/alterado ou bloqueado.
- Print/log da mensagem.
- Resultado PROBAT.
- Log ExecAuto/FwModel.
- Evidência TIR.

## Prompt exemplo

```text
Monte matriz de testes para MATA030 com customização que exige NCM para produtos de revenda e bloqueia alteração de grupo por usuário sem permissão. Inclua cenários, massa, PROBAT, ExecAuto/FwModel, TIR e evidências.
```
