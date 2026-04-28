# Roadmap de Rotinas Protheus para QA

Este roadmap organiza a evolução da skill `testing-protheus-routines` por rotinas Protheus de maior impacto funcional e risco de regressão.

## Critério de priorização

A prioridade considera:

- impacto financeiro e fiscal;
- volume transacional;
- frequência de customizações ADVPL/TLPP;
- uso de pontos de entrada;
- dependência de SX3, SX7, SXB, gatilhos e validações;
- aderência a ExecAuto, FwModel, PROBAT e TIR;
- facilidade de gerar cenários reutilizáveis.

## Lote 1 - MVP técnico vendável

| Prioridade | Módulo | Rotina | Nome funcional | Foco de QA |
|---|---|---|---|---|
| P0 | Compras | MATA120 | Pedido de Compras | Alçada, produto, fornecedor, TES, centro de custo, aprovação e integração |
| P0 | Financeiro | FINA050 | Contas a Pagar | Inclusão, alteração, baixa, retenções, vencimento, natureza e rastreabilidade |
| P0 | Faturamento | MATA410 | Pedido de Venda | Cliente, produto, TES, preço, estoque, bloqueios e liberação |
| P1 | Estoque/Custos | MATA103 | Documento de Entrada | TES, impostos, estoque, financeiro, custo e integração contábil |
| P1 | Cadastros | MATA030 | Produto | Validações SX3, unidade, grupo, NCM, rastreabilidade e impacto em compras/vendas |

## Lote 2 - Cobertura operacional

| Prioridade | Módulo | Rotina | Nome funcional | Foco de QA |
|---|---|---|---|---|
| P1 | Compras | MATA110 | Solicitação de Compras | Aprovação, necessidade, centro de custo, comprador e geração de pedido |
| P1 | Financeiro | FINA070 | Contas a Receber | Títulos, baixa, juros, cliente, natureza e integração com faturamento |
| P1 | Faturamento | MATA460A | Documento de Saída | Geração de nota, impostos, financeiro, estoque e rejeições |
| P2 | Estoque | MATA220 | Movimentação Interna | Saldos, armazém, lote, custo médio e rastreabilidade |
| P2 | Cadastros | MATA020 | Fornecedor | Dados fiscais, duplicidade, bloqueio, validações e impacto em compras/financeiro |

## Lote 3 - Especialização por automação

| Prioridade | Módulo | Rotina | Técnica principal | Entregável esperado |
|---|---|---|---|---|
| P1 | Compras | MATA120 | ExecAuto/FwModel | Template de inclusão e alteração automatizada |
| P1 | Financeiro | FINA050 | ExecAuto/PROBAT | Regras isoladas e roteiro funcional |
| P1 | Faturamento | MATA410 | FwModel/TIR | Validação de interface e modelo |
| P2 | Estoque | MATA103 | ExecAuto/FwModel | Validação de integração fiscal/estoque/financeiro |
| P2 | Cadastros | MATA030 | PROBAT/SX3 | Validação de campos obrigatórios e regras cadastrais |

## Estrutura sugerida por rotina

Cada rotina deve ter um arquivo dedicado em `routines/<rotina>.md` com:

1. Contexto funcional.
2. Objetivo da rotina.
3. Principais tabelas envolvidas.
4. Pontos de entrada comuns.
5. Riscos de customização.
6. Cenários positivos.
7. Cenários negativos.
8. Cenários de regressão.
9. Massa de dados.
10. Estratégia PROBAT.
11. Estratégia ExecAuto/FwModel.
12. Estratégia TIR/WebApp.
13. Evidências esperadas.
14. Prompt exemplo para uso da skill.

## Ordem recomendada de implementação

1. `routines/MATA120.md`
2. `routines/FINA050.md`
3. `routines/MATA410.md`
4. `routines/MATA103.md`
5. `routines/MATA030.md`

## Meta do lote 1

Transformar a skill em uma base prática para analistas Protheus que precisam gerar rapidamente:

- matriz de testes;
- massa de dados;
- roteiro técnico;
- automação inicial;
- evidências;
- checklist de regressão;
- análise de risco da customização.
