# Claude Code Plugin / Marketplace

Plugin: `protheus-qa`. Marketplace próprio: `protheus-qa-marketplace`.
Skill: `testing-protheus-routines`. **Versão: consultar [VERSION](VERSION)**; os dois manifestos devem estar sincronizados com esse arquivo.

## Manifestos

`.claude-plugin/plugin.json` aponta `skills` para `./`, preservando a skill na raiz. A origem no catálogo `.claude-plugin/marketplace.json` é um objeto, não uma string `github:`:

```json
{
  "source": "github",
  "repo": "danielmontagna86-source/claude-skill-protheus-qa",
  "ref": "main"
}
```

## Instalação pelo marketplace próprio

No terminal com Claude Code instalado:

```shell
claude plugin marketplace add danielmontagna86-source/claude-skill-protheus-qa
claude plugin install protheus-qa@protheus-qa-marketplace
claude plugin list
claude plugin details protheus-qa
```

O comando de registro recebe a origem. O nome do marketplace vem do JSON; não passe um nome extra antes da origem. O identificador de instalação combina `plugin@marketplace`.

Para validar os manifestos de um clone local:

```shell
claude plugin validate .
```

Esses comandos são instruções, não uma declaração de instalação ou de teste do cliente Claude Code realizado nesta entrega. A configuração acompanha `main`; para revisão de uma versão fixa, use o pacote da tag publicada.

## Instalação direta da skill

Alternativa por projeto: clonar na pasta `.claude/skills/testing-protheus-routines`, conforme [README](README.md). Não instale simultaneamente cópias divergentes por plugin e diretório local. A instalação não fornece Python, navegador, driver ou um ERP; consulte [TIR_QUICKSTART](TIR_QUICKSTART.md).

## Validação e distribuição

Após instalar, confirme que a skill aparece e produza um plano com os 13 itens canônicos, sem acesso ao ERP. O CI valida scripts, contrato e pacote; não autentica em Claude Code nem Protheus.

Este é um marketplace próprio. Não houve submissão, aprovação ou inclusão no catálogo oficial da Anthropic. O projeto também não possui certificação TOTVS.

Referências oficiais consultadas em 01/10/2026:
- https://code.claude.com/docs/en/plugin-marketplaces
- https://code.claude.com/docs/en/discover-plugins
