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

Para evitar problemas de descoberta pelo Claude, a pasta final da skill deve ser sempre:

```text
testing-protheus-routines
```

## Caminho recomendado: pacote oficial

O pacote oficial deve ser o arquivo:

```text
testing-protheus-routines.zip
```

A estrutura interna do ZIP deve ser:

```text
testing-protheus-routines.zip
└── testing-protheus-routines/
    ├── SKILL.md
    ├── README.md
    ├── INSTALL.md
    ├── USAGE.md
    ├── examples/
    ├── evals/
    ├── references/
    ├── routines/
    ├── scripts/
    └── templates/
```

### Gerar pacote localmente

Na raiz do repositório:

```bash
python scripts/validate_skill.py
python scripts/package_skill.py
```

Saída esperada:

```text
dist/testing-protheus-routines.zip
```

### Gerar pacote pelo GitHub Actions

O workflow `.github/workflows/validate-and-package.yml` valida a skill e gera o artefato:

```text
testing-protheus-routines
```

Esse artefato contém o arquivo:

```text
dist/testing-protheus-routines.zip
```

Use esse ZIP para instalação no Claude.ai.

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
python scripts/validate_skill.py
```

### Instalação por projeto

```bash
cd .claude/skills/testing-protheus-routines
git pull
python scripts/validate_skill.py
```

## Instalação no Claude.ai

Opção recomendada:

1. Gere ou baixe `testing-protheus-routines.zip`.
2. Confirme que o ZIP contém a pasta raiz `testing-protheus-routines/`.
3. Envie o arquivo em:

```text
Claude.ai > Customize > Skills
```

## Empacotamento manual alternativo

Use somente se não for usar `scripts/package_skill.py`:

```bash
git clone https://github.com/danielmontagna86-source/claude-skill-protheus-qa.git testing-protheus-routines
zip -r testing-protheus-routines.zip testing-protheus-routines
```

Antes de enviar, valide que a pasta raiz dentro do ZIP é `testing-protheus-routines/`, e não `claude-skill-protheus-qa/`.

## Validação local

Execute:

```bash
python scripts/validate_skill.py
```

O retorno esperado é:

```text
Skill validation passed.
```

Se houver erro, corrija antes de empacotar ou distribuir.

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

## Checklist antes de distribuir

- `SKILL.md` existe na raiz.
- O `name` do frontmatter é `testing-protheus-routines`.
- O ZIP final se chama `testing-protheus-routines.zip`.
- A pasta raiz dentro do ZIP se chama `testing-protheus-routines/`.
- `python scripts/validate_skill.py` passa sem erro.
- `evals/eval-mvp.md` foi usado para validar respostas de exemplo.
