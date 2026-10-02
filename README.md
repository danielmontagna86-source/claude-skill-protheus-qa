# Protheus QA — testing-protheus-routines

**Daniel Montagna / Protheus IA Lab · versão 0.2.0-rc.4**

Skill para planejar e revisar testes de rotinas e customizações TOTVS Protheus, com TDN, ADVPL/TLPP, PROBAT, ExecAuto/FwModel e TIR. Mantém o nome `testing-protheus-routines` e o contrato original de 13 itens do [SKILL.md](SKILL.md).

## Comece aqui

| Preciso de... | Procedimento |
|---|---|
| Instalar manualmente no meu projeto | [INSTALL.md — Windows, Claude Code, Codex e validação](INSTALL.md) |
| Pedir à IA para instalar | [INSTALL_WITH_AI.md — prompt pronto e limites](INSTALL_WITH_AI.md) |
| Usar a skill com IA no trabalho | [USAGE_WITH_AI.md — primeiro uso e prompts por tarefa](USAGE_WITH_AI.md) |
| Preparar execução TIR autorizada | [TIR_QUICKSTART.md — runtime e operação de consulta](TIR_QUICKSTART.md) |

A instalação básica copia a skill; **não exige TIR e não acessa o ERP**. Os guias também acompanham o ZIP instalável. A rc.4 atualiza o onboarding e sua validação; não amplia o executor nem elimina os riscos identificados na rc.3.

## O que esta versão entrega

A especialização TIR 2.14.10 acrescenta seis comandos: inspeção de fontes sem regravação, validação de caso/perfil, preflight estático, geração determinística, executor controlado e verificação de evidências. A execução liberada é **um caso de consulta por processo, em homologação segregada**. Gravações e rotinas transacionais não são suportadas pelo executor desta pré-release.

**Testes offline e publicação não equivalem a homologação no ERP.** Não houve validação funcional em uma instalação Protheus nesta entrega. Os testes com helper simulado registram `execution_mode=simulated` e `erp_validated=false`.

Para preparar uma execução autorizada, consulte o **[guia prático Windows e operação](TIR_QUICKSTART.md)**. Consulte [limites de segurança](SECURITY.md), [baseline TIR](references/tir/baseline-2.14.10.md), [notas da versão](RELEASE_NOTES/v0.2.0-rc.4.md) e [avaliações comportamentais pendentes](evals/tir-behavioral.md).

## Segunda revisão técnica

A rc.3 acrescenta validação de PNG e observações, encerramento em interrupções, relatório de falha de limpeza, snapshot da aprovação e reprodução binária do pacote entre Windows/Linux. Veja o [code review e fontes primárias](references/tir/review-2026-10-01.md).

**Dependências: não há aprovação de segurança para o runtime.** O TIR fixado inclui bibliotecas com avisos conhecidos, incluindo Requests 2.31.0. A publicação anexa auditoria e inventário; sucesso dos testes não elimina esses riscos. A política exige `dependency_risks_reviewed=true` do responsável autorizado antes de uma execução real. Isso é uma declaração de revisão, não assinatura digital ou correção de CVEs.

## Instalação por projeto

Use o pacote da release `v0.2.0-rc.4`, conferindo `SHA256SUMS.txt`, e siga [INSTALL.md](INSTALL.md). A pasta final é `.claude/skills/testing-protheus-routines` para Claude Code ou `.agents/skills/testing-protheus-routines` para Codex. O guia interrompe a instalação se o destino já existir e evita repositórios Git aninhados.

Para instalação assistida, copie o prompt de [INSTALL_WITH_AI.md](INSTALL_WITH_AI.md) no agente aberto no projeto. Sem acesso à máquina, a IA apenas orienta; não declare instalação local a partir de uma resposta textual.

## Uso da skill

```text
Use testing-protheus-routines para analisar esta customização.
Confirme fontes, riscos, massa e resultado esperado.
Separe PROBAT, ExecAuto/FwModel e TIR conforme o risco.
Preserve os 13 itens. Não invente campos, mensagens ou APIs.
Gere apenas artefatos locais. Não execute no ERP.
```

A escolha da técnica permanece: regra isolada → PROBAT confirmado; operação automática documentada → ExecAuto; modelo MVC confirmado → FwModel; interface e mensagem visual → TIR. Quando faltar evidência, entregar roteiro e declarar a lacuna. Não presumir que toda rotina disponibiliza ExecAuto/FwModel.

## Ferramentas

| Comando em `scripts/` | Finalidade | Acessa o ERP? |
|---|---|---|
| `inspect_sources.py` | Hash, encoding explícito e símbolos lexicais; preserva bytes | Não |
| `validate_case.py` | Contrato, fontes, esperado independente e argumentos públicos | Não |
| `preflight_tir.py` | Python/pacote/configuração, sem importar TIR | Não |
| `generate_tir_tests.py` | Caso, perfil, código de revisão e manifesto determinístico | Não |
| `run_tir_suite.py` | Verificação de autorização e execução isolada de consulta | Somente com todas as barreiras atendidas |
| `collect_evidence.py` | Confere integridade dos resultados/artefatos locais | Não |

`verify_tir_api.py --fetch` é uma checagem de desenvolvimento com acesso explícito ao código público fixado da TOTVS. Não abre navegador nem acessa o ERP.

## Contrato e conhecimento preservados

O [SKILL.md](SKILL.md) continua sendo a fonte do nome, descoberta e contrato obrigatório de 13 itens. O arquivo não foi reescrito nesta evolução. As fichas em [routines/INDEX.md](routines/INDEX.md), referências de backend, templates, exemplos e avaliações anteriores permanecem no repositório.

Módulos prioritários: Financeiro, Faturamento, Estoque e Compras. A presença de uma ficha não certifica aquela rotina no seu ambiente. Campos, filial, release, customizações, massa e resultado esperado exigem confirmação.

## Validação e pacote

```powershell
python -m unittest discover -s tests -v
python scripts/validate_skill.py
python scripts/validate_tir_release.py
python scripts/verify_tir_api.py --fetch
python scripts/package_skill.py
```

A automação GitHub testa o checkout e o ZIP em Python 3.12 no Windows e no Linux, compara os pacotes byte a byte, confere a API e faz uma instalação/importação isolada do TIR com auditoria de dependências. Após publicar, baixa os assets novamente e verifica os bytes e o commit. A auditoria pode concluir com vulnerabilidades encontradas; esse status é publicado, não convertido em aprovação de segurança. Seus resultados devem ser lidos no run correspondente; a existência do workflow não significa que ele passou.

O pacote é criado em `dist/testing-protheus-routines.zip`. `dist/SHA256SUMS.txt` contém o checksum. Dados de execução, configuração com credenciais e evidências não pertencem à distribuição.

## Fora do escopo

Deploy de Protheus, atualização de RPO, patches, reinício de serviços, administração de produção, execução financeira/fiscal real e alterações diretas em tabelas. O workflow deste repositório serve apenas à validação e distribuição da própria skill.

## Documentação

[Instalação](INSTALL.md) · [Instalação com IA](INSTALL_WITH_AI.md) · [Uso com IA](USAGE_WITH_AI.md) · [Uso e cenários](USAGE.md) · [Guia TIR](TIR_QUICKSTART.md) · [Changelog](CHANGELOG.md) · [Segurança](SECURITY.md) · [Licença MIT](LICENSE).

O marketplace é próprio; a publicação neste GitHub não significa inclusão no catálogo oficial da Anthropic nem homologação pela TOTVS.
