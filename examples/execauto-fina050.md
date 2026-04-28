# Exemplo ExecAuto - FINA050

## Cenario

Validar inclusao tecnica de titulo a pagar e bloqueio de titulo sem natureza financeira.

## Quando usar

Use ExecAuto quando o objetivo for validar fluxo funcional tecnico da rotina, sem depender da interface.

## Massa minima

- Fornecedor valido em SA2.
- Natureza financeira valida.
- Empresa e filial controladas.
- Numero/prefixo/parcela exclusivos para evitar duplicidade.

## Exemplo conceitual

```advpl
#include "protheus.ch"

User Function TstF050Nat()
    Local aCabec := {}
    Local lOk    := .T.

    Private lMsErroAuto := .F.

    // Ajustar campos conforme TDN/ambiente.
    AAdd(aCabec, {"E2_PREFIXO", "TST", Nil})
    AAdd(aCabec, {"E2_NUM"    , "000001", Nil})
    AAdd(aCabec, {"E2_PARCELA", "01", Nil})
    AAdd(aCabec, {"E2_TIPO"   , "NF", Nil})
    AAdd(aCabec, {"E2_NATUREZ", "001", Nil})
    AAdd(aCabec, {"E2_FORNECE", "000001", Nil})
    AAdd(aCabec, {"E2_LOJA"   , "01", Nil})
    AAdd(aCabec, {"E2_EMISSAO", Date(), Nil})
    AAdd(aCabec, {"E2_VENCTO" , Date()+10, Nil})
    AAdd(aCabec, {"E2_VENCREA", Date()+10, Nil})
    AAdd(aCabec, {"E2_VALOR"  , 100, Nil})

    // Confirmar assinatura da rotina no ambiente antes de usar.
    // MSExecAuto({|x,y| FINA050(x,y)}, aCabec, 3)

    If lMsErroAuto
        lOk := .F.
        // MostraErro()
    EndIf

    // Evidencia esperada: SE2 contem ou nao contem o titulo conforme cenario.
Return lOk
```

## Evidencias

- Retorno sem erro para titulo valido.
- Registro criado em SE2.
- Bloqueio/erro para natureza vazia ou invalida.
- Registro nao criado em SE2 no cenario negativo.

## Limites

Este exemplo e conceitual. Confirmar assinatura, campos obrigatorios e comportamento da rotina no ambiente/TDN antes de executar.
