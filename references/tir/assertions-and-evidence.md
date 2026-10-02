# Asserções, grids e evidências

`GetValue` retorna o observado. `IfExists` retorna presença/ausência. A fachada `CheckResult` delega sem retorno booleano; nunca escreva `assert helper.CheckResult(...)`. Para grids, `CheckResult(..., grid=True)` é seguido de `LoadGrid()`. O motor ainda verifica `GetValue`, com comparação exata, e chama `AssertTrue()` para concluir o estado de erro do TIR.

Fonte: https://github.com/totvs/tir/blob/dbc12e7a0563174a3f6c16832046229d71d464cf/tir/main.py

O esperado vem da especificação funcional aprovada, não da implementação que está sob teste. Preserve padding, tipo e representação. Cenário negativo corretamente rejeitado pode ser um teste aprovado; não converter automaticamente cenário negativo em `AssertFalse()`.

PASS exige caso executado, identidade válida, todas as verificações, ausência de falha/erro/skip, screenshot não vazio e encerramento da sessão. Zero casos, apenas skips, saída zero sem resultado e evidência ausente não aprovam. Testes simulados não marcam `erp_validated=true`.

O bundle é regenerado canonicamente antes da execução; alterações no JSON ou Python gerado invalidam a revisão. O worker recebe snapshot e motor com hash aprovado. O manifesto de evidências permite detectar alteração posterior, mas não autentica criptograficamente um operador.

Um screenshot de formulário preenchido não prova gravação. Por isso gravação e sua releitura/cleanup continuam fora deste executor até homologação própria. A evidência é restrita e local; o agente não pode trocar expectativas para fazer o resultado passar.
