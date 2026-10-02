# Changelog

Todas as mudanças relevantes deste projeto serão registradas aqui.

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
