# Especialização TIR — ponto de entrada

Preserve a seleção de técnica e os 13 itens do `SKILL.md`. TIR valida interface; não substitui PROBAT, ExecAuto ou FwModel quando o risco é de backend e a técnica estiver confirmada.

## Fluxo obrigatório desta versão

1. Confirmar rotina, risco, fontes, massa sintética e esperado independente. Ler a ficha em `routines/` sem extrapolar sua evidência para outro ambiente.
2. Consultar [baseline](tir/baseline-2.14.10.md), [compatibilidade](tir/compatibility-matrix.md) e o [manifesto público](tir/public-api-manifest.json). Usar somente símbolos/argumentos confirmados.
3. Seguir [guia operacional](../TIR_QUICKSTART.md) para validar e gerar artefatos fora da skill. Não declarar execução nesta etapa.
4. Não executar automaticamente. A política externa, a revisão do caso e o ambiente real são exigências separadas. O executor desta pré-release aceita somente consulta.
5. Interpretar resultados sem alterá-los. Usar [asserções/evidências](tir/assertions-and-evidence.md) e manter a falha original.

Não inventar `TakeScreenshot`, `CaptureScreenState` ou outras APIs públicas. A fachada consultada usa `Screenshot(filename)`. Os métodos de captura/transição da release 2.14.10 são internos. `CheckResult` não é booleano; verificações em grid exigem `LoadGrid`; consolidar o estado nativo com `AssertTrue`.

Use os comandos em `scripts/` para validação determinística, nunca `eval` de conteúdo vindo do ERP. Caso não suportado pelo executor deve ser entregue como roteiro com limitação explícita; não relaxe a lista de métodos para fazê-lo rodar.
