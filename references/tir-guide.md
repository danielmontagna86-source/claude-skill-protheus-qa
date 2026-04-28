# Guia TIR

## Uso correto

Use TIR quando o objetivo for validar interface WebApp/APW:

- abertura de rotina;
- botões;
- campos;
- abas/pastas;
- grids;
- browse;
- mensagens;
- fluxo visual de usuário;
- evidências com print/log.

## Quando não usar

- Regra pura/cálculo.
- Validação que pode ser feita por ExecAuto/FwModel.
- Teste de tabela sem necessidade visual.
- Fluxo instável sem massa controlada.

## Padrão de teste TIR

1. Configurar `config.json`.
2. Abrir módulo/rotina.
3. Preencher campos.
4. Executar operação.
5. Validar mensagem ou resultado visual.
6. Salvar log e screenshot quando aplicável.
7. Validar tabela como evidência complementar, quando necessário.

## Configuração mínima

```json
{
  "Url": "http://localhost:8080",
  "Browser": "Firefox",
  "Environment": "ENVIRONMENT",
  "Language": "pt-br",
  "User": "admin",
  "Password": "",
  "TimeOut": 90,
  "Headless": true,
  "ScreenshotFolder": "./log",
  "LogFolder": "./log"
}
```

## Evidências

- log do TIR;
- screenshot;
- mensagem apresentada;
- registro visível no browse;
- validação complementar em tabela.

## Cuidados

- TIR é mais frágil que teste de regra ou ExecAuto.
- Usar apenas quando o comportamento visual fizer parte do risco.
- Controlar massa para evitar falso negativo.
- Garantir que falhas retornem erro real para o executor.
