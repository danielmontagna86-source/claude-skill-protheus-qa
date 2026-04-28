# Guia SX3, SX7 e SXB para QA

## Objetivo

Orientar testes para validações, gatilhos e fórmulas configuradas no dicionário do Protheus.

## SX3 - Campos e validações

Use quando a customização altera:

- validação de campo;
- obrigatoriedade;
- gatilho de preenchimento indireto;
- help/mensagem;
- máscara/tamanho;
- regra de bloqueio.

### Testes recomendados

- Valor válido deve ser aceito.
- Valor inválido deve ser bloqueado.
- Campo obrigatório não deve aceitar vazio.
- Mensagem deve orientar o usuário.
- Gravação final deve refletir o valor correto.

## SX7 - Gatilhos

Use quando a regra preenche ou altera campos automaticamente.

### Testes recomendados

- Campo origem preenchido corretamente.
- Campo destino atualizado corretamente.
- Gatilho não deve sobrescrever valor manual indevido.
- Gatilho deve respeitar empresa/filial/parâmetros.
- Efeito colateral deve ser validado na tabela.

## SXB - Fórmulas

Use quando a customização depende de fórmula/cálculo configurado.

### Testes recomendados

- Entrada normal.
- Entrada zerada.
- Entrada nula/vazia.
- Limites e arredondamento.
- Impacto em gravação e relatórios.

## Evidências

- mensagem exibida;
- valor gravado;
- campo alterado;
- consulta em tabela;
- print/log quando visual;
- massa usada.

## Regra

Nunca assumir o conteúdo de SX3, SX7 ou SXB sem fonte do ambiente, exportação do dicionário, TDN ou confirmação do usuário.
