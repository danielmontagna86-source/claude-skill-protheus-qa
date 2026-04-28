# MATA120 - Pedido de Compras

## Contexto funcional

A rotina MATA120 é usada para manutenção de Pedido de Compras no Protheus. É uma das principais rotinas do fluxo de suprimentos e costuma receber customizações para validação de fornecedor, produto, TES, centro de custo, alçada, aprovação, comprador, prazos e integração com solicitação de compras.

## Objetivo da rotina no QA

Garantir que o Pedido de Compras seja incluído, alterado, aprovado, bloqueado ou rejeitado conforme regras funcionais, fiscais, financeiras e cadastrais, sem quebrar integrações com estoque, financeiro, fiscal e documentos de entrada.

## Principais tabelas envolvidas

| Tabela | Uso esperado |
|---|---|
| SC7 | Itens do Pedido de Compras |
| SA2 | Cadastro de Fornecedores |
| SB1 | Cadastro de Produtos |
| SF4 | TES |
| CT1/CTT | Contas e centros de custo, quando aplicável |
| SCR/SCP/SCQ | Solicitação/cotação/pedido, conforme fluxo utilizado |
| SX3 | Dicionário de campos e obrigatoriedade |
| SX7 | Gatilhos |
| SXB | Consultas padrão e fórmulas |

> Validar nomes/tabelas conforme release, dicionário local e customizações do cliente. Não assumir estrutura fixa sem confirmar no ambiente.

## Pontos de entrada comuns

Os pontos de entrada variam por release, pacote e arquitetura usada. Antes de sugerir código ou teste automatizado, confirmar no fonte/local do cliente ou documentação TDN da versão.

Exemplos de áreas onde normalmente há customização:

- validação antes da gravação do pedido;
- validação por item;
- preenchimento automático de campos;
- bloqueio por fornecedor/produto;
- regra de alçada;
- integração com solicitação ou cotação;
- aprovação e liberação;
- validação de centro de custo;
- regra fiscal/TES;
- mensagens em tela.

## Riscos de customização

| Risco | Impacto |
|---|---|
| Validar somente o cabeçalho e esquecer itens | Pedido gravado com item inconsistente |
| Bloquear fornecedor sem considerar exceções | Interrupção indevida do processo de compras |
| Alterar TES automaticamente sem rastreio | Erro fiscal ou divergência no documento de entrada |
| Exigir centro de custo para todo produto | Quebra de produtos sem controle gerencial |
| Customização sem rollback transacional | Pedido parcial ou inconsistência de item |
| Mensagem genérica | Analista não entende o motivo do bloqueio |
| Teste apenas pela interface | Falha em ExecAuto/FwModel não detectada |

## Cenários positivos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA120-POS-001 | Incluir pedido com fornecedor ativo, produto ativo, TES válida e centro de custo correto | Pedido gravado com sucesso |
| MATA120-POS-002 | Incluir pedido com múltiplos itens válidos | Todos os itens gravados na SC7 corretamente |
| MATA120-POS-003 | Alterar quantidade de item antes da aprovação | Quantidade atualizada e recalculada conforme regra |
| MATA120-POS-004 | Usar produto com regra específica de centro de custo | Pedido aceito quando centro de custo for informado |
| MATA120-POS-005 | Gerar pedido a partir de solicitação aprovada | Pedido vinculado corretamente ao documento origem |

## Cenários negativos

| ID | Cenário | Resultado esperado |
|---|---|---|
| MATA120-NEG-001 | Fornecedor bloqueado/inativo | Pedido não deve ser gravado |
| MATA120-NEG-002 | Produto bloqueado/inativo | Item não deve ser aceito |
| MATA120-NEG-003 | TES inválida para operação | Sistema deve bloquear com mensagem clara |
| MATA120-NEG-004 | Centro de custo obrigatório não informado | Sistema deve bloquear gravação do item/pedido |
| MATA120-NEG-005 | Quantidade menor ou igual a zero | Item deve ser rejeitado |
| MATA120-NEG-006 | Preço unitário zerado quando regra não permite | Sistema deve impedir gravação |
| MATA120-NEG-007 | Pedido acima da alçada do usuário | Pedido deve ficar bloqueado ou exigir aprovação |

## Cenários de regressão

- Inclusão manual via interface.
- Inclusão via ExecAuto, se usada pelo cliente.
- Alteração de item já gravado.
- Exclusão/cancelamento quando permitido.
- Aprovação/liberação quando houver workflow.
- Integração com solicitação de compras.
- Integração posterior com documento de entrada.
- Validação de mensagens em tela via TIR/WebApp.
- Teste multi-filial quando o ambiente usar compartilhamento de tabelas.
- Teste com usuário comprador e usuário sem permissão.

## Massa de dados mínima

| Tipo | Massa |
|---|---|
| Fornecedor válido | SA2 ativo, sem bloqueio, com condição fiscal compatível |
| Fornecedor bloqueado | SA2 com status/regra que impeça compra |
| Produto válido | SB1 ativo, com unidade, grupo e NCM conforme política do cliente |
| Produto bloqueado | SB1 com regra que impeça compra |
| TES válida | SF4 compatível com compra e documento de entrada |
| TES inválida | SF4 incompatível com o tipo de operação |
| Centro de custo válido | CTT ativo e aceito pela regra |
| Centro de custo inválido | CTT inexistente, bloqueado ou incompatível |
| Usuário comprador | Permissão para incluir/alterar pedido |
| Usuário restrito | Sem alçada ou sem permissão para fluxo crítico |

## Estratégia PROBAT

Usar PROBAT para testar regras isoladas ADVPL/TLPP, principalmente quando a customização estiver encapsulada em função validável.

Casos ideais:

- validação de fornecedor;
- validação de produto;
- regra de centro de custo obrigatório;
- cálculo ou validação de alçada;
- validação de TES;
- normalização de mensagens de erro.

Exemplo de prompt para gerar teste PROBAT:

```text
Crie um teste PROBAT para uma função ADVPL que valida se centro de custo é obrigatório no MATA120 quando o produto pertence ao grupo X e o valor do item é maior que Y.
```

## Estratégia ExecAuto/FwModel

Usar ExecAuto ou FwModel para validar o fluxo técnico de inclusão/alteração quando o cliente usa integração, automação, carga ou processo sem interface.

Validar:

- retorno de sucesso/erro;
- gravação correta na SC7;
- mensagens retornadas;
- rollback em caso de falha;
- preenchimento automático de campos;
- comportamento multi-item;
- compatibilidade com a mesma regra da interface.

## Estratégia TIR/WebApp

Usar TIR quando a regra precisa ser comprovada pela interface, principalmente quando há mensagem, bloqueio visual, campos obrigatórios ou comportamento dependente de tela.

Validar:

- acesso à rotina;
- preenchimento de cabeçalho;
- inclusão de item;
- tentativa de gravação inválida;
- mensagem exibida;
- sucesso na gravação válida;
- evidência de tela antes e depois da ação.

## Evidências esperadas

- Print ou log da inclusão válida.
- Print ou log da mensagem de bloqueio.
- Registro SC7 gerado ou não gerado, conforme cenário.
- Log da automação ExecAuto/FwModel, quando aplicável.
- Resultado PROBAT para regra isolada.
- Evidência TIR para comportamento de interface.
- Massa usada no teste.
- Versão/release do Protheus e ambiente.

## Checklist rápido para analista

```text
[ ] Confirme release e dicionário local.
[ ] Confirme campos obrigatórios SX3.
[ ] Confirme gatilhos SX7.
[ ] Confirme se há ponto de entrada/customização.
[ ] Confirme se o fluxo usa solicitação/cotação antes do pedido.
[ ] Confirme se há regra de alçada.
[ ] Confirme se a regra vale por filial, produto, fornecedor ou usuário.
[ ] Teste interface e automação, se ambas existirem.
[ ] Gere evidência antes/depois.
[ ] Registre limitações e premissas.
```

## Prompt exemplo para uso da skill

```text
Monte uma matriz de testes para a rotina MATA120 considerando uma customização que obriga centro de custo quando o produto pertence ao grupo MATPRIMA e o valor total do item é maior que 5.000. Inclua cenários positivos, negativos, regressão, massa de dados, estratégia PROBAT, ExecAuto/FwModel e TIR.
```
