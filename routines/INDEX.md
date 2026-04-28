# Índice de Rotinas

Este índice ajuda a skill a localizar rapidamente fichas técnicas por rotina, módulo e nível de cobertura QA.

## Rotinas documentadas

| Rotina | Módulo | Domínio | Status | Arquivo |
|---|---|---|---|---|
| FINA050 | Financeiro | Contas a pagar / títulos a pagar | MVP | `routines/FINA050.md` |
| FINA080 | Financeiro | Contas a receber / baixas e recebimentos | Completo | `routines/FINA080.md` |
| MATA010 | Estoque/Cadastros | Cadastro de produto | MVP | `routines/MATA010.md` |
| MATA120 | Compras | Pedido/solicitação de compra conforme ambiente | MVP | `routines/MATA120.md` |
| MATA220 | Estoque | Movimentações internas | Completo | `routines/MATA220.md` |
| MATA410 | Faturamento | Pedido de venda | MVP | `routines/MATA410.md` |
| MATA460 | Faturamento | Documento de saída / faturamento | MVP | `routines/MATA460.md` |

## Como usar este índice

1. Identifique a rotina informada pelo usuário.
2. Consulte a ficha correspondente em `routines/`.
3. Use a ficha como referência local, mas não invente campos, parâmetros ou pontos de entrada.
4. Quando a ficha estiver em status `MVP`, trate detalhes específicos como hipótese até haver confirmação por TDN, dicionário, código ou fonte do usuário.
5. Quando não existir ficha para a rotina, use o formato padrão da skill e marque como necessário confirmar fonte funcional/técnica.

## Status

| Status | Significado |
|---|---|
| MVP | Cobertura suficiente para orientar QA, mas exige confirmação técnica do ambiente |
| Completo | Cobertura ampliada com riscos, cenários, massa, técnica e evidências |
| Planejado | Rotina ainda não documentada ou pendente de expansão |

## Regra de segurança

Mesmo quando a rotina estiver documentada, a resposta deve respeitar a regra anti-alucinação do `SKILL.md`: não afirmar campo, parâmetro, ponto de entrada ou comportamento específico sem fonte confiável.
