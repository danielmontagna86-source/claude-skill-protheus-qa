# Claude Skill: ADVPL/Protheus QA Specialist

Claude Skill para criar planos, cenários, massas, casos e roteiros de testes para rotinas e customizações TOTVS Protheus.

> Nome público do repositório: `claude-skill-protheus-qa`  
> Nome real da skill no Claude: `testing-protheus-routines`  
> Versão atual: `0.1.0`

## Fonte única da verdade

| Definição | Fonte oficial | Observação |
|---|---|---|
| Nome real da skill | `SKILL.md` > frontmatter `name` | Deve permanecer `testing-protheus-routines` |
| Descrição oficial da skill | `SKILL.md` > frontmatter `description` | Usada pelo Claude para descoberta e acionamento |
| Formato esperado de saída | `SKILL.md` > seção `Formato padrão de resposta` | Define os 13 itens obrigatórios |
| Versão atual | `VERSION` | Deve ser sincronizada com `CHANGELOG.md` e releases |
| Histórico de mudanças | `CHANGELOG.md` | Registra evolução funcional da skill |
| Pacote instalável | `dist/testing-protheus-routines.zip` | Gerado por `scripts/package_skill.py` |

Regra operacional: qualquer alteração de nome, versão ou formato de resposta deve começar pela fonte oficial acima. Outros arquivos apenas explicam ou refletem essas definições.

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
├── VERSION
├── references/
├── routines/
├── templates/
├── examples/
├── evals/
├── scripts/
├── RELEASE_NOTES/
├── INSTALL.md
├── USAGE.md
├── CHANGELOG.md
└── LICENSE
```

## Matriz artefato x finalidade

| Artefato | Finalidade | Como usar | Pode ser fonte oficial? |
|---|---|---|---|
| `SKILL.md` | Instrução principal da skill | Define comportamento, escopo, regras e formato de resposta | Sim, para nome, descrição e formato |
| `VERSION` | Versão atual do pacote | Deve acompanhar releases e changelog | Sim, para versão |
| `references/` | Consulta conceitual | Apoia regras gerais de QA, TDN, evidências, técnicas e anti-alucinação | Não, exceto como referência auxiliar |
| `routines/` | Fichas por rotina Protheus | Orienta tabelas, riscos, massa, cenários e evidências por rotina | Sim, para contexto local da rotina |
| `templates/` | Esqueletos reutilizáveis | Base para gerar casos, PROBAT, ExecAuto e TIR | Não, é modelo de preenchimento |
| `examples/` | Exemplos prontos | Demonstra aplicação da skill por técnica ou rotina | Não, é exemplo validável |
| `evals/` | Cenários de validação | Define critérios de aceite dos exemplos e do comportamento da skill | Sim, para validação |
| `scripts/` | Automação de validação e pacote | Valida estrutura e gera ZIP instalável | Não, é ferramenta operacional |
| `.github/workflows/` | Validação/release no GitHub Actions | Empacota, valida e prepara publicação versionada | Não, é automação de entrega |
| `RELEASE_NOTES/` | Notas por versão | Documenta conteúdo publicado em cada versão | Sim, para release publicada |
| `INSTALL.md` | Instalação | Explica modo local, projeto e Claude.ai | Não, é guia operacional |
| `USAGE.md` | Uso e exemplos | Explica prompts, critérios e ligação com evals | Não, é guia de uso |
| `CHANGELOG.md` | Histórico | Lista mudanças por versão | Sim, para histórico |

## Compatibilidade por modo de instalação

| Modo | Caminho/entrada | O que muda | Quando usar | Observação QA |
|---|---|---|---|---|
| Claude Code local | `~/.claude/skills/testing-protheus-routines` | Skill fica disponível para o usuário no ambiente local | Uso individual e recorrente | Bom para evolução rápida e validação técnica |
| Instalação por projeto | `.claude/skills/testing-protheus-routines` | Skill fica versionada junto do projeto Protheus | Times que querem padronizar QA por repositório | Melhor para rastreabilidade por cliente/projeto |
| Upload Claude.ai | `testing-protheus-routines.zip` | Usa pacote fechado com pasta raiz correta | Distribuição manual para ambiente Claude.ai | Deve usar ZIP gerado por `scripts/package_skill.py` |
| GitHub Actions artifact | Workflow `validate-and-package` | Gera artefato validado automaticamente | Distribuição interna e conferência antes de release | Não substitui release versionada |
| Release GitHub | Tag `vX.Y.Z` + ZIP | Publica versão imutável para instalação | Distribuição pública/versionada | Deve estar sincronizada com `VERSION` e `CHANGELOG.md` |

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

### Opção 3 - Upload para Claude.ai

Gere o pacote oficial:

```bash
python scripts/validate_skill.py
python scripts/package_skill.py
```

Depois envie o arquivo abaixo em Claude.ai > Customize > Skills:

```text
dist/testing-protheus-routines.zip
```

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

## Critérios de aceite por exemplo

| Exemplo | Eval correspondente | Critério mínimo de aceite |
|---|---|---|
| Customização FINA050 bloqueando título sem natureza | `evals/eval-mvp.md` > Eval 1 | Retornar 13 itens, classificar Financeiro/FINA050, usar SE2 e recomendar técnica conforme confirmação do ambiente |
| MATA410 com preço abaixo do mínimo | `evals/eval-mvp.md` > Eval 2 | Retornar 13 itens, usar SC5/SC6, separar PROBAT para regra e TIR para mensagem |
| MATA120 com centro de custo obrigatório | `evals/eval-mvp.md` > Eval 3 | Retornar 13 itens, usar SC7, definir fornecedor/produto/quantidade/preço/centro de custo e evidência |
| MATA010 com unidade e armazém padrão | `evals/eval-mvp.md` > Eval 4 | Retornar 13 itens, usar SB1 e considerar SB2/SB5 quando aplicável |
| MATA460 gerando documento de saída e financeiro | `evals/eval-mvp.md` > Eval 5 | Retornar 13 itens, usar SF2/SD2 e considerar SE1/SB2 conforme cenário |
| SX3/SX7 | `evals/eval-mvp.md` > Eval 6 | Retornar 13 itens, não inventar dicionário, pedir confirmação/exportação quando necessário |

## Validação

Use os cenários em `evals/eval-mvp.md` para verificar se a skill retorna o formato padrão com 13 itens obrigatórios.

```bash
python scripts/validate_skill.py
```

Saída esperada:

```text
Skill validation passed.
```

## Release versionada

A versão atual preparada é `0.1.0`.

Para publicar uma release versionada no GitHub:

1. confirme que `VERSION` contém `0.1.0`;
2. confirme que `CHANGELOG.md` possui a seção `0.1.0`;
3. gere o pacote com `python scripts/package_skill.py`;
4. crie a tag `v0.1.0`;
5. publique `dist/testing-protheus-routines.zip` como asset da release.

As notas da versão ficam em `RELEASE_NOTES/v0.1.0.md`.

## Documentação adicional

- `INSTALL.md`: instalação e publicação.
- `USAGE.md`: exemplos de uso.
- `CHANGELOG.md`: histórico de versões.
- `RELEASE_NOTES/`: notas de releases versionadas.

## Status

Versão pública `0.1.0` para validação técnica e evolução incremental.
