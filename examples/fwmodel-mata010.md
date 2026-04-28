# Exemplo FwModel - MATA010

## Cenario

Validar inclusao tecnica de produto por modelo MVC, sem depender da tela.

## Quando usar

Use FwModel quando a rotina for MVC/modelo e o objetivo for validar dados, regras do modelo e persistencia.

## Massa minima

- Codigo de produto exclusivo para teste.
- Tipo de produto valido.
- Unidade de medida valida.
- Armazem padrao valido.
- Empresa e filial controladas.

## Exemplo conceitual

```advpl
#include "protheus.ch"

User Function TstM010Model()
    Local oModel := Nil
    Local lOk    := .T.

    // Confirmar modelo e estrutura no ambiente antes de usar.
    oModel := FwLoadModel("MATA010")
    oModel:SetOperation(MODEL_OPERATION_INSERT)
    oModel:Activate()

    oModel:SetValue("SB1MASTER", "B1_COD"   , "TST0001")
    oModel:SetValue("SB1MASTER", "B1_DESC"  , "PRODUTO TESTE QA")
    oModel:SetValue("SB1MASTER", "B1_TIPO"  , "PA")
    oModel:SetValue("SB1MASTER", "B1_UM"    , "UN")
    oModel:SetValue("SB1MASTER", "B1_LOCPAD", "01")

    If !oModel:VldData()
        lOk := .F.
    Else
        lOk := oModel:CommitData()
    EndIf

    oModel:DeActivate()

    // Evidencia esperada: SB1 contem ou nao contem o produto conforme cenario.
Return lOk
```

## Evidencias

- Retorno de validacao do modelo.
- Registro criado em SB1.
- Mensagens/erros do modelo quando massa for invalida.
- Consulta posterior em SB1/SB5/SB2 quando aplicavel.

## Limites

Confirmar nome do modelo, id das subestruturas e campos obrigatorios no ambiente antes de executar.
