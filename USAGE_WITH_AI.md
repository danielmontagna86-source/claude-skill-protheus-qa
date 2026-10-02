# Uso com IA — do primeiro prompt às evidências

[Início](README.md) · [Instalação](INSTALL.md) · [Instalação com IA](INSTALL_WITH_AI.md) · [Operação TIR](TIR_QUICKSTART.md)

## 1. Primeiro uso

Abra a IA no projeto onde instalou a skill. Os blocos `text` desta página são **prompts para a conversa**, não comandos de terminal. O uso para planejamento não exige instalar TIR nem fornecer senha de ERP.

```text
Use testing-protheus-routines para esta demanda de QA Protheus.
Leia o SKILL.md instalado e informe caminho/versão. Consulte referências
 e fichas pertinentes, não todos os arquivos indiscriminadamente.
Preserve os 13 itens canônicos. Não execute nada no ERP.
Demanda: elaborar o plano de teste da customização descrita abaixo.
```

Acrescente o contexto real no mesmo pedido. No Claude Code, use `/testing-protheus-routines` quando esse comando aparecer no seletor; se aparecer como plugin, use o comando com namespace exibido. No Codex, selecione a skill disponível no cliente ou solicite pelo nome. Não presuma que colar o nome instala a skill. Os caminhos e a descoberta estão documentados em [INSTALL.md](INSTALL.md).

## 2. Contexto mínimo para a IA

Copie este formulário e substitua somente o que conhece. A ausência de dados deve permanecer explícita, não preenchida com exemplos públicos.

```text
Rotina/módulo: [informar]
Regra funcional e comportamento esperado: [informar]
Customização/ponto de entrada/modelo: [confirmado ou não confirmado]
Fontes autorizados para leitura: [caminhos/arquivos]
Documentação e versão consultada: [informar]
Release/build/LIB/RPO/interface: [informar ou não confirmado]
Empresa/filial/data-base: [somente contexto não sensível autorizado]
Massa sintética disponível: [informar]
Risco prioritário e impacto: [informar]
Objetivo desta solicitação: somente análise / cenários / geração offline
Responsável que validará o esperado: [informar]
```

Não envie credenciais, dados pessoais de clientes ou extratos reais. Compartilhamento de fontes privados com a IA depende da política da empresa. A ficha local de uma rotina não certifica o dicionário, parâmetros ou customização da sua instalação.

## 3. Prompts de trabalho

### A. Analisar uma customização ADVPL/TLPP

```text
Use testing-protheus-routines. Analise apenas os fontes que autorizei.
Não regrave arquivos, não converta encoding e não compile.
Separe comportamento confirmado, hipótese e informação faltante.
Escolha PROBAT para regra isolável confirmada, ExecAuto/FwModel quando
houver contrato documentado e TIR apenas para o risco de interface.
Crie os cenários positivos, negativos e de regressão, a massa mínima,
o esperado independente da implementação e a evidência necessária.
Entregue os 13 itens e bloqueie automação quando faltar informação crítica.
```

### B. Planejar regressão de uma alteração

```text
Use testing-protheus-routines para revisar o diff fornecido.
Não modifique código. Relacione cada alteração ao risco funcional,
aos fluxos relacionados e aos testes existentes. Não invente tabelas,
campos ou pontos de entrada. Priorize por impacto com justificativa.
Nos 13 itens, deixe explícitos cenários cobertos, lacunas e controles
negativos que demonstrarão que o teste detecta uma falha real.
Não execute rotinas nem conclua aprovação apenas porque houve compilação.
```

### C. Preparar um caso TIR, sem executar

```text
Use testing-protheus-routines e leia TIR_QUICKSTART.md,
SECURITY.md e references/tir/public-api-manifest.json.
Prepare um caso somente de consulta para a rotina e massa confirmadas.
Use os modelos de templates/tir/; não copie os cadastros das fixtures de testes.
Não habilite perfil nem modifique política de aprovação. Campos desconhecidos
continuam como lacunas. Gere rascunhos fora da pasta da skill.
Com dados suficientes, use validate_case.py e generate_tir_tests.py com
os argumentos documentados. Não execute run_tir_suite.py nesta solicitação.
Se o validador retornar BLOCKED, preserve o bloqueio e explique a causa.
Registre fontes, resultado esperado, hash e os 13 itens. Código gerado
é artefato de revisão; não deve ser executado diretamente.
```

A geração exige perfil/caso válidos. Os modelos públicos foram feitos para bloquear enquanto incompletos; a IA não deve falsificar dados ou habilitar o ambiente para conseguir produzir um bundle. A configuração preenchida/habilitada exige decisão do operador; alterar depois da geração exige novo bundle e nova autorização.

### D. Interpretar falha e evidências

```text
Use testing-protheus-routines para analisar o resultado e os logs sanitizados
que disponibilizei. Não altere result.json, manifesto, caso ou esperado.
Diferencie falha funcional, falha de teste, massa, seletor, sincronização,
ambiente e credencial. Use apenas evidências existentes e cite os arquivos.
Não aceite screenshot ausente, zero testes ou skipped como PASS.
Apresente diagnóstico, evidências e limitações nos 13 itens.
Não faça retry, não repita Salvar e não corrija o ERP automaticamente.
```

### E. Consolidar QA para gestão

```text
Use testing-protheus-routines para consolidar as execuções fornecidas.
Dentro dos 13 itens, destaque riscos cobertos, casos obrigatórios bloqueados,
falhas funcionais versus falhas de automação e evidências faltantes.
Separe resultado offline, simulação e execução real. Não conte repetições
como novos cenários. Não altere os resultados de origem nem avalie pessoas
por quantidade de testes ou linhas de código produzidas.
```

## 4. Exemplo de aplicação ao trabalho

Demanda ilustrativa: uma customização de pedido de venda deve rejeitar um preço abaixo do mínimo definido pelo negócio. A IA deve confirmar o ponto de entrada/modelo e as fontes antes de recomendar implementação; os nomes dos campos e mensagens não são presumidos.

O plano deve distinguir a regra de comparação do preço da mensagem apresentada na tela. O resultado esperado deve vir de uma regra aprovada, não da cópia do cálculo que está sendo testado. Um cenário de rejeição correta é um teste aprovado; não implica chamar `AssertFalse()` por ser “negativo”.

A skill pode planejar esse teste. O executor desta pré-release é mais restrito: **somente consulta**, sem preenchimento, gravação, transmissão, SQL ou execução de código arbitrário. Um roteiro planejado não amplia automaticamente o que o runner permite.

## 5. Contrato esperado em toda resposta QA

1. Objetivo do teste
2. Base funcional/TDN usada
3. Tipo de customização
4. Risco QA
5. Técnica recomendada
6. Cenários positivos
7. Cenários negativos
8. Cenários de regressão
9. Massa de dados
10. Tabelas/campos
11. Exemplo de automação ou roteiro
12. Evidência esperada
13. Limitações

Dados ausentes: `Não confirmado no contexto fornecido`, com a dependência. Itens não aplicáveis: justificar. Critérios adicionais e exemplos por módulo estão em [USAGE.md](USAGE.md), [routines/INDEX.md](routines/INDEX.md) e [evals/tir-behavioral.md](evals/tir-behavioral.md). Existir um arquivo de eval não significa que a avaliação comportamental foi executada.

## 6. Quando chegar à execução real

Siga [TIR_QUICKSTART.md](TIR_QUICKSTART.md) com o responsável pelo ambiente. Runtime e revisão de dependências, isolamento, navegador/driver, massa, esperado e autorização precisam estar aprovados antes de iniciar. A política fica fora do controle do agente; a IA não pode assinar/autoaprovar o próprio teste.

Prepare o primeiro piloto com uma consulta conhecida e um controle negativo. Um sucesso de validação estática ou de geração é apenas sucesso daquele estágio, não PASS no Protheus. O preflight não testa rede, autenticação ou driver. Credenciais só entram no terminal autorizado, nunca no prompt.

O piloto, a versão do cliente IA e os riscos de dependência permanecem sujeitos à validação local. A instalação dos guias não altera `erp_validated` nem aprova execução em produção.
