# Uso da Claude Skill Protheus QA

## Objetivo

Esta skill ajuda Claude a atuar como especialista em QA para rotinas e customizações TOTVS Protheus.

Ela deve transformar uma solicitação genérica como:

```text
Monte testes para MATA120.
```

em uma resposta estruturada com:

1. Objetivo do teste.
2. Base funcional/TDN usada.
3. Tipo de customização.
4. Risco QA.
5. Técnica recomendada.
6. Cenários positivos.
7. Cenários negativos.
8. Cenários de regressão.
9. Massa de dados.
10. Tabelas/campos.
11. Exemplo de automação ou roteiro.
12. Evidência esperada.
13. Limitações.

## Prompts recomendados

### Financeiro

```text
Crie testes para uma customização na FINA050 que bloqueia título a pagar sem natureza financeira.
```

### Faturamento

```text
Monte QA para customização na MATA410 que bloqueia pedido de venda com preço abaixo do mínimo.
```

```text
Monte testes para MATA460 validando geração de documento de saída, título financeiro e baixa de estoque.
```

### Compras

```text
Monte testes para MATA120 com validação de centro de custo obrigatório.
```

### Estoque

```text
Crie um roteiro de testes para MATA010 validando unidade de medida e armazém padrão.
```

### SX3/SX7/SXB

```text
Crie testes para uma validação SX3 no campo de natureza e um gatilho SX7 que preenche centro de custo automaticamente.
```

### PROBAT

```text
Crie um exemplo PROBAT para uma função ADVPL que valida preço mínimo no pedido de venda.
```

### ExecAuto

```text
Crie um roteiro ExecAuto conceitual para testar inclusão de título a pagar na FINA050.
```

### FwModel

```text
Crie um roteiro FwModel para validar cadastro de produto na MATA010.
```

### TIR

```text
Crie um roteiro TIR para validar mensagem visual na MATA410.
```

## Boas práticas

- Informe rotina, módulo e regra de negócio sempre que possível.
- Informe se existe ponto de entrada, SX3, SX7, SXB, ExecAuto, FwModel, TIR ou PROBAT envolvido.
- Informe tabelas/campos quando tiver certeza.
- Quando não houver certeza, peça para a skill marcar como hipótese.

## O que a skill não deve fazer

- Inventar campo, parâmetro ou ponto de entrada.
- Usar TIR para tudo.
- Usar PROBAT para validar tela.
- Usar ExecAuto para validar mensagem visual.
- Ignorar massa de dados e evidência.

## Validação

Use `evals/eval-mvp.md` para testar se a skill está respondendo no padrão correto.
