#include "protheus.ch"

/*
    Template de teste funcional técnico com ExecAuto.

    Ajustar:
    - rotina chamada;
    - arrays de cabeçalho/itens/perguntas;
    - operação;
    - massa;
    - validação em tabela.
*/
User Function TstExecAuto()
    Local aCabec  := {}
    Local aItens  := {}
    Local lOk     := .T.

    Private lMsErroAuto := .F.

    // TODO: preparar empresa/filial/ambiente quando necessário.
    // TODO: preencher aCabec e aItens conforme TDN da rotina.
    // Exemplo conceitual:
    // AAdd(aCabec, {"CAMPO", xValor, Nil})
    // AAdd(aItens,  { {"CAMPO", xValor, Nil} })

    // TODO: trocar <ROTINA> pela rotina automática real.
    // TODO: confirmar assinatura da rotina na TDN ou no ambiente.
    // MSExecAuto({|x,y,z| <ROTINA>(x,y,z)}, aCabec, aItens, 3) // 3 = inclusão quando aplicável

    If lMsErroAuto
        lOk := .F.
        // MostraErro()
    EndIf

    // TODO: validar tabela afetada como evidência.

Return lOk
