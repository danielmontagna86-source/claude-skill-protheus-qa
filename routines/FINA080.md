# FINA080

## Objetivo
Guia minimo de QA para rotina financeira de recebimentos no Protheus.

## Escopo
- Validar processamento total e parcial.
- Validar reversao operacional.
- Validar permissao de usuario.
- Validar integracao automatizada.
- Validar consistencia das tabelas SE1 e SE5.

## Tabelas
| Tabela | Uso |
|---|---|
| SE1 | Titulos |
| SE5 | Movimentos |
| SA1 | Cliente |
| SX3 | Dicionario |
| SX7 | Gatilhos |
| SXB | Consultas |

## Cenarios positivos
| ID | Cenario | Esperado |
|---|---|---|
| FINA080-POS-001 | Processamento valido | SE1 e SE5 consistentes |
| FINA080-POS-002 | Processamento parcial | Saldo correto |
| FINA080-POS-003 | Reversao permitida | Movimento revertido |

## Cenarios negativos
| ID | Cenario | Esperado |
|---|---|---|
| FINA080-NEG-001 | Registro inexistente | Operacao bloqueada |
| FINA080-NEG-002 | Registro ja processado | Reprocessamento bloqueado |
| FINA080-NEG-003 | Valor inconsistente | Operacao rejeitada |
| FINA080-NEG-004 | Usuario sem permissao | Acao bloqueada |

## Automacao
- PROBAT para regras isoladas.
- ExecAuto/FwModel para integracao e rollback.
- TIR/WebApp para evidencia visual.

## Evidencias
- SE1 antes e depois.
- SE5 gerado ou revertido.
- Logs da rotina.
- Evidencias de tela.
