# Claude Skill: ADVPL/Protheus QA Specialist

Skill para criar planos, cenários, massas, casos e roteiros de testes para rotinas e customizações TOTVS Protheus.

## Objetivo

Transformar documentação TDN, rotinas Protheus, customizações ADVPL/TLPP e contexto funcional em:

- plano de QA;
- matriz de cenários;
- massa de dados;
- estratégia de automação;
- exemplos com PROBAT, ExecAuto/FwModel e TIR;
- evidências de validação.

## Escopo

A skill cobre QA e testes para:

- rotinas Protheus;
- pontos de entrada;
- pontos de entrada MVC;
- validações SX3;
- gatilhos SX7;
- fórmulas SXB;
- regras ADVPL/TLPP;
- ExecAuto;
- FwModel;
- TIR/WebApp;
- PROBAT/TLPP.

## Fora do escopo

Esta skill não é focada em:

- CI/CD;
- deploy;
- patch;
- T-Cloud;
- release;
- infraestrutura de entrega.

## Pilares

```text
TDN -> comportamento esperado
Customização -> risco
PROBAT -> regra isolada
ExecAuto/FwModel -> fluxo funcional técnico
TIR -> interface WebApp/APW
Evidência -> prova do resultado
```

## Estrutura

```text
.
├── SKILL.md
├── references/
├── routines/
├── templates/
├── examples/
└── evals/
```

## Instalação

### Opção 1 - Claude CLI

Quando o comando de instalação de skills estiver disponível no seu ambiente:

```bash
claude skill install https://github.com/danielmontagna86-source/claude-skill-protheus-qa
```

### Opção 2 - Instalação manual

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/danielmontagna86-source/claude-skill-protheus-qa.git ~/.claude/skills/claude-skill-protheus-qa
```

Depois reinicie ou recarregue o Claude Code para reconhecer a skill local.

## Módulos priorizados

- Financeiro
- Faturamento
- Estoque
- Compras

## Uso esperado

Exemplos de solicitações que devem acionar a skill:

```text
Monte testes para uma customização na FINA050.
Crie cenários para validar ponto de entrada na MATA410.
Gere massa de teste para Pedido de Compras MATA120.
Crie um template PROBAT para uma regra isolada ADVPL.
Crie um roteiro TIR para validar mensagem no WebApp.
```

## Validação

Use os cenários em `evals/eval-mvp.md` para verificar se a skill retorna o formato padrão com 13 itens obrigatórios.

## Status

Versão inicial para validação técnica e evolução incremental.
