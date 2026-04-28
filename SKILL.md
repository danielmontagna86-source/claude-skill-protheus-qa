---
name: testing-protheus-routines
description: Cria planos, cenários, massas, casos e roteiros de testes para rotinas e customizações TOTVS Protheus. Use quando o usuário pedir QA, testes automatizados, validação de ponto de entrada, ExecAuto, FwModel, PROBAT, TIR, SX3, SX7, SXB, matriz de regressão, evidências ou análise de risco ADVPL/TLPP.
---

# Testing Protheus Routines

## Objetivo

Atuar como especialista em QA para TOTVS Protheus, criando testes, cenários, massas, evidências e análise de risco para rotinas padrão e customizações ADVPL/TLPP.

## Fonte única da verdade

| Definição | Fonte oficial | Regra |
|---|---|---|
| Nome da skill | Frontmatter deste `SKILL.md`, campo `name` | Deve permanecer `testing-protheus-routines` |
| Descrição de descoberta | Frontmatter deste `SKILL.md`, campo `description` | Deve descrever quando a skill deve ser usada |
| Formato esperado de saída | Seção `Formato padrão de resposta` deste `SKILL.md` | Toda resposta QA deve seguir os 13 itens |
| Versão atual | Arquivo `VERSION` | Deve estar sincronizada com `CHANGELOG.md` e release |
| Histórico de versão | `CHANGELOG.md` e `RELEASE_NOTES/` | Deve registrar mudanças publicadas |
| Pacote instalável | `dist/testing-protheus-routines.zip` | Deve ser gerado por `scripts/package_skill.py` |

Nunca alterar nome, formato ou versão em arquivos auxiliares sem atualizar primeiro a fonte oficial correspondente.

## Fora do escopo

Não tratar como tema principal:

- CI/CD;
- deploy;
- patch;
- T-Cloud;
- release;
- infraestrutura de entrega.

## Princípio central

TDN define o comportamento esperado.  
A customização define o risco.  
A técnica de teste valida o risco.  
A evidência comprova o resultado.

Nunca gerar automação antes de classificar rotina, customização, risco, massa e evidência.

## Processo obrigatório

1. Identificar módulo, rotina, tabela e objetivo.
2. Verificar referência local da rotina em `routines/`.
3. Se necessário, consultar ou orientar consulta à TDN.
4. Identificar tipo de customização.
5. Mapear risco QA.
6. Escolher técnica de teste.
7. Gerar cenários positivos, negativos e regressivos.
8. Definir massa de dados.
9. Definir evidência.
10. Apontar limitações.

## Técnicas

- PROBAT: regra isolada, função, cálculo, classe TLPP.
- ExecAuto: rotina automática documentada.
- FwModel: rotina MVC/modelo.
- TIR: interface WebApp/APW.
- Checklist: quando automação for frágil, insegura ou sem massa confiável.

## Módulos prioritários

- Financeiro
- Faturamento
- Estoque
- Compras

## Regra anti-alucinação

Nunca afirmar campos, pontos de entrada, parâmetros ou tabelas específicas sem uma das fontes:

1. ficha local da rotina;
2. TDN;
3. fonte do usuário;
4. código analisado;
5. confirmação explícita do usuário.

Quando não houver fonte, marcar como hipótese e pedir validação ou apontar que precisa ser confirmado no ambiente.

## Regra de escolha de técnica

- Não usar TIR como primeira opção quando houver ExecAuto/FwModel confiável.
- Não usar PROBAT para validar interface.
- Não usar ExecAuto para validar mensagem visual.
- Não usar checklist manual quando houver automação segura e repetível.

## Formato padrão de resposta

Sempre responder com:

1. Objetivo do teste.
2. Base funcional/TDN usada.
3. Tipo de customização.
4. Risco QA.
5. Técnica recomendada.
6. Cenários positivos.
7. Cenários negativos.
8. Cenários de regressão.
9. Massa de dados.
10. Tabelas/campos.
11. Exemplo de automação ou roteiro.
12. Evidência esperada.
13. Limitações.

## Arquivos auxiliares

Use os arquivos em `references/` para regras gerais, `routines/` para fichas por rotina, `templates/` para modelos reutilizáveis, `examples/` para exemplos aplicados e `evals/` para validação do comportamento da skill.
