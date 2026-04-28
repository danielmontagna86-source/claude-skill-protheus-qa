# FINA090 - Baixas a Pagar

## Contexto

Rotina usada para baixa/pagamento de títulos a pagar. Impacta contas a pagar, movimentos financeiros, banco/caixa, borderô, CNAB, retenções, desconto, juros, contabilidade e conciliação.

## Objetivo de QA

Garantir que títulos a pagar sejam baixados, estornados, bloqueados ou rejeitados corretamente, respeitando saldo, status, data, banco, valor, permissões e regras financeiras.

## Tabelas principais

| Tabela | Uso |
|---|---|
| SE2 | Títulos a pagar |
| SE5 | Movimentos e baixas |
| SA2 | Fornecedor |
| SED | Natureza financeira |
| SEB | Ocorrências/retornos, quando aplicável |
| SX3/SX7/SXB | Dicionário, gatilhos e consultas |

## Riscos

- Baixa duplicada.
- Baixa de título já baixado.
- Valor maior que saldo.
- Banco/conta inválido.
- Juros, multa ou desconto divergente.
- Data de pagamento fora da regra.
- Estorno indevido.
- Integração sem rollback.

## Cenários positivos

| ID | Cenário | Resultado esperado |
|---|---|---|
| FINA090-POS-001 | Baixar título aberto com valor válido | SE2 atualizado e SE5 gerado |
| FINA090-POS-002 | Baixa parcial permitida | Saldo remanescente correto |
| FINA090-POS-003 | Baixa com desconto/juros permitido | Valores gravados corretamente |
| FINA090-POS-004 | Estorno permitido | Movimento revertido corretamente |
| FINA090-POS-005 | Baixa por borderô/CNAB, quando usado | Status financeiro consistente |

## Cenários negativos

| ID | Cenário | Resultado esperado |
|---|---|---|
| FINA090-NEG-001 | Título inexistente | Bloqueia operação |
| FINA090-NEG-002 | Título já baixado | Impede nova baixa |
| FINA090-NEG-003 | Valor maior que saldo | Bloqueia baixa |
| FINA090-NEG-004 | Banco/conta inválido | Rejeita operação |
| FINA090-NEG-005 | Data fora do período permitido | Bloqueia ou exige aprovação |
| FINA090-NEG-006 | Usuário sem permissão baixa/estorna | Bloqueia ação |

## Regressão

- Baixa manual total.
- Baixa parcial.
- Estorno.
- Baixa por integração/ExecAuto/FwModel.
- Baixa via borderô/CNAB, quando aplicável.
- Juros, desconto e multa.
- Multi-filial.
- Contabilidade/conciliação, quando aplicável.

## Massa mínima

- Título aberto.
- Título já baixado.
- Título parcial.
- Fornecedor válido e bloqueado.
- Banco/conta válido e inválido.
- Usuário financeiro e restrito.
- Cenário com juros/desconto.

## PROBAT

Testar título baixado, saldo, valor, data, banco, permissão, estorno e regra de desconto/juros.

## ExecAuto/FwModel

Validar baixa automatizada, retorno de erro, rollback, atualização SE2, geração SE5 e aderência à interface.

## TIR/WebApp

Validar tela, seleção do título, baixa válida, bloqueios, mensagens e evidência visual.

## Evidências

- SE2 antes/depois.
- SE5 gerado ou estornado.
- Print/log de mensagem.
- Resultado PROBAT.
- Log ExecAuto/FwModel.
- Evidência TIR.

## Prompt exemplo

```text
Monte matriz de testes para FINA090 com customização que bloqueia baixa de título já baixado, valor maior que saldo e alteração de data de pagamento por usuário sem permissão. Inclua cenários, massa, PROBAT, ExecAuto/FwModel, TIR e evidências.
```
