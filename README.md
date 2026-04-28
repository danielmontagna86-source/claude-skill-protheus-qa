# Claude Skill: ADVPL/Protheus QA Specialist

Claude Skill para criar planos, cenários, massas, casos e roteiros de testes para rotinas e customizações TOTVS Protheus.

> Nome público do repositório: `claude-skill-protheus-qa`  
> Nome real da skill no Claude: `testing-protheus-routines`

## Por que existem dois nomes?

O repositório usa um nome descritivo para GitHub:

```text
claude-skill-protheus-qa
```

Mas a skill, dentro do Claude, usa o nome definido no `SKILL.md`:

```yaml
name: testing-protheus-routines
```

Por isso, ao instalar localmente, clone este repositório dentro de uma pasta chamada:

```text
testing-protheus-routines
```

Isso evita confusão e garante que o Claude reconheça a skill corretamente.

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
├── evals/
├── INSTALL.md
├── USAGE.md
├── CHANGELOG.md
└── LICENSE
```

## Instalação

### Opção 1 - Instalação local no Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/danielmontagna86-source/claude-skill-protheus-qa.git ~/.claude/skills/testing-protheus-routines
```

Depois reinicie ou recarregue o Claude Code.

### Opção 2 - Instalação por projeto

Dentro do repositório de um projeto Protheus:

```bash
mkdir -p .claude/skills
git clone https://github.com/danielmontagna86-source/claude-skill-protheus-qa.git .claude/skills/testing-protheus-routines
```

### Opção 3 - Instalação futura por CLI

Quando o comando `claude skill install` estiver disponível no seu ambiente:

```bash
claude skill install https://github.com/danielmontagna86-source/claude-skill-protheus-qa
```

Se o comando instalar usando o nome do repositório, renomeie a pasta final para `testing-protheus-routines`.

## Como empacotar para upload no Claude.ai

```bash
git clone https://github.com/danielmontagna86-source/claude-skill-protheus-qa.git testing-protheus-routines
zip -r testing-protheus-routines.zip testing-protheus-routines
```

Depois envie o arquivo `testing-protheus-routines.zip` em Claude.ai > Customize > Skills.

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

## Documentação adicional

- `INSTALL.md`: instalação e publicação.
- `USAGE.md`: exemplos de uso.
- `CHANGELOG.md`: histórico de versões.

## Status

Versão inicial pública para validação técnica e evolução incremental.
