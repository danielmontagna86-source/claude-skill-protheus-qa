# Template canonico de saida

Fonte oficial: `SKILL.md` > `Contrato obrigatorio de saida`.

Toda resposta de QA da skill `testing-protheus-routines` deve usar exatamente os 13 itens abaixo, nesta ordem e com estes nomes.

1. Objetivo do teste
   - Informar o que sera validado, rotina/processo e resultado esperado.

2. Base funcional/TDN usada
   - Informar a referencia funcional usada.
   - Se nao houver fonte, usar: `Nao confirmado no contexto fornecido`.

3. Tipo de customizacao
   - Classificar como ponto de entrada, MVC, SX3, SX7, SXB, regra ADVPL/TLPP, ExecAuto, FwModel, TIR/WebApp ou hipotese.

4. Risco QA
   - Explicar risco funcional, tecnico ou regressivo.

5. Tecnica recomendada
   - Indicar PROBAT, ExecAuto, FwModel, TIR/WebApp ou checklist.
   - Justificar a escolha.

6. Cenarios positivos
   - Listar fluxos esperados com sucesso.

7. Cenarios negativos
   - Listar erros, bloqueios, mensagens e excecoes esperadas.

8. Cenarios de regressao
   - Listar fluxos relacionados que nao podem quebrar.

9. Massa de dados
   - Informar dados minimos, cadastros, parametros e pre-condicoes.

10. Tabelas/campos
   - Informar tabelas/campos conhecidos.
   - Marcar hipoteses como nao confirmadas.

11. Exemplo de automacao ou roteiro
   - Informar exemplo PROBAT, ExecAuto, FwModel, TIR/WebApp ou checklist manual.

12. Evidencia esperada
   - Informar evidencia verificavel em tela, tabela, log, retorno, mensagem ou relatorio.

13. Limitacoes
   - Informar lacunas, premissas, dependencias do ambiente e pontos que exigem confirmacao.

## Regras

- Nao remover itens.
- Nao renomear itens.
- Nao juntar itens.
- Nao reordenar itens.
- Preencher todos os itens.
- Usar `Nao confirmado no contexto fornecido` quando faltar fonte.
- Usar `Nao aplicavel` quando uma tecnica ou evidencia nao se aplicar.
- Manter foco em QA Protheus com TDN, ADVPL/TLPP, PROBAT, ExecAuto/FwModel e TIR/WebApp.
