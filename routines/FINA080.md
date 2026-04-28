# FINA080 - Baixas a Receber / Recebimentos

## Objetivo

Guia de QA para validar a rotina financeira FINA080 em cenarios de baixa, recebimento, reversao/cancelamento operacional, integracao e consistencia contabil/financeira no TOTVS Protheus.

Use esta ficha quando o pedido envolver:

- baixa de titulo a receber;
- recebimento total ou parcial;
- juros, multa, desconto ou abatimento;
- estorno/reversao de baixa;
- consistencia entre titulo e movimento financeiro;
- validacao de customizacao, ponto de entrada, regra SX3/SX7/SXB ou automacao ligada a recebimentos.

## Contexto funcional

A FINA080 e usada no fluxo de contas a receber para registrar ou controlar recebimentos/baixas de titulos. A validacao deve garantir que o saldo do titulo, o movimento financeiro e os efeitos de integracao fiquem consistentes.

Fluxo conceitual:

```text
Cliente / Documento de origem
→ SE1 - Titulo a receber
→ FINA080 - Baixa/recebimento
→ SE5 - Movimento financeiro
→ Reflexos auxiliares conforme configuracao do ambiente
```

> Observacao: nomes exatos de campos, parametros, pontos de entrada e comportamentos especificos devem ser confirmados por TDN, dicionario SX3, fonte do usuario ou codigo analisado. Nao inventar campo ou ponto de entrada.

## Tabelas principais e auxiliares

| Tabela | Uso esperado no QA | Cuidado |
|---|---|---|
| SE1 | Titulo a receber, saldo, status e valores do recebimento | Confirmar campos no dicionario do ambiente |
| SE5 | Movimento financeiro gerado, cancelado ou revertido | Validar valor, data, historico e vinculo com o titulo |
| SA1 | Cliente usado na massa de teste | Cliente deve estar ativo e coerente com filial/loja |
| SE4 | Condicao de pagamento, quando houver origem comercial | Usar somente se fizer parte do fluxo testado |
| SF2/SD2 | Documento de saida e itens, quando o titulo vier do faturamento | Validar apenas se a origem do titulo for NF/faturamento |
| SX3 | Validacoes de campo e metadados | Nao afirmar conteudo sem exportacao ou fonte |
| SX7 | Gatilhos que alteram preenchimentos | Confirmar origem/destino do gatilho |
| SXB | Consultas padrao relacionadas | Confirmar alias, retorno e filtro |

## Riscos QA

| Risco | Impacto | Prioridade |
|---|---|---|
| Baixa duplicada | Titulo recebido duas vezes ou saldo incorreto | Alta |
| Baixa parcial incorreta | Saldo residual errado | Alta |
| Valor com juros/desconto inconsistente | Divergencia financeira e contabil | Alta |
| SE1 atualizado sem SE5 correspondente | Rastreabilidade quebrada | Alta |
| SE5 gerado sem alteracao coerente em SE1 | Movimento financeiro sem base | Alta |
| Reversao incompleta | Saldo ou movimento permanece incorreto | Alta |
| Permissao indevida | Usuario executa baixa/cancelamento sem autorizacao | Media/Alta |
| Customizacao bloqueia caso valido | Interrupcao operacional | Media |
| Customizacao permite caso invalido | Risco financeiro e auditoria | Alta |
| Automacao sem massa controlada | Teste instavel e falso positivo | Media |

## Cenarios positivos

| ID | Cenario | Massa minima | Resultado esperado | Evidencia |
|---|---|---|---|---|
| FINA080-POS-001 | Baixa total valida de titulo em aberto | Cliente ativo, titulo SE1 em aberto, valor integral | Titulo baixado e movimento SE5 gerado | SE1 antes/depois + SE5 |
| FINA080-POS-002 | Baixa parcial valida | Titulo em aberto com valor maior que o recebido | Saldo residual correto | SE1 saldo + SE5 do valor recebido |
| FINA080-POS-003 | Baixa com desconto permitido | Titulo em aberto, regra de desconto confirmada | Valor liquido e saldo coerentes | SE1/SE5 + regra aplicada |
| FINA080-POS-004 | Baixa com juros/multa permitida | Titulo vencido, regra de juros confirmada | Valor recebido maior que principal conforme regra | SE1/SE5 + calculo |
| FINA080-POS-005 | Reversao/cancelamento permitido | Titulo previamente baixado | Movimento revertido e saldo restaurado | SE1 restaurado + SE5 reversao/cancelamento |
| FINA080-POS-006 | Baixa de titulo originado no faturamento | SF2/SD2/SE1 validos, quando aplicavel | Recebimento mantem rastreabilidade com origem | SF2/SD2/SE1/SE5 conforme cenario |

## Cenarios negativos

| ID | Cenario | Resultado esperado | Evidencia |
|---|---|---|---|
| FINA080-NEG-001 | Tentar baixar titulo inexistente | Operacao bloqueada ou retorno de erro controlado | Mensagem/retorno + ausencia de SE5 |
| FINA080-NEG-002 | Tentar baixar titulo ja liquidado | Reprocessamento bloqueado | SE1 sem nova alteracao + nenhum SE5 duplicado |
| FINA080-NEG-003 | Informar valor maior que saldo permitido | Operacao rejeitada ou tratada pela regra confirmada | Mensagem/retorno + saldo preservado |
| FINA080-NEG-004 | Usuario sem permissao executa baixa | Acao bloqueada | Evidencia de permissao + ausencia de movimento |
| FINA080-NEG-005 | Data de baixa invalida para regra do ambiente | Operacao bloqueada ou classificada conforme parametrizacao | Mensagem/retorno + logs |
| FINA080-NEG-006 | Customizacao bloqueia natureza/cliente/carteira invalida | Bloqueio com mensagem clara | Retorno da regra + SE1/SE5 sem alteracao indevida |
| FINA080-NEG-007 | Falha simulada no meio do processo | Transacao deve permanecer consistente | SE1 e SE5 sem divergencia |

## Cenarios de regressao

| ID | Area afetada | Validacao |
|---|---|---|
| FINA080-REG-001 | Baixa total padrao | Garantir que customizacao nao quebrou fluxo original |
| FINA080-REG-002 | Baixa parcial | Validar saldo residual depois da customizacao |
| FINA080-REG-003 | Estorno/reversao | Validar restauracao do titulo e movimento financeiro |
| FINA080-REG-004 | Faturamento integrado | Validar titulo vindo de documento de saida, se aplicavel |
| FINA080-REG-005 | Permissoes | Validar perfil autorizado e perfil bloqueado |
| FINA080-REG-006 | Relatorios/consultas financeiras | Validar se baixa aparece corretamente nas consultas usadas pela operacao |
| FINA080-REG-007 | SX3/SX7/SXB | Validar se validacoes/gatilhos/consultas continuam coerentes |

## Massa minima de dados

Monte massa controlada por filial e ambiente:

| Campo conceitual | Exemplo | Observacao |
|---|---|---|
| Filial | 01 | Usar filial de homologacao |
| Cliente | Cliente ativo SA1 | Confirmar loja e situacao cadastral |
| Titulo | SE1 em aberto | Criar titulo exclusivo para teste |
| Valor principal | 1000,00 | Usar valores simples para conferencia |
| Valor parcial | 400,00 | Usar para teste de saldo residual |
| Desconto | 50,00 | Somente se regra permitir |
| Juros/multa | 20,00 | Somente se regra permitir |
| Data emissao | Data anterior ao vencimento | Coerente com regra financeira |
| Data vencimento | Vencido e/ou a vencer | Criar massas separadas |
| Data baixa | Data atual de homologacao | Confirmar calendario/periodo aberto |
| Usuario | Perfil autorizado e perfil bloqueado | Validar permissao |

## Tecnica recomendada

### PROBAT

Use para testar regra isolada, como:

- calculo de valor permitido para baixa;
- validacao de desconto/juros/multa;
- validacao de regra de cliente, natureza, carteira ou filial;
- funcao ADVPL/TLPP desacoplada da tela.

Nao usar PROBAT para validar mensagem visual ou comportamento de tela.

### ExecAuto / FwModel

Use quando houver automacao confiavel e confirmada para o fluxo de baixa/recebimento no ambiente.

Validar:

- entrada correta da massa;
- retorno da rotina;
- atualizacao de SE1;
- geracao/estorno em SE5;
- rollback em caso de falha;
- logs da execucao.

Nao afirmar que existe ExecAuto/FwModel para a rotina sem fonte. Marcar como hipotese quando nao confirmado.

### TIR / WebApp

Use para validar:

- mensagem visual;
- bloqueio em tela;
- comportamento de botoes;
- preenchimento visual de campos;
- fluxo de usuario quando a automacao tecnica nao cobre interface.

Nao usar TIR como primeira opcao para regra isolada ou integracao repetivel.

### Checklist manual

Use quando:

- nao houver massa confiavel;
- nao houver automacao documentada;
- o fluxo depender de aprovacao humana;
- o risco de automatizar for maior que o ganho inicial.

## Exemplo de roteiro de validacao

```text
1. Criar ou selecionar cliente ativo em SA1.
2. Gerar titulo SE1 em aberto com valor controlado.
3. Registrar snapshot inicial de SE1.
4. Executar baixa total ou parcial pela tecnica escolhida.
5. Validar retorno da rotina ou mensagem visual.
6. Consultar SE1 e conferir saldo/status.
7. Consultar SE5 e conferir movimento gerado.
8. Executar reversao/cancelamento, quando aplicavel.
9. Validar restauracao de SE1 e movimento de reversao/ausencia de duplicidade em SE5.
10. Registrar evidencias finais.
```

## Evidencias esperadas

- SE1 antes e depois da baixa.
- SE5 gerado, cancelado ou revertido.
- Valor principal, valor recebido, saldo, juros, desconto e multa, quando aplicavel.
- Retorno de ExecAuto/FwModel, quando usado.
- Evidencia de tela/mensagem, quando TIR/WebApp for usado.
- Log da customizacao, quando existir.
- Identificacao da massa: filial, cliente, titulo, parcela, valor e usuario.

## Limites e hipoteses

- Campos exatos de SE1/SE5 devem ser confirmados no dicionario do ambiente.
- Pontos de entrada nao devem ser citados como certos sem fonte.
- Parametros financeiros variam por cliente, release e configuracao.
- Baixas com integracao bancaria, contabil ou conciliacao podem exigir cenarios adicionais.
- Se a rotina estiver customizada, priorizar analise do codigo ADVPL/TLPP antes de automatizar.

## Prompt exemplo

```text
Crie testes para uma customizacao na FINA080 que bloqueia baixa de titulo a receber quando o cliente estiver com restricao financeira, validando SE1, SE5, massa de dados, tecnica recomendada e evidencias.
```
