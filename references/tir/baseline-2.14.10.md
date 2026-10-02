# Baseline TIR 2.14.10

Data de pesquisa: 01/10/2026. Tag `v2.14.10`, commit `dbc12e7a0563174a3f6c16832046229d71d464cf`, release publicada em 25/09/2026. Fonte: https://github.com/totvs/tir/releases/tag/v2.14.10

O pacote de execução é `tir-framework`, módulo Python `tir`, baseline Python 3.12. Não acompanhar `main` automaticamente nem trocar dependências isoladamente. O preflight verifica Python e versão instalada por metadata, sem importar TIR. Isso não é um lockfile transitivo nem auditoria de vulnerabilidades.

A API utilizada está em `tir/main.py`; blob Git confirmado `082afe46702649276d994ea1e783e6e27cc6eef2`. `scripts/verify_tir_api.py` compara esse blob e as assinaturas por AST, sem executar o código. O manifesto é um SUBCONJUNTO suportado; ausência de um método não significa que a TOTVS não o oferece.

Fontes primárias: https://github.com/totvs/tir/blob/dbc12e7a0563174a3f6c16832046229d71d464cf/tir/main.py e https://github.com/totvs/tir/blob/v2.14.10/setup.py

PR #2131 acrescenta captura/transição de tela; #2134 corrige a espera por desbloqueio. Esses detalhes internos não se tornam APIs públicas por conversão para PascalCase. Clique disparado não é prova de resultado funcional. Fontes: https://github.com/totvs/tir/pull/2131 e https://github.com/totvs/tir/pull/2134

A implementação atual não afirma controlar o SmartClient desktop nativo, homologar todas as releases Protheus ou suportar todos os modos POUI/SSO.
