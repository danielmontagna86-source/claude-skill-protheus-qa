# MATA410 - Pedido de Venda

## Contexto funcional

A rotina MATA410 é usada para manutenção de Pedido de Venda no Protheus. É uma rotina crítica do fluxo comercial e costuma receber customizações envolvendo cliente, produto, TES, preço, desconto, margem, condição de pagamento, vendedor, estoque, crédito, bloqueios, aprovação/liberação e integração com faturamento.

## Objetivo da rotina no QA

Garantir que o Pedido de Venda seja incluído, alterado, bloqueado, liberado ou rejeitado conforme regras comerciais, fiscais, financeiras e de estoque, sem gerar inconsistências no faturamento, saldo, crédito do cliente ou documento de saída.

## Principais tabelas envolvidas

| Tabela | Uso esperado |
|---|---|
| SC5 | Cabeçalho do Pedido de Venda |
| SC6 | Itens do Pedido de Venda |
| SA1 | Cadastro de Clientes |
| SB1 | Cadastro de Produtos |
| SB2 | Saldos de estoque, quando aplicável |
| SF4 | TES |
| SE4 | Condições de pagamento |
| DA0/DA1 | Tabela de preço, quando usada pelo cliente |
| SX3 | Dicionário de campos e obrigatoriedade |
| SX7 | Gatilhos |
| SXB | Consultas padrão e fórmulas |

> Validar nomes/tabelas conforme release, dicionário local e customizações do cliente. Não assumir estrutura fixa sem confirmar no ambiente.

## Pontos de entrada comuns

Os pontos de entrada variam por release, pacote e arquitetura usada. Antes de sugerir código ou automação, confirmar no fonte/local do cliente ou documentação TDN da versão.

Áreas comuns de customização:

- validação antes da gravação do pedido;
- validação por item;
- validação de cliente bloqueado/inadimplente;
- regra de limite de crédito;
- regra de preço, desconto e margem mínima;
- validação de estoque;
- validação de TES e operação fiscal;
- preenchimento automático de vendedor, tabela de preço ou condição de pagamento;
- aprovação/liberação comercial;
- mensagens em tela;
- integração posterior com documento de saída.

## Riscos de customização

| Risco | Impacto |
|---|---|
| Validar apenas interface e esquecer ExecAuto/FwModel | Integração pode gravar pedido inválido |
| Permitir desconto acima do limite | Perda de margem comercial |
| Validar crédito só no cabeçalho | Itens podem elevar valor total acima da regra |
| Ignorar estoque por filial/armazém | Venda sem saldo disponível |
| Usar TES incorreta | Erro fiscal no documento de saída |
| Bloquear cliente sem exceções comerciais | Pedido legítimo impedido |
| Mensagem genérica | Usuário não identifica motivo do bloqueio |
| Não testar liberação posterior | Pedido bloqueado pode nunca seguir para faturamento |

## Cenários positivos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA410-POS-001 | Incluir pedido com cliente ativo, produto ativo, TES válida, preço válido e estoque disponível | Pedido gravado com sucesso |
| MATA410-POS-002 | Incluir pedido com múltiplos itens válidos | Cabeçalho e itens gravados corretamente em SC5/SC6 |
| MATA410-POS-003 | Aplicar desconto dentro do limite permitido | Pedido aceito e valores recalculados corretamente |
| MATA410-POS-004 | Usar condição de pagamento válida para o cliente | Condição aceita e pedido gravado |
| MATA410-POS-005 | Liberar pedido bloqueado por usuário com permissão/alçada | Pedido muda para status liberado conforme regra |

## Cenários negativos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA410-NEG-001 | Cliente bloqueado/inativo/inadimplente | Pedido não deve ser gravado ou deve ficar bloqueado conforme regra |
| MATA410-NEG-002 | Produto bloqueado/inativo | Item não deve ser aceito |
| MATA410-NEG-003 | TES inválida para operação | Sistema deve bloquear com mensagem clara |
| MATA410-NEG-004 | Estoque insuficiente quando regra exige saldo | Pedido/item deve ser bloqueado |
| MATA410-NEG-005 | Desconto acima do limite permitido | Sistema deve rejeitar ou exigir aprovação |
| MATA410-NEG-006 | Preço unitário zerado quando não permitido | Sistema deve impedir gravação |
| MATA410-NEG-007 | Limite de crédito excedido | Pedido deve ficar bloqueado ou exigir liberação |
| MATA410-NEG-008 | Condição de pagamento incompatível com cliente | Sistema deve rejeitar ou bloquear pedido |

## Cenários de regressão

- Inclusão manual pela interface.
- Inclusão via ExecAuto/FwModel, quando existir integração.
- Alteração de item já gravado.
- Exclusão/cancelamento de item, quando permitido.
- Alteração de preço e desconto.
- Validação de limite de crédito.
- Validação de estoque.
- Bloqueio e liberação comercial.
- Integração posterior com documento de saída.
- Validação multi-filial e armazém.
- Validação com usuário vendedor, gerente e usuário restrito.
- Validação de mensagens em tela via TIR/WebApp.

## Massa de dados mínima

| Tipo | Massa |
|---|---|
| Cliente válido | SA1 ativo, sem bloqueio e com limite/regra compatível |
| Cliente bloqueado | SA1 com status/regra que impeça venda ou exija liberação |
| Produto válido | SB1 ativo e permitido para venda |
| Produto bloqueado | SB1 com regra que impeça venda |
| Estoque suficiente | SB2 com saldo disponível no armazém/filial testada |
| Estoque insuficiente | SB2 sem saldo ou abaixo da quantidade solicitada |
| TES válida | SF4 compatível com venda e faturamento |
| TES inválida | SF4 incompatível com tipo de operação |
| Condição de pagamento válida | SE4 aceita para o cliente/regra comercial |
| Desconto válido | Percentual dentro do limite permitido |
| Desconto inválido | Percentual acima da alçada do usuário |
| Usuário vendedor | Permissão para incluir pedido |
| Usuário gerente | Permissão para liberar exceções, se aplicável |
| Usuário restrito | Sem permissão para regra crítica |

## Estratégia PROBAT

Usar PROBAT para testar regras isoladas ADVPL/TLPP quando a customização estiver encapsulada em função validável.

Casos ideais:

- validação de cliente bloqueado;
- validação de limite de crédito;
- cálculo/validação de desconto máximo;
- validação de margem mínima;
- validação de estoque disponível;
- validação de TES;
- validação de condição de pagamento;
- padronização de mensagens de erro.

Exemplo de prompt para gerar teste PROBAT:

```text
Crie um teste PROBAT para uma função ADVPL que valida se o pedido da MATA410 deve ser bloqueado quando o desconto do item ultrapassa o limite do usuário ou quando o cliente excede limite de crédito.
```

## Estratégia ExecAuto/FwModel

Usar ExecAuto ou FwModel para validar o fluxo técnico de inclusão/alteração quando o cliente usa integração, e-commerce, força de vendas, carga, API ou processo sem interface.

Validar:

- retorno de sucesso/erro;
- gravação correta em SC5/SC6;
- rollback em caso de falha;
- mensagens retornadas;
- cálculo de total do pedido;
- comportamento multi-item;
- aplicação da mesma regra usada na interface;
- impacto posterior no faturamento, quando aplicável.

## Estratégia TIR/WebApp

Usar TIR quando a regra precisa ser comprovada na interface, principalmente para mensagens, bloqueios visuais, campos obrigatórios, preço, desconto e liberação.

Validar:

- acesso à rotina;
- preenchimento do cabeçalho;
- inclusão de item;
- tentativa de gravação inválida;
- mensagem exibida;
- gravação válida;
- bloqueio/liberação;
- evidência visual antes e depois da ação.

## Evidências esperadas

- Print ou log da inclusão válida.
- Print ou log da mensagem de bloqueio.
- Registro SC5/SC6 gerado ou não gerado, conforme cenário.
- Log da automação ExecAuto/FwModel, quando aplicável.
- Resultado PROBAT para regra isolada.
- Evidência TIR para comportamento de interface.
- Massa usada no teste.
- Release/versão do Protheus, filial e armazém usados.

## Checklist rápido para analista

```text
[ ] Confirme release e dicionário local.
[ ] Confirme campos obrigatórios SX3.
[ ] Confirme gatilhos SX7.
[ ] Confirme regra de cliente bloqueado/crédito.
[ ] Confirme regra de preço, desconto e margem.
[ ] Confirme regra de estoque por filial/armazém.
[ ] Confirme TES e operação fiscal.
[ ] Confirme se há integração externa ou carga automática.
[ ] Teste interface e automação, se ambas existirem.
[ ] Gere evidência antes/depois.
```

## Prompt exemplo para uso da skill

```text
Monte uma matriz de testes para a rotina MATA410 considerando uma customização que bloqueia pedido quando o desconto do item ultrapassa 10% ou quando o cliente excede o limite de crédito. Inclua cenários positivos, negativos, regressão, massa de dados, estratégia PROBAT, ExecAuto/FwModel e TIR.
```
