# Instalação da Claude Skill Protheus QA

## Nome do repositório x nome da skill

Este repositório se chama:

```text
claude-skill-protheus-qa
```

Mas a skill declarada em `SKILL.md` se chama:

```yaml
name: testing-protheus-routines
```

Para evitar problemas de descoberta pelo Claude, instale sempre usando a pasta final:

```text
testing-protheus-routines
```

## Instalação local no Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/danielmontagna86-source/claude-skill-protheus-qa.git ~/.claude/skills/testing-protheus-routines
```

Depois reinicie ou recarregue o Claude Code.

## Instalação em um projeto

Dentro do repositório de um projeto Protheus:

```bash
mkdir -p .claude/skills
git clone https://github.com/danielmontagna86-source/claude-skill-protheus-qa.git .claude/skills/testing-protheus-routines
```

Depois versionar no projeto, se desejar compartilhar com a equipe:

```bash
git add .claude/skills/testing-protheus-routines
git commit -m "Add Protheus QA Claude Skill"
```

## Atualização

### Instalação local

```bash
cd ~/.claude/skills/testing-protheus-routines
git pull
```

### Instalação por projeto

```bash
cd .claude/skills/testing-protheus-routines
git pull
```

## Empacotar para Claude.ai

Para subir manualmente no Claude.ai:

```bash
git clone https://github.com/danielmontagna86-source/claude-skill-protheus-qa.git testing-protheus-routines
zip -r testing-protheus-routines.zip testing-protheus-routines
```

Depois envie o arquivo `testing-protheus-routines.zip` em:

```text
Claude.ai > Customize > Skills
```

## Teste após instalação

Use um prompt simples:

```text
Monte testes para MATA120 com validação de centro de custo obrigatório.
```

A resposta esperada deve trazer:

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
