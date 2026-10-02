# Instalação — Protheus QA

**Procedimento da versão 0.2.0-rc.4 · Daniel Montagna / Protheus IA Lab**

[Início](README.md) · [Instalar com IA](INSTALL_WITH_AI.md) · [Usar com IA](USAGE_WITH_AI.md) · [Preparar execução TIR](TIR_QUICKSTART.md)

## 1. Escolha o que será instalado

| Objetivo | Necessário | Não é necessário nesta etapa |
|---|---|---|
| Usar a skill para planejar/revisar QA | Claude Code ou Codex já configurado; arquivos da skill no projeto | Python, TIR, navegador automatizado ou credenciais do ERP |
| Validar as ferramentas offline | Python 3.12; pacote extraído | TIR e acesso ao Protheus |
| Executar consulta TIR em homologação | Runtime, navegador/driver, perfil, caso e autorização externa | Produção; operações de gravação não são suportadas |

**Instalar a skill não instala o TIR nem autoriza acesso ao ERP.** A pré-release mantém os riscos de dependências e os limites descritos em [SECURITY.md](SECURITY.md).

O repositório chama-se `claude-skill-protheus-qa`. O nome da skill e de sua pasta final é **`testing-protheus-routines`**. Não renomeie o `SKILL.md`.

## 2. Baixe o pacote da release

Abra a [release v0.2.0-rc.4](https://github.com/danielmontagna86-source/claude-skill-protheus-qa/releases/tag/v0.2.0-rc.4). Baixe os assets `testing-protheus-routines.zip` e `SHA256SUMS.txt`. Não confunda o pacote instalável com o botão **Source code (zip)** ou com o ZIP externo de um artifact do GitHub Actions.

A pasta interna deve ser `testing-protheus-routines/`, contendo `SKILL.md`, `VERSION`, scripts, referências e estes guias. Leia as notas da release e o código antes de executar scripts. Checksum verifica integridade contra o valor publicado; não é assinatura independente nem certificação de segurança.

## 3. Windows — instalação por projeto

Abra o PowerShell na **raiz do projeto onde a IA será usada**, não na pasta de produção do Protheus. Confira o caminho com `Get-Location`. O procedimento não exige administrador nem altera a política de execução do PowerShell.

### 3.1 Download e conferência

Este bloco acessa apenas o GitHub para baixar os dois assets. Se a rede corporativa bloquear, use o download aprovado pela empresa; não desligue TLS, proxy ou proteção de endpoint.

```powershell
$ErrorActionPreference = 'Stop'
$Version = '0.2.0-rc.4'
$Base = "https://github.com/danielmontagna86-source/claude-skill-protheus-qa/releases/download/v$Version"
$Stage = Join-Path ([IO.Path]::GetTempPath()) ('protheus-qa-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $Stage | Out-Null
$Zip = Join-Path $Stage 'testing-protheus-routines.zip'
$Checksums = Join-Path $Stage 'SHA256SUMS.txt'
Invoke-WebRequest -UseBasicParsing -Uri "$Base/testing-protheus-routines.zip" -OutFile $Zip
Invoke-WebRequest -UseBasicParsing -Uri "$Base/SHA256SUMS.txt" -OutFile $Checksums
$Match = [regex]::Match((Get-Content -LiteralPath $Checksums -Raw), '(?m)^([a-fA-F0-9]{64})\s+testing-protheus-routines\.zip\s*$')
if (-not $Match.Success) { throw 'Checksum ausente ou formato inesperado.' }
$Actual = (Get-FileHash -LiteralPath $Zip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Actual -ne $Match.Groups[1].Value.ToLowerInvariant()) { throw 'Checksum divergente: interrompa.' }
Expand-Archive -LiteralPath $Zip -DestinationPath $Stage
$Source = Join-Path $Stage 'testing-protheus-routines'
if (-not (Test-Path -LiteralPath (Join-Path $Source 'SKILL.md'))) { throw 'Estrutura de skill invalida.' }
if ((Get-Content -LiteralPath (Join-Path $Source 'VERSION') -Raw).Trim() -ne $Version) { throw 'Versao divergente.' }
Write-Output "Pacote conferido em: $Source"
```

### 3.2 Revise e copie para um único agente

Leia `SKILL.md`, `SECURITY.md` e os scripts na pasta exibida antes de continuar. No **mesmo terminal**, selecione `claude` ou `codex`. O destino deve estar ausente; uma instalação existente interrompe a cópia, sem sobrescrita.

```powershell
$Agent = 'claude' # Troque por 'codex' para instalar no Codex.
$Project = (Get-Location).Path
$Paths = @{ claude = '.claude\skills'; codex = '.agents\skills' }
if (-not $Paths.ContainsKey($Agent)) { throw 'Agente invalido.' }
$Parent = Join-Path $Project $Paths[$Agent]
$Destination = Join-Path $Parent 'testing-protheus-routines'
if (Test-Path -LiteralPath $Destination) { throw 'Skill ja existe. Siga a secao Atualizacao.' }
if (-not (Test-Path -LiteralPath $Parent)) { New-Item -ItemType Directory -Path $Parent -Force | Out-Null }
Copy-Item -LiteralPath $Source -Destination $Destination -Recurse
Get-Content -LiteralPath (Join-Path $Destination 'VERSION')
Test-Path -LiteralPath (Join-Path $Destination 'SKILL.md')
Write-Output "Skill copiada para: $Destination"
```

Resultado esperado: versão `0.2.0-rc.4`, `True` e o caminho correto. Isso comprova cópia/estrutura, não descoberta pelo agente nem homologação. Abra uma nova sessão da IA e faça o teste da seção 6.

Não faça clone Git dentro da pasta de skills de outro repositório: isso pode criar um repositório aninhado em vez de arquivos normalmente compartilháveis. O pacote extraído não contém `.git`. Para compartilhar com a equipe, revise o diff e versione **somente a pasta instalada**; nunca inclua workspace, evidências ou segredos.

## 4. Outros caminhos e clientes

| Cliente/escopo | Caminho final |
|---|---|
| Claude Code por projeto | `.claude/skills/testing-protheus-routines/SKILL.md` |
| Claude Code pessoal | `~/.claude/skills/testing-protheus-routines/SKILL.md` |
| Codex por projeto | `.agents/skills/testing-protheus-routines/SKILL.md` |
| Codex pessoal | `~/.agents/skills/testing-protheus-routines/SKILL.md` |

No Windows, `~` corresponde ao diretório do usuário, acessível por `$HOME`. Prefira o escopo por projeto; só instale no pessoal mediante decisão explícita. Não mantenha duas versões da mesma skill concorrendo no mesmo agente. Usar os dois agentes é possível, mas atualize ambas as cópias a partir do mesmo pacote.

No Linux/macOS, baixe e confira o mesmo pacote, extraia em uma pasta temporária e copie a pasta interna para o destino correspondente. Não são necessárias instalação global ou permissões de administrador para a skill. A homologação do runtime TIR é uma etapa separada.

No Claude.ai: com Skills e execução de código habilitadas conforme a política da conta, abra **Customize > Skills > + > Create skill > Upload a skill** e envie o ZIP instalável. A interface e as políticas podem variar; consulte a fonte oficial abaixo. A sessão hospedada não ganha acesso ao seu PC, VPN ou ERP apenas por receber a skill.

O pacote inclui metadados de plugin. Clientes Claude Code que carregam esse formato podem mostrar um comando com namespace; use o nome efetivamente listado pelo cliente. [MARKETPLACE.md](MARKETPLACE.md) descreve a distribuição alternativa como plugin. Publicação própria não significa inclusão em catálogo oficial.

## 5. Validação offline opcional

Com Python 3.12 já instalado, na raiz da **pasta da skill** copiada, execute um comando por vez. Não avance após retorno diferente de zero.

```powershell
py -3.12 scripts/validate_skill.py
py -3.12 scripts/validate_tir_release.py
py -3.12 scripts/run_local_checks.py --output C:\ProtheusQA\reports\onboarding-tests.json
```

O relatório deve indicar `scope=offline_tools_only`, zero falhas/erros/skips e `erp_validated=false`. A contagem exata está no relatório da versão executada. Esses comandos não instalam TIR e não acessam o ERP. Se Python estiver ausente, a instalação para uso de instruções continua possível; não declare que os testes foram executados.

Para desenvolver/gerar um ZIP, mantenha o clone em pasta separada dos projetos consumidores e use `scripts/package_skill.py`. O resultado fica em `dist/testing-protheus-routines.zip`; o checksum em `dist/SHA256SUMS.txt`. Prefira a tag revisada, não atualização irrestrita pela `main`.

## 6. Primeiro uso e confirmação da descoberta

Abra o cliente no projeto escolhido. Cole este texto **na conversa com a IA**, não no PowerShell:

```text
Use testing-protheus-routines. Primeiro confirme o caminho do SKILL.md
carregado e leia VERSION. Informe se encontrou outra cópia com o mesmo nome.
Leia também USAGE_WITH_AI.md. Não acesse o ERP, não peça credenciais e
não instale dependências. Explique como esta skill organiza um plano QA
nos 13 itens canônicos, sem inventar dados de uma rotina.
```

Se o cliente não descobrir a skill, informe o caminho completo do `SKILL.md`, abra nova sessão e confira as políticas do agente. Leitura manual do arquivo ajuda o diagnóstico, mas não prova que a descoberta automática funcionou. Não altere `AGENTS.md`, `CLAUDE.md` ou permissões globais para esconder esse problema.

## 7. Atualização, rollback e remoção

Baixe uma versão explícita, confira checksum e leia as mudanças. Feche a sessão que usa a skill. Faça backup da pasta atual **fora de qualquer diretório de descoberta de skills**. Instale a nova pasta inteira em destino vazio, valide e reabra a sessão. Não misture arquivos por cima da versão antiga, não use `git pull` indiscriminado e não edite o pacote histórico da release.

Para rollback, retire a cópia nova, restaure o backup revisado e confirme `VERSION`. Para remover, mova apenas a pasta `testing-protheus-routines` instalada para fora dos diretórios de skills. Não remova fontes, workspace, venv, política ou evidências como parte dessa operação.

## 8. Problemas comuns

| Sintoma | Ação |
|---|---|
| `SKILL.md` não encontrado | Verifique se extraiu um ZIP externo de Actions ou criou uma pasta duplicada |
| Destino já existe | Pare, compare versões e faça atualização com backup |
| IA não encontra a skill | Confira projeto, caminho, duplicatas, política e nova sessão |
| `py -3.12` ausente | Use instruções sem runtime ou solicite instalação aprovada do Python |
| Modelo de perfil/caso retorna `BLOCKED` | Esperado: os exemplos estão incompletos/desabilitados; não remova as barreiras |
| TIR não importa ou há alertas de dependência | Consulte a auditoria e [TIR_QUICKSTART.md](TIR_QUICKSTART.md); não atualize bibliotecas isoladamente |

## Fontes de instalação e descoberta

Consultadas em 01/10/2026. Os comandos deste projeto são procedimentos próprios; os caminhos e a descoberta foram conferidos nas documentações dos clientes.

- [Claude Code — skills](https://code.claude.com/docs/en/skills)
- [OpenAI — skills locais no Codex](https://developers.openai.com/codex/skills)
- [OpenAI — personalização e caminhos](https://learn.chatgpt.com/docs/customization/overview)
- [Anthropic — upload e uso no Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
