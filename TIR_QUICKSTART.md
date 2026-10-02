# TIR 2.14.10 — uso prático da pré-release

## 1. Escopo e preparação

O executor desta candidata aceita apenas consulta por APIs públicas selecionadas. Não preenche campos, grava, exclui, envia arquivos, executa SQL, chama métodos internos nem importa Python arbitrário fornecido pelo agente. O código gerado é um artefato de revisão; o worker usa a especificação validada no motor fixo. Executar esse arquivo gerado diretamente não autoriza uma sessão.

Uma consulta ainda pode disparar código customizado ao abrir a rotina. O responsável técnico precisa confirmar que a rotina e as navegações aprovadas não têm efeitos de negócio. O isolamento deve existir na rede, nas contas e nas integrações; não apenas no nome do ambiente.

Requisitos de execução: Python 3.12, pacote `tir-framework==2.14.10`, navegador/driver preparados, WebApp em HTTPS, usuário restrito, massa sintética, integrações bloqueadas e autorização externa. HTTP e URLs com credenciais, query string ou fragmento não são aceitos nesta versão. Nenhum script instala pacotes ou altera a infraestrutura automaticamente.

```powershell
py -3.12 -m venv .venv-tir
.\.venv-tir\Scripts\python.exe -m pip install "tir-framework==2.14.10"
.\.venv-tir\Scripts\python.exe -m pip check
```

Esses comandos não representam uma instalação já realizada. Registre dependências resolvidas, avalie vulnerabilidades e homologue navegador/driver antes do piloto. Não atualize Selenium isoladamente.

## 2. Perfil e caso

Use os modelos de `templates/tir/`. Eles contêm `PREENCHER`, destino `.invalid`, execução desabilitada e autorização expirada: devem falhar até serem completados com evidência real. Não use os dados dos testes unitários como cadastros Protheus.

Mantenha o workspace **fora da pasta da skill**. Exemplo de organização:

```text
C:\ProtheusQA\work\perfil.json
C:\ProtheusQA\work\caso.json
C:\ProtheusQA\work\bundle-001\
C:\ProtheusQA\runs\run-001\
C:\ProtheusQA\approvals\qa-001.json  # gravação restrita ao aprovador
```

No perfil, preencha versão/build/RPO, evidência da interface, programa inicial, módulo, data-base, empresa/grupo e filial. Preserve espaços significativos. Os três marcadores de tela devem identificar ambiente, grupo e filial; o caso acrescenta um marcador próprio da rotina. Sem marcadores confiáveis, não execute.

`NewHome`, `POUILogin` e `SSOLogin` são decisões verificadas no ambiente. O modelo não escolhe automaticamente as flags pela release. A presença de SSO no perfil não prova compatibilidade do seu fluxo nem permite contornar MFA.

No caso, registre fontes confirmadas, aprovação funcional do esperado, massa sintética e cada passo com `source_id`. A especificação usa somente argumentos nomeados (`kwargs`). O campo `expected` é obrigatório em `GetValue`/`IfExists`; em `CheckResult`, o esperado é `kwargs.user_value`. Comparações do motor são exatas, inclusive tipo, caixa e padding.

## 3. Comandos offline

Execute na raiz do clone, usando o Python da sua venv:

```powershell
python scripts/inspect_sources.py C:\Fontes\ZROTINA.prw --encoding cp1252
python scripts/validate_case.py --case C:\ProtheusQA\work\caso.json --profile C:\ProtheusQA\work\perfil.json
python scripts/preflight_tir.py --profile C:\ProtheusQA\work\perfil.json
python scripts/generate_tir_tests.py --case C:\ProtheusQA\work\caso.json --profile C:\ProtheusQA\work\perfil.json --output C:\ProtheusQA\work\bundle-001
```

A inspeção é lexical, não um parser/compilador ADVPL. O preflight não abre navegador, verifica rede, autentica ou comprova o driver; `READY_FOR_AUTHORIZATION` só indica as verificações estáticas implementadas. Python diferente de 3.12, pacote ausente/divergente e perfil desabilitado bloqueiam a execução.

O bundle contém `case.json`, `profile.json`, `test_case.py` e `manifest.json`. Sua geração é determinística e não sobrescreve um diretório existente. Habilitar o perfil após a geração altera seu hash: regenere um novo bundle e obtenha nova revisão/autorização.

## 4. Autorização externa

Um operador autorizado deve completar `templates/tir/approval.example.json`, fora do clone e do bundle, sob controle de acesso do sistema operacional. O agente não deve aprovar seu próprio trabalho.

A autorização fixa URL, ambiente, grupo, filial, hash do bundle, hash do motor exibido no preflight, aprovador, validade com timezone (até 24 horas), botões de navegação aprovados e limite total de execução. Também registra confirmação de isolamento das integrações e menor privilégio. Essas duas confirmações são declarações do operador, não verificações automáticas da rede.

No Windows, configure a ACL para impedir alterações por quem gera os casos. No POSIX, o runner rejeita política gravável por grupo/outros. **O JSON não tem assinatura digital, e `approved_by` não autentica uma pessoa.** Não execute com um agente que possa modificar a política, o runtime ou suas proteções de sistema.

## 5. Credenciais e execução

Não escreva senhas no JSON versionado, argumentos, prompt, commit ou exemplo. No PowerShell, uma sessão interativa autorizada pode usar:

```powershell
$cred = Get-Credential -Message "Usuario de homologacao Protheus"
$env:TIR_USER = $cred.UserName
$env:TIR_PASSWORD = $cred.GetNetworkCredential().Password
try {
    python scripts/run_tir_suite.py --bundle C:\ProtheusQA\work\bundle-001 --policy C:\ProtheusQA\approvals\qa-001.json --output C:\ProtheusQA\runs\run-001 --execute
} finally {
    Remove-Item Env:TIR_USER, Env:TIR_PASSWORD -ErrorAction SilentlyContinue
    $cred = $null
}
```

O runner cria uma configuração temporária em diretório restrito, copia o motor aprovado, inicia um processo Python isolado, verifica identidade antes de abrir a rotina e não faz retry de casos. Um processo por caso evita compartilhar o singleton de configuração do TIR entre ambientes. O limite externo tenta encerrar somente a árvore de processos criada por essa execução. Timeout exige revisão do estado; não autoriza uma nova tentativa automaticamente.

O worker chama `AssertTrue()` para verificar o estado de erros do TIR. Em `CheckResult(..., grid=True)`, processa `LoadGrid()` antes da conclusão. `GetValue` oferece o observado explícito; `CheckResult` nunca é interpretado como booleano.

## 6. Resultados

```powershell
python scripts/collect_evidence.py --run-dir C:\ProtheusQA\runs\run-001
```

Códigos: `0` para comando concluído conforme seu estágio; `1` para execução FAIL/ERROR; `2` para bloqueio ou contrato inválido. Código zero em geração/validação NÃO significa PASS no ERP.

A execução PASS exige um caso executado, todas as verificações previstas, identidade confirmada, sem falhas/erros/skips, screenshot não vazio e encerramento da sessão. O resultado identifica execução real ou simulada. Uma falha permanece no run original; use novo diretório/run para uma repetição posteriormente autorizada.

`result.json`, `case.json`, `profile.json`, logs e screenshots ficam restritos localmente. `evidence-manifest.json` registra integridade por SHA-256, não autenticidade criptográfica. A coleta posterior confere os hashes e rejeita alteração, arquivos extras ou symlinks. Console tem mascaramento literal de credenciais; imagens e logs nativos devem ser revisados/sanitizados antes de qualquer compartilhamento.

## 7. Liberação e limites

O próximo marco é um piloto real de leitura, com controle negativo que prove que o teste detecta a falha esperada. Gravações, cleanup de dados, ExecAuto/FwModel/PROBAT executáveis e expansão dos fluxos não estão implementados no runner desta pré-release. Essas técnicas continuam disponíveis como planejamento/roteiro na skill existente.

Não houve avaliação comparativa por modelo nem revisão humana externa. Não há garantia de ausência de defeitos, certificação TOTVS, instalação na sua máquina ou acesso já realizado ao seu ERP.
