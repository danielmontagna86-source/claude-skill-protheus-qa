# Exemplo PROBAT - Regra Isolada

## Cenario

Customizacao valida se um titulo a pagar pode ser gravado sem natureza financeira.

## Objetivo

Demonstrar quando usar PROBAT: regra isolada, sem tela e sem depender diretamente da rotina.

## Regra alvo conceitual

```advpl
User Function ValNatFin(cNatureza)
    Local lValido := !Empty(cNatureza)
Return lValido
```

## Teste TLPP com PROBAT

```tlpp
#include "tlpp-core.th"
#include "tlpp-probat.th"

namespace custom.tests.financeiro

using namespace tlpp.probat

@TestFixture(owner='qa-protheus', target='VALNATFIN.PRW')
class TestValidaNaturezaFinanceira

    @Test('deve permitir natureza preenchida')
    public method devePermitirNaturezaPreenchida()

    @Test('deve bloquear natureza vazia')
    public method deveBloquearNaturezaVazia()

endclass

public method devePermitirNaturezaPreenchida() class TestValidaNaturezaFinanceira
    local lRet := U_ValNatFin('001')
    assertTrue(lRet, 'Natureza preenchida deve ser aceita')
return .T.

public method deveBloquearNaturezaVazia() class TestValidaNaturezaFinanceira
    local lRet := U_ValNatFin('')
    assertFalse(lRet, 'Natureza vazia deve ser bloqueada')
return .T.
```

## Evidencias

- Resultado da suite PROBAT.
- Assert positivo e negativo.
- Associacao com fonte alvo.

## Limite

Este exemplo nao valida tela nem gravacao em SE2. Para fluxo funcional da FINA050, usar ExecAuto ou roteiro funcional complementar.
