# 0.2.0-rc.5 — revisão adversarial e regressão

Corrige finalização PASS inconsistente, descendente POSIX sobrevivente, PNG ilegível com CRC válido, colisões Windows em ZIP, troca de arquivo após verificação, overflow JSON, validade de autorização inválida e marcadores de identidade duplicados. Acrescenta testes e verificações CodeQL/cobertura/instalação. Runtime TIR e alertas de dependência não foram alterados; não há homologação ERP.

# Changelog

## 0.2.0-rc.4 — Procedimentos de instalação e uso com IA

- INSTALL.md revisado: skill versus runtime, release fixa, checksum, destino sem sobrescrita, validação offline, descoberta, atualização e rollback.
- INSTALL_WITH_AI.md: prompts de instalação por projeto, verificação e preparação separada/autorizada do runtime.
- USAGE_WITH_AI.md: primeiro uso, contexto mínimo, prompts de análise, regressão, geração offline e interpretação de evidências.
- README e guias existentes conectados; os novos guias entram no pacote e recebem testes de links/contrato/CLI/distribuição.
- Sem alteração do SKILL.md canônico, do motor TIR ou dos modelos de segurança. Riscos de dependências e homologação ERP continuam pendentes.


Todas as mudanças relevantes deste projeto serão registradas aqui.

## 0.2.0-rc.3 - 2026-10-01

### Fixed

- PASS exige imagens existentes, estrutura PNG válida e observações vinculadas ao caso aprovado.
- Arquivos adicionais não escapam mais da integridade pelo nome summary.md.
- Tipos booleanos não substituem contadores inteiros; JSON e caminhos recebem limites adicionais.
- Interrupções encerram o processo próprio; falha de limpeza gera registro ERROR e quarentena.
- O hash de aprovação fica ligado ao snapshot validado, não a um arquivo posteriormente alterado.
- Pacotes byte-idênticos entre plataformas com textos normalizados e ZIP_STORED.

### Added

- Segunda revisão com regressões reproduzidas antes da correção e fontes primárias.
- Reexecução de testes a partir do ZIP, comparação entre builds e leitura dos assets após publicação.
- Instalação/importação TIR isolada e auditoria de dependências sem corrigir/ocultar achados.
- Revisão explícita de risco de dependências na autorização. Não é aprovação de segurança do runtime.

## 0.2.0-rc.2 - 2026-10-01

### Fixed

- Guia legado de marketplace atualizado: versão consultada em VERSION, origem GitHub tipada e comandos com identificação do marketplace.
- Exemplos de instalação separados de validação efetivamente executada.
- Correção documental; motor TIR e seus limites permanecem iguais aos da rc.1.

## 0.2.0-rc.1 - 2026-10-01

### Added

- Especialização TIR 2.14.10 com manifesto de API pública e verificação do blob oficial.
- Seis comandos de inspeção, validação, preflight, geração, execução controlada de consulta e coleta.
- Contratos estritos, hashes, autorização externa expiráveis, worker isolado e evidências locais.
- Testes determinísticos e controles negativos, sem conexão ao ERP.
- Guia Windows, segurança, templates desabilitados e avaliação comportamental explicitamente pendente.
- Workflow Python 3.12 Windows/Linux, pacote reproduzível e publicação condicionada às verificações.

### Changed

- Distribuição com inventário SHA-256 e exclusão de dados de execução.
- Origem GitHub no manifesto do marketplace corrigida para objeto tipado.
- Identidade, SKILL.md, contrato de 13 itens e fichas existentes preservados.

### Limitations

- Pré-release, não homologada em Protheus. Executor limitado a consulta; gravações/transações bloqueadas.
- Sem certificação TOTVS, benchmark comportamental concluído ou revisão humana externa.

## 0.1.0 - 2026-04-28

### Added

- Versão pública inicial da Claude Skill `testing-protheus-routines`.
- `SKILL.md` com instruções principais da skill.
- Referências para processo QA, TDN, PROBAT, ExecAuto/FwModel, TIR, evidências, customizações e SX3/SX7/SXB.
- Templates para caso de teste, PROBAT, ExecAuto e TIR.
- Fichas iniciais de rotinas Protheus:
  - FINA050 - Contas a Pagar;
  - MATA410 - Pedido de Venda;
  - MATA460 - Documento de Saída / Faturamento;
  - MATA120 - Pedido de Compras;
  - MATA010 - Cadastro de Produtos.
- Exemplos por técnica:
  - PROBAT;
  - ExecAuto;
  - FwModel;
  - TIR.
- Evals MVP com 6 cenários e checklist obrigatório dos 13 itens de resposta.
- Documentação pública de instalação e uso.

### Notes

- O repositório se chama `claude-skill-protheus-qa`.
- A skill declarada no Claude se chama `testing-protheus-routines`.
- A pasta de instalação deve ser `testing-protheus-routines`.
- Esta versão é um MVP público para validação técnica e evolução incremental.
