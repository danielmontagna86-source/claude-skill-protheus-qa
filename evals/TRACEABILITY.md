# Rastreabilidade de exemplos e evals

Este arquivo padroniza a ligacao entre exemplos de uso, evals e criterios de aceite.

## Fonte dos criterios

| Item | Fonte |
|---|---|
| Formato obrigatorio | `SKILL.md` |
| Exemplos | `USAGE.md` |
| Evals | `evals/eval-mvp.md` |
| Versao | `VERSION` |

## Matriz exemplo x eval

| Exemplo | Eval | Criterio de aceite |
|---|---|---|
| EX-FIN-001 | Eval 1 - FINA050 | 13 itens, rotina Financeiro/FINA050, SE2, massa e evidencia |
| EX-AUT-002 | Eval 1 - FINA050 | ExecAuto tratado como dependente de confirmacao |
| EX-FAT-001 | Eval 2 - MATA410 | SC5/SC6, preco minimo, PROBAT para regra e TIR para mensagem |
| EX-AUT-001 | Eval 2 - MATA410 | PROBAT somente para regra isolada |
| EX-AUT-004 | Eval 2 - MATA410 | TIR somente para tela ou mensagem |
| EX-COM-001 | Eval 3 - MATA120 | SC7, centro de custo obrigatorio e massa controlada |
| EX-EST-001 | Eval 4 - MATA010 | SB1 e tabelas auxiliares quando aplicavel |
| EX-AUT-003 | Eval 4 - MATA010 | FwModel condicionado a confirmacao do ambiente |
| EX-FAT-002 | Eval 5 - MATA460 | SF2/SD2, financeiro e estoque conforme cenario |
| EX-DIC-001 | Eval 6 - SX3/SX7 | Nao inventar dicionario; pedir fonte ou exportacao |

## Criterio geral

Um exemplo e considerado aceito quando:

- retorna os 13 itens definidos em `SKILL.md`;
- identifica modulo, rotina e dominio funcional;
- aponta tabelas principais sem inventar campos especificos;
- escolhe a tecnica de teste conforme o risco;
- define massa minima de dados;
- define evidencias verificaveis;
- diferencia positivo, negativo e regressao;
- explicita limitacoes, hipoteses e dependencias do ambiente.
