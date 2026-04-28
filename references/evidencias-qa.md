# Guia de Evidências QA

## Objetivo

Padronizar quais evidências devem ser esperadas para cada tipo de teste Protheus.

## Tipos de evidência

| Técnica | Evidências principais |
|---|---|
| PROBAT | assert, resultado da suíte, log de execução |
| ExecAuto | retorno, erro capturado, tabela alterada, massa usada |
| FwModel | validação do modelo, persistência, retorno da operação |
| TIR | screenshot, log, mensagem, browse, campo exibido |
| Checklist | print, consulta, assinatura de homologação, evidência manual |

## Evidências por módulo

### Financeiro

- SE1, SE2 e SE5 conforme operação.
- Saldo, baixa, vencimento, natureza, fornecedor/cliente.
- Log de regra customizada quando existir.

### Faturamento

- SC5/SC6 para pedido.
- SD2/SF2 para documento de saída.
- SE1 quando gerar título.
- Mensagem de bloqueio, crédito, estoque ou TES.

### Compras

- SC1 para solicitação.
- SC7 para pedido.
- SD1/SF1 para entrada.
- SE2 quando gerar financeiro.

### Estoque

- SB1 para cadastro.
- SB2 para saldo.
- SD3 para movimentos internos.
- Custo/saldo quando aplicável.

## Regra

Toda evidência deve responder:

```text
O que foi executado?
Qual massa foi usada?
Qual resultado era esperado?
Onde o resultado foi comprovado?
```
