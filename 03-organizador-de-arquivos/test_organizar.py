from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from organizar import mover_sem_sobrescrever, planejar


class TestOrganizador(unittest.TestCase):
    def test_simulacao_nao_modifica_pasta(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "foto.JPG").write_bytes(b"exemplo")
            (raiz / ".oculto").write_text("ignorar", encoding="utf-8")
            (raiz / "subpasta").mkdir()
            (raiz / "subpasta" / "nota.txt").write_text("ficar", encoding="utf-8")
            antes = set(raiz.rglob("*"))
            plano = planejar(raiz)
            self.assertEqual(len(plano), 1)
            self.assertEqual(plano[0][1].parent.name, "imagens")
            self.assertEqual(set(raiz.rglob("*")), antes)

    def test_conflitos_preservam_conteudo(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "documentos").mkdir()
            (raiz / "documentos" / "nota.txt").write_bytes(b"antigo")
            (raiz / "nota.txt").write_bytes(b"novo")
            (raiz / "nota_1.txt").write_bytes(b"terceiro")
            plano = planejar(raiz)
            self.assertEqual(len({destino for _, destino in plano}), 2)
            for origem, destino in plano:
                mover_sem_sobrescrever(origem, destino)
            conteudos = {arquivo.read_bytes() for arquivo in (raiz / "documentos").iterdir()}
            self.assertEqual(conteudos, {b"antigo", b"novo", b"terceiro"})
            self.assertEqual(planejar(raiz), [])

    def test_destino_criado_depois_do_plano_nao_e_sobrescrito(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            origem = raiz / "nota.txt"
            origem.write_bytes(b"original")
            _, destino = planejar(raiz)[0]
            destino.parent.mkdir()
            destino.write_bytes(b"nao substituir")
            with self.assertRaises(FileExistsError):
                mover_sem_sobrescrever(origem, destino)
            self.assertEqual(origem.read_bytes(), b"original")
            self.assertEqual(destino.read_bytes(), b"nao substituir")

    def test_falha_de_copia_preserva_origem(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            origem = raiz / "nota.txt"
            origem.write_bytes(b"original")
            _, destino = planejar(raiz)[0]
            with patch("organizar.shutil.copyfileobj", side_effect=OSError("Falha simulada")):
                with self.assertRaises(OSError):
                    mover_sem_sobrescrever(origem, destino)
            self.assertEqual(origem.read_bytes(), b"original")
            self.assertFalse(destino.exists())

    def test_nome_da_categoria_ocupado_por_arquivo(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "documentos").write_bytes(b"existente")
            (raiz / "nota.txt").write_bytes(b"novo")
            with self.assertRaises(ValueError):
                planejar(raiz)


if __name__ == "__main__":
    unittest.main()
