# Guia ExecAuto e FwModel

## Uso correto

Use ExecAuto quando a rotina possuir execução automática documentada ou consolidada no ambiente.

Use FwModel quando a rotina for MVC/modelo e o objetivo for validar regra, persistência ou comportamento do modelo sem depender da tela.

## Quando priorizar

- Inclusão técnica de título, pedido, solicitação, documento ou cadastro.
- Alteração e exclusão controlada.
- Validação de gravação em tabela.
- Teste funcional repetível sem dependência visual.

## Quando não usar

- Para validar mensagem visual, layout, clique, browse ou usabilidade.
- Para processo sem massa reversível.
- Quando a rotina automática não for documentada ou segura.

## Padrão de teste ExecAuto

1. Preparar ambiente, empresa e filial.
2. Preparar massa base.
3. Montar arrays de cabeçalho/itens/perguntas conforme rotina.
4. Executar rotina automática.
5. Capturar erro/retorno.
6. Validar tabelas afetadas.
7. Limpar ou sinalizar massa criada.

## Padrão de teste FwModel

1. Carregar modelo da rotina.
2. Definir operação: inclusão, alteração ou exclusão.
3. Popular campos necessários.
4. Validar modelo.
5. Confirmar operação.
6. Validar persistência.

## Evidências

- retorno da execução;
- variável de erro da rotina automática, quando aplicável;
- registro criado/alterado/excluído;
- consulta em tabela;
- log técnico;
- massa usada.

## Cuidados

- Nunca assumir campos sem fonte.
- Confirmar operação e arrays na documentação da rotina.
- Garantir massa reversível.
- Evitar teste destrutivo em ambiente não controlado.
