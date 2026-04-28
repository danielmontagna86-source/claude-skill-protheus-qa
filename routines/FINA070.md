# FINA070 - Contas a Receber

## Contexto

Rotina para manutenção de títulos a receber. Impacta faturamento, cobrança, baixa, juros, multa, desconto, fluxo de caixa, contabilidade, boleto, CNAB, PIX e integrações.

## Objetivo de QA

Garantir que títulos a receber sejam criados, alterados, bloqueados ou rejeitados corretamente, mantendo consistência em cliente, natureza, vencimento, valor, parcela, baixa e rastreabilidade financeira.

## Tabelas principais

| Tabela | Uso |
|---|---|
| SE1 | Títulos a receber |
| SA1 | Cliente |
| SED | Natureza financeira |
| SE5 | Movimentos e baixas |
| SE4 | Condição de pagamento |
| SF2/SD2 | Origem por faturamento |
| SX3/SX7/SXB | Dicionário, gatilhos e consultas |

## Riscos

| Risco | Impacto |
|---|---|
| Título duplicado | Cobrança indevida |
| Cliente bloqueado aceito | Risco financeiro |
| Natureza incorreta | Erro contábil ou gerencial |
| Vencimento inválido | Fluxo de caixa errado |
| Juros/multa/desconto divergentes | Cobrança incorreta |
| Integração sem validar regra | Título inválido por carga/API |

## Cenários positivos

| ID | Cenário | Resultado esperado |
|---|---|---|
| FINA070-POS-001 | Incluir título com cliente, natureza, valor e vencimento válidos | SE1 gravado |
| FINA070-POS-002 | Incluir título parcelado | Parcelas coerentes |
| FINA070-POS-003 | Alterar vencimento permitido | Vencimento atualizado |
| FINA070-POS-004 | Título originado do faturamento | Vínculo preservado |
| FINA070-POS-005 | Baixa posterior válida | Movimento SE5 coerente |

## Cenários negativos

| ID | Cenário | Resultado esperado |
|---|---|---|
| FINA070-NEG-001 | Cliente bloqueado/inativo | Bloqueia gravação |
| FINA070-NEG-002 | Natureza inválida | Rejeita título |
| FINA070-NEG-003 | Valor menor ou igual a zero | Bloqueia gravação |
| FINA070-NEG-004 | Vencimento inválido | Bloqueia ou exige justificativa |
| FINA070-NEG-005 | Título duplicado | Impede duplicidade |
| FINA070-NEG-006 | Desconto ou juros fora da regra | Rejeita operação |
| FINA070-NEG-007 | Usuário sem permissão altera campo crítico | Bloqueia alteração |

## Regressão

- Inclusão manual.
- Inclusão por faturamento.
- Inclusão por integração/ExecAuto/FwModel.
- Alteração de vencimento.
- Alteração de natureza.
- Duplicidade.
- Baixa posterior.
- CNAB, boleto ou PIX, quando usado.
- Multi-filial.

## Massa mínima

- Cliente válido e bloqueado.
- Natureza válida e inválida.
- Título novo e duplicado.
- Título parcelado.
- Vencimento válido e inválido.
- Usuário financeiro e restrito.
- Título originado de nota fiscal.

## PROBAT

Testar duplicidade, cliente bloqueado, natureza, vencimento, valor, regra de desconto/juros e permissão.

```text
Crie um teste PROBAT para validar que a FINA070 bloqueia título duplicado e impede alteração de vencimento por usuário sem permissão.
```

## ExecAuto/FwModel

Validar inclusão/alteração automatizada, retorno de erro, rollback, gravação SE1 e aderência às regras da interface.

## TIR/WebApp

Validar tela, preenchimento, mensagens, gravação válida, bloqueio de cenário inválido e evidência visual.

## Evidências

- Registro SE1 criado ou bloqueado.
- SE5 gerado em baixa posterior, quando aplicável.
- Print/log da mensagem.
- Resultado PROBAT.
- Log ExecAuto/FwModel.
- Evidência TIR.

## Prompt exemplo

```text
Monte matriz de testes para FINA070 com customização que bloqueia título duplicado e impede alteração de vencimento por usuário sem permissão. Inclua cenários, massa, PROBAT, ExecAuto/FwModel, TIR e evidências.
```
