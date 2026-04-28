# Matriz de Decisão QA Protheus

## Decisão por tipo de validação

| Situação | Técnica principal | Técnica auxiliar | Evidência |
|---|---|---|---|
| Regra pura/cálculo | PROBAT | Checklist | Assert |
| Classe TLPP | PROBAT | Review | Assert + log |
| Fonte ADVPL testável | PROBAT em TLPP | Refatoração leve | Assert |
| Rotina automática | ExecAuto | Consulta tabela | Retorno + tabela |
| Rotina MVC | FwModel | TIR | Modelo + tabela |
| Tela WebApp/APW | TIR | Checklist | Print/log/mensagem |
| Ponto de entrada | Rotina + validação efeito | TIR/ExecAuto | Tabela/log/mensagem |
| Ponto de entrada MVC | Evento + PARAMIXB + retorno | FwModel/TIR | Modelo/tabela |
| SX3 validação | Teste funcional | Checklist | Bloqueio/mensagem |
| SX7 gatilho | Teste funcional | Consulta tabela | Campo alterado/tabela |
| SXB fórmula | Entrada/saída | Regressão | Resultado calculado |
| Financeiro | ExecAuto + tabela | TIR | SE1/SE2/SE5 |
| Faturamento | ExecAuto/FwModel/TIR | PROBAT | SC5/SC6/SD2/SE1 |
| Compras | ExecAuto + tabela | TIR | SC1/SC7/SD1/SE2 |
| Estoque | TIR/ExecAuto + tabela | PROBAT | SB1/SB2/SD3 |

## Regras de escolha

1. Se a regra é isolável, priorize PROBAT.
2. Se a rotina tem ExecAuto documentado, priorize ExecAuto para teste funcional técnico.
3. Se a rotina é MVC e o objetivo é modelo/dados, use FwModel quando possível.
4. Se o objetivo é tela, botão, browse, mensagem ou fluxo visual, use TIR.
5. Se não há massa confiável ou a automação é destrutiva, gere checklist guiado.

## Antipadrões

- Usar TIR para validar regra pura.
- Usar PROBAT para validar tela.
- Usar ExecAuto para validar mensagem visual.
- Ignorar filial, empresa, parâmetros MV_* ou massa reversível.
- Assumir ponto de entrada sem fonte.
