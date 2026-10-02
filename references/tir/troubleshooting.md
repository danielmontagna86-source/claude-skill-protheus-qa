# Diagnóstico sem mascarar falhas

| Bloqueio/erro | Ação apropriada |
|---|---|
| `placeholder_profile`, `placeholder_case`, `placeholder_url` | Completar modelo com fonte real; não substituir por IDs públicos arbitrários |
| `runtime_not_ready` | Conferir Python 3.12, pacote exato e perfil; não usar `--force` inexistente |
| `bundle_tampered`, `manifest_tampered` | Refazer geração/revisão/autorização em novo diretório |
| `unapproved_engine` | Revisar atualização da skill e aprovar o novo hash |
| `approval_expired_or_too_long` | Obter nova autorização do operador; agente não prorroga |
| `identity_check_failed` | Não abrir rotina; revisar marcadores/destino/empresa/filial |
| `writes_not_released`, `read_only_navigation_only` | Entregar roteiro; não contornar a restrição de consulta |
| `observed_type_mismatch`, `observed_value_mismatch` | Investigar dado, regra, máscara, seletor e versão; não ajustar esperado sem aprovação |
| Screenshot ausente ou erro no encerramento | Classificar como execução incompleta; coletar diagnóstico local e revisar recursos |
| Timeout | Verificar processo e estado do ambiente antes de novo run autorizado |

Não aumentar timeout indefinidamente, espalhar sleeps ou repetir Salvar. As esperas do framework também exigem uma verificação funcional posterior. Diferencie defeito funcional, erro de massa, interface, versão, credenciais e infraestrutura.

Referência primária sobre sincronização: https://www.selenium.dev/documentation/webdriver/waits/
