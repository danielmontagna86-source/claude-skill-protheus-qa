# Uso da TDN na Skill

## Objetivo

Usar a TDN como base funcional/técnica para transformar documentação de rotina Protheus em cenários de teste.

## O que extrair da TDN

Para cada rotina, identificar:

- objetivo funcional;
- módulo;
- tabela principal;
- tabelas relacionadas;
- campos críticos;
- parâmetros MV_*;
- pontos de entrada;
- existência de rotina automática;
- exemplos de ExecAuto;
- comportamento MVC/FwModel;
- regras fiscais, financeiras, estoque ou faturamento;
- mensagens e validações importantes;
- observações e restrições.

## Não copiar página inteira

A skill deve resumir em ficha testável:

```text
rotina -> objetivo -> tabelas -> campos -> riscos -> cenários -> técnica -> evidência
```

## Fonte insuficiente

Quando não houver referência local ou TDN confirmada:

- declarar incerteza;
- marcar como hipótese;
- pedir confirmação do ambiente, fonte ou rotina;
- não inventar campo, ponto de entrada ou parâmetro.

## Modelo de ficha TDN

```md
# ROTINA - Nome

## Objetivo

## Tabela principal

## Tabelas relacionadas

## Campos críticos

## Parâmetros relevantes

## Operações

## Cenários mínimos

## Técnica recomendada

## Evidências

## Limitações
```
