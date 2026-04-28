# FINA050 - Contas a Pagar

## Módulo

Financeiro

## Objetivo funcional

Controlar títulos e compromissos a pagar da empresa, como duplicatas, notas fiscais, adiantamentos, pagamentos antecipados e demais obrigações financeiras.

## Tabela principal

- SE2 - Títulos a pagar

## Tabelas relacionadas

- SA2 - Fornecedores
- SE5 - Movimentações/baixas financeiras
- SA6 - Bancos
- SX5 / naturezas / parâmetros, conforme ambiente

## Campos críticos

- E2_PREFIXO
- E2_NUM
- E2_PARCELA
- E2_TIPO
- E2_NATUREZ
- E2_FORNECE
- E2_LOJA
- E2_EMISSAO
- E2_VENCTO
- E2_VENCREA
- E2_VALOR
- E2_SALDO

## Técnicas recomendadas

- ExecAuto para inclusão, alteração e exclusão funcional técnica.
- PROBAT quando a regra customizada estiver isolada em função/classe.
- TIR apenas para validar mensagem, tela, browse ou fluxo visual.
- Consulta em SE2/SE5 para evidência.

## Cenários mínimos

### Positivos

1. Incluir título válido com fornecedor, natureza, vencimento e valor.
2. Incluir título com vencimento real válido.
3. Alterar título permitido.
4. Excluir título permitido, quando aplicável.

### Negativos

1. Bloquear título sem natureza financeira.
2. Bloquear título com fornecedor inexistente.
3. Bloquear título com natureza inválida.
4. Bloquear vencimento menor que emissão, se regra do ambiente exigir.
5. Bloquear título com valor zerado, se regra do ambiente exigir.

### Regressão

1. Garantir que título válido continue gravando em SE2.
2. Garantir que regra customizada não bloqueie títulos legítimos.
3. Validar que saldo e vencimento permanecem consistentes.

## Customizações comuns

- Validação de natureza financeira.
- Bloqueio por fornecedor.
- Regras por filial.
- Validação de impostos/retenções.
- Geração de log/auditoria.
- Integração com aprovação ou pagamento.

## Evidências esperadas

- Registro criado ou não criado em SE2.
- Retorno/erro do ExecAuto.
- Log da customização, quando existir.
- Mensagem visual via TIR, quando aplicável.

## Limitações

Confirmar assinatura da rotina automática, campos obrigatórios, parâmetros e pontos de entrada na TDN, no fonte ou no ambiente do cliente antes de gerar automação definitiva.
