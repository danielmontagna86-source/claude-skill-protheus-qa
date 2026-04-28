# Processo QA Protheus

## Objetivo

Padronizar a criação de testes para rotinas e customizações TOTVS Protheus.

## Fluxo obrigatório

```text
1. Entender a rotina
2. Identificar comportamento padrão pela TDN ou ficha local
3. Identificar customização
4. Mapear risco
5. Escolher técnica
6. Criar cenários
7. Definir massa
8. Executar ou orientar execução
9. Coletar evidência
10. Registrar limitações
```

## Perguntas essenciais

- Qual módulo?
- Qual rotina?
- Qual operação: inclusão, alteração, exclusão, baixa, geração, aprovação, cancelamento?
- Existe ficha local em `routines/`?
- Existe documentação TDN?
- Existe customização ADVPL/TLPP?
- A customização está em ponto de entrada, SX3, SX7, SXB, ExecAuto, MVC, REST, job ou tela?
- Quais tabelas são afetadas?
- Qual evidência comprova que passou?

## Saída mínima aceitável

Toda resposta deve gerar pelo menos:

- cenários positivos;
- cenários negativos;
- massa de dados;
- técnica recomendada;
- evidência esperada;
- limitações.

## Critério de qualidade

Uma resposta boa não apenas sugere ferramenta. Ela conecta:

```text
rotina -> tabela -> risco -> técnica -> cenário -> massa -> evidência
```
