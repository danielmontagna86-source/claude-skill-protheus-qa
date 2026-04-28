# Guia PROBAT

## Uso correto

Use PROBAT quando o objetivo for testar:

- função isolada;
- cálculo;
- regra de validação;
- classe TLPP;
- service TLPP;
- regra ADVPL extraída para função testável.

## Regras importantes

- PROBAT executa testes escritos em TLPP.
- Mesmo quando o alvo for ADVPL (`.prw`), o teste deve ser escrito em `.tlpp`.
- PROBAT não valida interface, botão, browse ou mensagem visual.
- Use TIR para interface e ExecAuto/FwModel para fluxo funcional técnico.

## Estrutura mínima

```tlpp
#include "tlpp-core.th"
#include "tlpp-probat.th"

namespace custom.tests.financeiro

using namespace tlpp.probat

@TestFixture(owner='qa-protheus', target='fonte_alvo.prw')
class TestRegraFinanceira

    @Test('deve validar regra com entrada válida')
    public method deveValidarRegraValida()

endclass

public method deveValidarRegraValida() class TestRegraFinanceira
    local lRet := .T.

    assertTrue(lRet, 'Regra válida deve retornar verdadeiro')
return .T.
```

## Quando pedir refatoração

Se a regra estiver acoplada à tela, DB ou rotina monolítica, sugerir extrair uma função testável antes de criar PROBAT.

Exemplo:

```advpl
User Function ValPrecoMin(cProduto, nPrecoVenda)
    // retorna .T. ou .F.
Return lValido
```

Depois testar em TLPP com PROBAT.

## Evidências

- asserts executados;
- resultado da suíte;
- log da execução;
- cobertura, se disponível;
- relação entre teste e fonte alvo.
