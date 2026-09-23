from decimal import Decimal
from pathlib import Path
import tempfile
import unittest

from gastos import ler_gastos, resumir


class TestGastos(unittest.TestCase):
    def ler_texto(self, conteudo):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "gastos.csv"
            caminho.write_text(conteudo, encoding="utf-8")
            return ler_gastos(caminho)

    def test_soma_exata_e_categorias_normalizadas(self):
        gastos = self.ler_texto(
            "data;descricao;categoria;valor\n"
            "2026-09-01;A; Mercado ;0,10\n"
            "2026-09-02;B;mercado;0.20\n"
        )
        quantidade, total, categorias = resumir(gastos)
        self.assertEqual(quantidade, 2)
        self.assertEqual(total, Decimal("0.30"))
        self.assertEqual(categorias, {"mercado": Decimal("0.30")})

    def test_filtro_mensal(self):
        gastos = ler_gastos(Path(__file__).with_name("exemplo.csv"))
        quantidade, total, _ = resumir(gastos, "2026-09")
        self.assertEqual(quantidade, 7)
        self.assertEqual(total, Decimal("363.30"))
        self.assertEqual(resumir(gastos, "2025-01"), (0, Decimal("0"), {}))

    def test_linhas_invalidas(self):
        linhas = [
            "2026-02-30;Almoço;comida;10",
            "2026-09-01;Almoço;comida;NaN",
            "2026-09-01;Almoço;comida;Infinity",
            "2026-09-01;Almoço;comida;-10",
            "2026-09-01;Almoço;comida;1,234",
            "2026-09-01;Almoço;;10",
            "2026-09-01;Almoço;comida",
            "2026-09-01;Almoço;comida;10;extra",
        ]
        for linha in linhas:
            with self.subTest(linha=linha), self.assertRaisesRegex(ValueError, "Linha 2"):
                self.ler_texto("data;descricao;categoria;valor\n" + linha + "\n")

    def test_cabecalho_invalido(self):
        with self.assertRaises(ValueError):
            self.ler_texto("data,descricao,categoria,valor\n")


if __name__ == "__main__":
    unittest.main()
