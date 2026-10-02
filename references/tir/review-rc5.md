# Revisão adversarial da rc.4 — candidata rc.5

## Base e alcance

Revisão solicitada pelo mantenedor sobre o código e os procedimentos construídos neste projeto. Base: `v0.2.0-rc.4`, commit `8e0ea2181bf10b65fc872fe22c8340336462ae16`. ZIP original: SHA-256 `8b520eb16574666a91d6ac740181761ddaa86feb0fad2b14ebd7b99ebe4baa65`. O conteúdo foi conferido contra a publicação antes da revisão.

Foram lidos os scripts de contratos, executor, coletor, empacotamento, verificação, CLI, auditoria e instalação; testes, modelos de segurança, metadados e guias de IA. Revisão realizada por IA, inspeção de código, fontes primárias e execução de controles sintéticos. Não é revisão humana externa, certificação TOTVS ou auditoria exaustiva de todas as condições possíveis.

## Achados reproduzidos e correções

As severidades abaixo são priorização técnica deste projeto, não pontuação CVSS nem prova de exploração em produção. Os exemplos foram construídos em diretórios/processos descartáveis, sem ERP.

| ID | Prioridade | Evidência na rc.4 | Correção e regressão |
|---|---|---|---|
| R5-01 | Alta — resultado | Um resultado PASS com `exit_code=124`, limpeza falha e quarentena foi aceito pelo coletor | Exigir saída inteira zero, limpeza REMOVED e evidência LOCAL_ONLY; erro não pode declarar ERP validado. Testes `EvidenceEnvelopeReviewTests`. |
| R5-02 | Alta — operacional | Um processo-filho que ignorava SIGTERM continuou escrevendo após a saída do líder e retorno de stop_tree | Encerrar também remanescentes do grupo POSIX; limitar taskkill e conferir retorno. Teste real com heartbeat de processo próprio em `OwnedProcessReviewTests`. |
| R5-03 | Média — distribuição | ZIP sintético com SKILL.md e skill.md foi declarado VERIFIED | Recusar colisões por caixa, nomes reservados Windows, caminhos não canônicos e conflitos arquivo/diretório. Testes `ArchiveReviewTests`. Não havia essa colisão no ZIP oficial. |
| R5-04 | Média — evidência | PNG com CRC correto e IDAT não descompactável foi aceito | Validar zlib, tamanho/layout de linhas, filtros, combinações de formato e Adam7; expansão limitada a 128 MiB. Testes `PngReviewTests`. Não autentica o conteúdo visual. |
| R5-05 | Baixa — contrato | `1e999` foi lido como infinito apesar da rejeição declarada de números não finitos | Rejeitar também overflow de float durante parse. Testes de overflow e controle finito. |
| R5-06 | Média — erro controlado | Validade da política numérica gerou AttributeError em vez de BLOCKED estruturado | Validar tipo e timestamp; teste de CLI confirma bloqueio sem abrir processo. |
| R5-07 | Média — identificação | Os três marcadores podiam repetir o mesmo texto genérico | Exigir marcadores distintos. Isso elimina repetição trivial, mas não prova que os marcadores identificam corretamente o ambiente real. |
| R5-08 | Média — integridade | O teste do pacote validava bytes e depois reabria o caminho, permitindo troca entre as duas etapas | Extrair a mesma cópia em memória que foi verificada. Teste substitui o arquivo entre verificação e extração. |

O contrato de 13 itens e os bytes de SKILL.md foram preservados. A baseline e as permissões do TIR não foram ampliadas. Resultados históricos incompletos não devem ser editados para satisfazer o novo contrato: devem ser preservados e, quando necessário, substituídos por uma nova execução autorizada.

## Testes e distinções necessárias

A suíte original de **104 testes offline** passou novamente antes das correções. Foram acrescentados **37 testes** de regressão/integração offline, totalizando **141 testes**. Os controles novos foram confrontados com a implementação anterior e utilizados na correção. Falhas de subtests não são contadas como novos métodos de teste.

A validação local usa Python 3.13.5 apenas para as ferramentas offline. A matriz GitHub usa Python 3.12 Windows/Linux, testa checkout e ZIP e repete a instalação/importação do TIR em venv isolada. Os resultados efetivos pertencem aos JSONs/logs dos runs; este documento não antecipa a conclusão de jobs pendentes.

O fluxo completo pai → worker → coletor é testado com helper simulado e mantém `execution_mode=simulated` / `erp_validated=false`. O teste de encerramento usa processos reais próprios, não navegador ou ERP. Os testes de PNG/ZIP usam arquivos sintéticos e não evidências empresariais.

O workflow complementar acrescenta CodeQL Python com `security-and-quality`, relatório de cobertura de linhas/branches das ferramentas offline e instalação PowerShell em projeto descartável. Na instalação, os comandos da documentação são usados com download substituído por cópia de fixtures locais. São conferidos destinos Claude Code/Codex, integridade dos arquivos, recusa de sobrescrita e recusa de checksum incorreto. Não é instalação em um cliente IA real, teste de download público ou confirmação de descoberta automática.

Cobertura abaixo de 100% deve permanecer visível. Um relatório do processo principal não mede automaticamente os subprocessos nem o ERP. CodeQL concluído não significa ausência de alertas: conferir SARIF e resultados antes de declarar o parecer.

## Fontes primárias consultadas

Consulta em 01/10/2026, horário de São Paulo. As decisões acima são análise própria apoiada nos contratos documentados:

1. [Python 3.12 — subprocess, sessão e grupos](https://docs.python.org/3.12/library/subprocess.html)
2. [Python 3.12 — zipfile e segurança de extração](https://docs.python.org/3.12/library/zipfile.html)
3. [Python 3.12 — json e números não finitos](https://docs.python.org/3.12/library/json.html)
4. [Microsoft — regras de nomes Windows](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file)
5. [W3C — PNG Third Edition, IHDR, IDAT, filtros e interlace](https://www.w3.org/TR/png-3/)
6. [Claude Code — manifestos de plugin e caminhos de skills](https://code.claude.com/docs/en/plugins-reference)
7. [OpenAI — skills do Codex](https://developers.openai.com/codex/skills)
8. [GitHub — configuração avançada de CodeQL](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configuring-advanced-setup-for-code-scanning)
9. [TOTVS — fachada TIR da tag fixada](https://github.com/totvs/tir/blob/v2.14.10/tir/main.py)

A action CodeQL foi fixada no commit `2892aa5e19bbd11bc0cff5427e3b750a04d9e3c2`, resolvido a partir da tag oficial v4. Não foi usada uma API TIR inferida apenas por seu nome.

## Pendências e limites

Persistem a necessidade de avaliar os avisos de dependências, o piloto real autorizado, a compatibilidade navegador/driver e a confirmação dos marcadores e da massa da instalação do usuário. O runner não suporta gravações, SQL ou execução arbitrária e não contém processos que deliberadamente escapem do grupo/sessão por mecanismos do sistema operacional.

Não houve teste funcional no Protheus, compilação ADVPL/TLPP, execução PROBAT/ExecAuto/FwModel, benchmark comportamental com modelo/cliente IA ou aprovação humana do resultado esperado. As fichas de rotina são apoio de planejamento, não certificação por release/dicionário. Nenhuma conclusão desta revisão autoriza produção.
