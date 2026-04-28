# Claude Code Plugin / Marketplace

Este repositório está preparado para funcionar como plugin do Claude Code e também como fonte de marketplace self-hosted.

## Plugin

```text
Nome do plugin: protheus-qa
Versão: 0.1.0
Manifesto: .claude-plugin/plugin.json
Skill carregada: testing-protheus-routines
Arquivo principal da skill: SKILL.md
```

O manifesto do plugin aponta para a skill existente na raiz do repositório:

```json
{
  "skills": "./"
}
```

Isso evita duplicar a árvore de arquivos e mantém compatibilidade com a instalação manual da Claude Skill.

## Marketplace self-hosted

O catálogo local do marketplace está em:

```text
.claude-plugin/marketplace.json
```

Ele expõe o plugin:

```text
protheus-qa
```

com origem no repositório:

```text
github:danielmontagna86-source/claude-skill-protheus-qa
```

## Instalação manual da Skill

Para instalar como skill local:

```bash
mkdir -p ~/.claude/skills

git clone https://github.com/danielmontagna86-source/claude-skill-protheus-qa.git \
~/.claude/skills/testing-protheus-routines
```

## Instalação como plugin Claude Code

Clone o repositório:

```bash
git clone https://github.com/danielmontagna86-source/claude-skill-protheus-qa.git
cd claude-skill-protheus-qa
```

Depois use o fluxo de plugins da sua versão do Claude Code para instalar o plugin a partir do repositório local ou remoto.

Sugestão de referência operacional:

```bash
claude plugin marketplace add protheus-qa-marketplace https://github.com/danielmontagna86-source/claude-skill-protheus-qa
claude plugin install protheus-qa
```

Se sua versão do Claude Code usar comandos interativos, use o menu/comando de plugins para adicionar este repositório como marketplace ou fonte de plugin.

## Submissão ao marketplace oficial

Este repositório já contém os arquivos técnicos necessários para distribuição como plugin:

```text
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
SKILL.md
```

Para aparecer no marketplace oficial da Anthropic/Claude Code, ainda é necessário passar pelo processo oficial de submissão/revisão da Anthropic. Esse processo não é feito automaticamente por este repositório.

## Teste rápido após instalação

Use um prompt como:

```text
Monte testes para MATA120 com validação de centro de custo obrigatório.
```

A resposta esperada deve incluir plano de QA, cenários positivos, negativos, regressão, massa de dados, técnica recomendada, evidência e limitações.
