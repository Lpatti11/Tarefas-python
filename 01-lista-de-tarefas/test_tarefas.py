import json
from pathlib import Path
import tempfile
import unittest

from tarefas import adicionar, carregar, concluir, salvar


class TestTarefas(unittest.TestCase):
    def test_fluxo_com_persistencia(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "tarefas.json"
            tarefas = carregar(caminho)
            adicionar(tarefas, "  Estudar funções  ")
            adicionar(tarefas, "Praticar JSON")
            concluir(tarefas, 1)
            salvar(caminho, tarefas)
            resultado = carregar(caminho)
            self.assertEqual(resultado[0]["titulo"], "Estudar funções")
            self.assertTrue(resultado[0]["concluida"])
            self.assertEqual(resultado[1]["id"], 2)
            self.assertFalse(resultado[1]["concluida"])

    def test_titulo_vazio_e_id_inexistente(self):
        with self.assertRaises(ValueError):
            adicionar([], "   ")
        with self.assertRaises(ValueError):
            concluir([], 99)

    def test_arquivo_invalido_permanece_intacto(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "tarefas.json"
            for conteudo in ("{incompleto", '[{"id": 1}]', '{}'):
                caminho.write_text(conteudo, encoding="utf-8")
                with self.assertRaises(ValueError):
                    carregar(caminho)
                self.assertEqual(caminho.read_text(encoding="utf-8"), conteudo)

    def test_ids_duplicados_sao_rejeitados(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "tarefas.json"
            tarefa = {"id": 1, "titulo": "Ler", "concluida": False}
            caminho.write_text(json.dumps([tarefa, tarefa]), encoding="utf-8")
            with self.assertRaises(ValueError):
                carregar(caminho)


if __name__ == "__main__":
    unittest.main()
