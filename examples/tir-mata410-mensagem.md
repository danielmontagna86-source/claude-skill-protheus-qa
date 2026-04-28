# Exemplo TIR - MATA410 Mensagem Visual

## Cenario

Validar mensagem visual na inclusao de pedido de venda com preco abaixo do minimo permitido.

## Quando usar

Use TIR quando o risco envolve interface WebApp/APW, mensagem, botao, browse, grid ou experiencia visual do usuario.

Para regra de preco minimo isolada, prefira PROBAT. Para fluxo funcional tecnico sem tela, prefira ExecAuto/FwModel quando confirmado no ambiente.

## Configuracao conceitual

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

## Teste Python conceitual

```python
import unittest
from tir import Webapp


class TestMATA410PrecoMinimo(unittest.TestCase):
    """Valida mensagem visual de preco minimo no Pedido de Venda."""

    @classmethod
    def setUpClass(cls):
        cls.oHelper = Webapp()
        cls.oHelper.Setup("SIGAFAT", "MATA410")
        cls.oHelper.Program("MATA410")

    def test_deve_exibir_mensagem_preco_abaixo_minimo(self):
        self.oHelper.SetButton("Incluir")

        # Ajustar nomes de campos e massas conforme ambiente.
        # self.oHelper.SetValue("Cliente", "000001")
        # self.oHelper.SetValue("Loja", "01")
        # self.oHelper.SetValue("Produto", "PROD001")
        # self.oHelper.SetValue("Quantidade", "1")
        # self.oHelper.SetValue("Preco", "1.00")
        # self.oHelper.SetButton("Salvar")
        # self.oHelper.CheckResult("Preco abaixo do minimo")

        self.oHelper.AssertTrue()

    @classmethod
    def tearDownClass(cls):
        cls.oHelper.TearDown()


if __name__ == "__main__":
    unittest.main()
```

## Evidencias

- Log do TIR.
- Screenshot da mensagem.
- Mensagem esperada exibida ao usuario.
- Validacao complementar em SC5/SC6 para confirmar que pedido nao foi gravado, quando aplicavel.

## Limites

Confirmar modulo, rotina, labels dos campos, texto exato da mensagem e massa no ambiente antes de executar. Este exemplo nao substitui teste funcional tecnico com ExecAuto/FwModel.
