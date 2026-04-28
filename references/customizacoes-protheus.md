# Customizações Protheus

## Objetivo

Classificar customizações para orientar testes, risco e evidência.

## Tipos comuns

- User Function chamada por menu.
- Ponto de entrada convencional.
- Ponto de entrada MVC.
- Validação SX3.
- Gatilho SX7.
- Fórmula SXB.
- Rotina automática.
- FwModel/MVC.
- REST/API.
- Job/schedule.
- Relatório.

## Riscos por tipo

| Tipo | Risco típico | Teste recomendado |
|---|---|---|
| Ponto de entrada | abortar rotina, alterar regra padrão, gravar errado | executar rotina e validar efeito |
| PE MVC | PARAMIXB/retorno incorreto, evento errado | validar evento, retorno e modelo |
| SX3 | bloquear campo indevidamente | massa positiva/negativa |
| SX7 | preencher campo errado | validar origem/destino do gatilho |
| SXB | cálculo incorreto | testar entradas/saídas |
| Job | processar massa errada | massa controlada + log |
| REST/API | segurança e validação de payload | teste HTTP/PROBAT API |

## Processo

1. Identificar onde a customização roda.
2. Comparar comportamento padrão x comportamento customizado.
3. Mapear tabela e campo afetado.
4. Criar cenários positivos, negativos e regressivos.
5. Definir técnica e evidência.

## Regra

Não assumir ponto de entrada ou evento MVC sem fonte, código ou confirmação do usuário.
