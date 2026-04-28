import unittest
from tir import Webapp


class TestRotinaProtheus(unittest.TestCase):
    """Template de teste visual com TIR para Protheus WebApp/APW."""

    @classmethod
    def setUpClass(cls):
        cls.oHelper = Webapp()
        cls.oHelper.Setup("<MODULO>", "<ROTINA>")
        cls.oHelper.Program("<ROTINA>")

    def test_fluxo_visual(self):
        # TODO: ajustar botões, campos e mensagens conforme rotina.
        self.oHelper.SetButton("Incluir")

        # Exemplos conceituais:
        # self.oHelper.SetValue("<CAMPO>", "<VALOR>")
        # self.oHelper.SetButton("Confirmar")
        # self.oHelper.CheckResult("<MENSAGEM_ESPERADA>")

        self.oHelper.AssertTrue()

    @classmethod
    def tearDownClass(cls):
        cls.oHelper.TearDown()


if __name__ == "__main__":
    unittest.main()
