# Uso da Claude Skill Protheus QA

## Objetivo

Esta skill ajuda Claude a atuar como especialista em QA para rotinas e customizações TOTVS Protheus.

Ela deve transformar uma solicitação genérica como:

```text
Monte testes para MATA120.
```

em uma resposta estruturada com:

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

## Fonte única da verdade para uso

| Item | Fonte oficial |
|---|---|
| Nome da skill | `SKILL.md` > frontmatter `name` |
| Versão atual | `VERSION` |
| Formato esperado de saída | `SKILL.md` > `Formato padrão de resposta` |
| Critérios de aceite | `evals/eval-mvp.md` |
| Exemplos de prompt | Este arquivo e `examples/` |

## Prompts recomendados e critérios de aceite

| ID | Prompt | Eval correspondente | Critério de aceite resumido |
|---|---|---|---|
| EX-FIN-001 | `Crie testes para uma customização na FINA050 que bloqueia título a pagar sem natureza financeira.` | `evals/eval-mvp.md` > Eval 1 | Deve classificar Financeiro/FINA050, usar SE2, retornar 13 itens, definir massa e evidência |
| EX-FAT-001 | `Monte QA para customização na MATA410 que bloqueia pedido de venda com preço abaixo do mínimo.` | `evals/eval-mvp.md` > Eval 2 | Deve classificar Faturamento/MATA410, usar SC5/SC6, separar PROBAT para regra e TIR para mensagem |
| EX-FAT-002 | `Monte testes para MATA460 validando geração de documento de saída, título financeiro e baixa de estoque.` | `evals/eval-mvp.md` > Eval 5 | Deve usar SF2/SD2, considerar SC5/SC6, SE1 e SB2 conforme cenário |
| EX-COM-001 | `Monte testes para MATA120 com validação de centro de custo obrigatório.` | `evals/eval-mvp.md` > Eval 3 | Deve classificar Compras/MATA120, usar SC7, definir fornecedor, produto, quantidade, preço e centro de custo |
| EX-EST-001 | `Crie um roteiro de testes para MATA010 validando unidade de medida e armazém padrão.` | `evals/eval-mvp.md` > Eval 4 | Deve classificar Estoque/Cadastros/MATA010, usar SB1 e considerar SB2/SB5 quando aplicável |
| EX-DIC-001 | `Crie testes para uma validação SX3 no campo de natureza e um gatilho SX7 que preenche centro de custo automaticamente.` | `evals/eval-mvp.md` > Eval 6 | Deve classificar SX3/SX7 sem inventar dicionário, pedir confirmação/exportação quando necessário |
| EX-AUT-001 | `Crie um exemplo PROBAT para uma função ADVPL que valida preço mínimo no pedido de venda.` | `evals/eval-mvp.md` > Eval 2 | Deve usar PROBAT somente para regra isolada, não para interface |
| EX-AUT-002 | `Crie um roteiro ExecAuto conceitual para testar inclusão de título a pagar na FINA050.` | `evals/eval-mvp.md` > Eval 1 | Deve tratar ExecAuto como técnica condicionada à confirmação no ambiente |
| EX-AUT-003 | `Crie um roteiro FwModel para validar cadastro de produto na MATA010.` | `evals/eval-mvp.md` > Eval 4 | Deve tratar FwModel como técnica condicionada à confirmação no ambiente |
| EX-AUT-004 | `Crie um roteiro TIR para validar mensagem visual na MATA410.` | `evals/eval-mvp.md` > Eval 2 | Deve usar TIR para tela/mensagem, não para regra isolada |

## Como validar uma resposta gerada

Uma resposta é aceita quando:

1. contém os 13 itens definidos em `SKILL.md`;
2. identifica rotina, módulo, tabela e objetivo;
3. escolhe a técnica de teste de acordo com o risco;
4. não inventa campo, parâmetro, ponto de entrada ou comportamento sem fonte;
5. define massa mínima de teste;
6. define evidência esperada;
7. conecta o exemplo ao eval correspondente;
8. explicita limitações e hipóteses do ambiente.

## Boas práticas

- Informe rotina, módulo e regra de negócio sempre que possível.
- Informe se existe ponto de entrada, SX3, SX7, SXB, ExecAuto, FwModel, TIR ou PROBAT envolvido.
- Informe tabelas/campos quando tiver certeza.
- Quando não houver certeza, peça para a skill marcar como hipótese.

## O que a skill não deve fazer

- Inventar campo, parâmetro ou ponto de entrada.
- Usar TIR para tudo.
- Usar PROBAT para validar tela.
- Usar ExecAuto para validar mensagem visual.
- Ignorar massa de dados e evidência.

## Validação

Use `evals/eval-mvp.md` para testar se a skill está respondendo no padrão correto.

```bash
python scripts/validate_skill.py
```
