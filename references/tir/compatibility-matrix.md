# Compatibilidade e decisões de interface

| Item | Verificação implementada | Confirmação ainda necessária |
|---|---|---|
| Python | Exatamente major/minor 3.12 para worker real | Runtime/venv autorizado |
| TIR | Metadata igual a 2.14.10 | Instalação íntegra e dependências auditadas |
| API | Subconjunto conferido contra blob/AST fixado | Comportamento na interface real |
| Navegador | Configuração Chrome ou Firefox | Versão, driver, permissões e teste mínimo |
| URL | HTTPS, sem query/fragmento/credenciais e correspondência literal à política | TLS, rede e segregação reais |
| Empresa/filial/ambiente | Setup explícito, política e três marcadores de tela | Marcadores inequívocos e autorização |
| Release/build/RPO | Inventário declarado obrigatório | Identificação efetiva do ambiente |

A documentação da tag distingue `POUI`, `POUILogin`, `NewHome` e `SSOLogin`. A nota sobre `NewHome` a partir de 12.1.2610 e a nota de depreciação/remoção de `POUILogin` a partir de 12.1.2510 precisam ser confrontadas com o ambiente, não convertidas em garantia automática. O executor não expõe `POUI`, que não deve ser ligado genericamente para Protheus.

Fontes: https://github.com/totvs/tir/blob/v2.14.10/doc_files/source/configjson.rst e https://github.com/totvs/tir/blob/v2.14.10/tir/technologies/core/config.py

O ConfigLoader tem estado singleton; por isso cada caso usa um processo separado. Não misture destinos em uma sessão nem manipule o singleton privado para reutilizá-la.
