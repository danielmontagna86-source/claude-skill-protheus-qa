# FINA050 - Contas a Pagar

## Contexto funcional

A rotina FINA050 é usada para manutenção de títulos de contas a pagar no Protheus. Ela costuma concentrar regras críticas envolvendo fornecedor, natureza financeira, vencimento, parcelas, impostos/retenções, centro de custo, aprovação e integração com processos posteriores de baixa, borderô, CNAB, contabilidade e fluxo de caixa.

## Objetivo da rotina no QA

Garantir que títulos a pagar sejam incluídos, alterados, bloqueados ou rejeitados conforme regras financeiras, fiscais, contábeis e cadastrais, mantendo rastreabilidade e evitando divergências em pagamentos, baixas e integrações bancárias.

## Principais tabelas envolvidas

| Tabela | Uso esperado |
|---|---|
| SE2 | Títulos a pagar |
| SA2 | Cadastro de fornecedores |
| SED | Naturezas financeiras |
| SE5 | Movimentos financeiros/baixas, quando aplicável em fluxo posterior |
| CT1/CTT | Contas contábeis e centros de custo, quando aplicável |
| SX3 | Dicionário de campos e obrigatoriedade |
| SX7 | Gatilhos |
| SXB | Consultas padrão e fórmulas |

> Validar nomes/tabelas conforme release, dicionário local e customizações do cliente. Não assumir estrutura fixa sem confirmar no ambiente.

## Pontos de entrada comuns

Os pontos de entrada variam por release, pacote e customização. Antes de propor código ou automação, confirmar no fonte/local do cliente ou documentação TDN da versão.

Áreas comuns de customização:

- validação antes da gravação do título;
- validação de fornecedor;
- validação de natureza financeira;
- obrigatoriedade de centro de custo;
- regras de vencimento;
- bloqueio por valor, filial, fornecedor ou tipo de título;
- cálculo ou validação de retenções;
- preenchimento automático de campos;
- rastreabilidade para fluxo de pagamento;
- integração com borderô, CNAB ou baixa financeira.

## Riscos de customização

| Risco | Impacto |
|---|---|
| Permitir título duplicado | Pagamento em duplicidade |
| Validar apenas interface e esquecer integração | Carga/ExecAuto grava título inválido |
| Natureza financeira errada | Erro contábil, fiscal ou gerencial |
| Vencimento inválido | Distorção de fluxo de caixa |
| Retenção calculada incorretamente | Erro fiscal e divergência de pagamento |
| Centro de custo obrigatório sem exceção | Bloqueio indevido de despesas legítimas |
| Alteração sem trilha de auditoria | Falha de rastreabilidade financeira |
| Bloqueio genérico sem mensagem clara | Usuário não identifica causa do erro |

## Cenários positivos

| ID | Cenário | Resultado esperado |
|---|---|---|
| FINA050-POS-001 | Incluir título com fornecedor ativo, natureza válida, valor positivo e vencimento válido | Título gravado na SE2 com sucesso |
| FINA050-POS-002 | Incluir título com centro de custo obrigatório informado | Título aceito e rastreável |
| FINA050-POS-003 | Incluir título parcelado com soma correta das parcelas | Parcelas gravadas com valores coerentes |
| FINA050-POS-004 | Alterar vencimento dentro de regra permitida | Vencimento atualizado corretamente |
| FINA050-POS-005 | Incluir título com retenção válida conforme regra do cliente | Retenção calculada/registrada conforme esperado |

## Cenários negativos

| ID | Cenário | Resultado esperado |
|---|---|---|
| FINA050-NEG-001 | Fornecedor bloqueado/inativo | Título não deve ser gravado |
| FINA050-NEG-002 | Natureza financeira inexistente ou bloqueada | Sistema deve bloquear gravação |
| FINA050-NEG-003 | Valor menor ou igual a zero | Sistema deve rejeitar título |
| FINA050-NEG-004 | Centro de custo obrigatório não informado | Gravação deve ser bloqueada |
| FINA050-NEG-005 | Título duplicado para fornecedor, prefixo, número, parcela e tipo | Sistema deve impedir duplicidade conforme regra |
| FINA050-NEG-006 | Vencimento inválido conforme política do cliente | Sistema deve bloquear ou exigir justificativa |
| FINA050-NEG-007 | Retenção divergente do cálculo esperado | Sistema deve rejeitar ou sinalizar inconsistência |

## Cenários de regressão

- Inclusão manual pela interface.
- Inclusão por integração/ExecAuto, quando existir.
- Alteração de vencimento.
- Alteração de natureza financeira.
- Alteração de centro de custo.
- Inclusão de título parcelado.
- Tentativa de duplicidade.
- Validação de fornecedor bloqueado.
- Validação multi-filial.
- Impacto posterior em borderô, baixa, CNAB ou fluxo de pagamento, quando usado pelo cliente.

## Massa de dados mínima

| Tipo | Massa |
|---|---|
| Fornecedor válido | SA2 ativo e permitido para lançamento financeiro |
| Fornecedor bloqueado | SA2 com regra que impeça geração de título |
| Natureza válida | SED ativa e compatível com o tipo de despesa |
| Natureza inválida | SED inexistente, bloqueada ou incompatível |
| Centro de custo válido | CTT ativo e aceito pela regra |
| Centro de custo inválido | CTT bloqueado, inexistente ou incompatível |
| Título duplicado | Mesma chave funcional usada pela regra do cliente |
| Título com retenção | Massa com imposto/retenção esperada |
| Usuário financeiro | Permissão para incluir/alterar título |
| Usuário restrito | Sem permissão ou sem alçada para regra crítica |

## Estratégia PROBAT

Usar PROBAT para testar regras isoladas ADVPL/TLPP, principalmente quando a customização estiver em função desacoplada.

Casos ideais:

- validação de duplicidade de título;
- validação de fornecedor bloqueado;
- obrigatoriedade de centro de custo;
- validação de natureza financeira;
- regra de vencimento;
- cálculo/validação de retenções;
- regra de alçada por valor.

Exemplo de prompt para gerar teste PROBAT:

```text
Crie um teste PROBAT para uma função ADVPL que valida se um título da FINA050 deve ser bloqueado quando fornecedor está inativo ou quando a natureza financeira exige centro de custo e o campo está vazio.
```

## Estratégia ExecAuto/FwModel

Usar ExecAuto/FwModel quando o cliente cria títulos por integração, carga, importação ou processo automático.

Validar:

- retorno de sucesso/erro;
- gravação correta na SE2;
- rollback em caso de falha;
- mensagens retornadas;
- preenchimento automático de campos;
- consistência com a mesma regra aplicada na interface;
- impacto em fluxo posterior de pagamento, quando aplicável.

## Estratégia TIR/WebApp

Usar TIR quando a regra precisa ser comprovada pela interface.

Validar:

- acesso à rotina;
- preenchimento de campos principais;
- tentativa de gravação inválida;
- mensagem exibida ao usuário;
- gravação válida;
- alteração permitida;
- evidência visual da rejeição ou sucesso.

## Evidências esperadas

- Print/log da inclusão válida.
- Print/log da mensagem de bloqueio.
- Registro SE2 gerado ou não gerado, conforme cenário.
- Resultado PROBAT da regra isolada.
- Log da automação ExecAuto/FwModel, quando aplicável.
- Evidência TIR para comportamento de interface.
- Massa usada no teste.
- Release/versão do Protheus, ambiente e filial.

## Checklist rápido para analista

```text
[ ] Confirme release e dicionário local.
[ ] Confirme campos obrigatórios SX3.
[ ] Confirme gatilhos SX7.
[ ] Confirme regra de duplicidade.
[ ] Confirme regra de natureza financeira.
[ ] Confirme regra de centro de custo.
[ ] Confirme regra de retenção/impostos.
[ ] Confirme se há integração ou carga automática.
[ ] Teste interface e automação, se ambas existirem.
[ ] Gere evidência antes/depois.
```

## Prompt exemplo para uso da skill

```text
Monte uma matriz de testes para a rotina FINA050 considerando uma customização que bloqueia títulos duplicados e exige centro de custo quando a natureza financeira pertence ao grupo DESPESA_OPERACIONAL. Inclua cenários positivos, negativos, regressão, massa de dados, estratégia PROBAT, ExecAuto/FwModel e TIR.
```
