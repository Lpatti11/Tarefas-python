"""Lista de tarefas no terminal, com dados persistidos em JSON."""

import argparse
import json
import os
from pathlib import Path
import tempfile


def carregar(caminho):
    """Um arquivo inexistente representa uma lista ainda vazia."""
    if not caminho.exists():
        return []

    tarefas = json.loads(caminho.read_text(encoding="utf-8"))
    if not isinstance(tarefas, list):
        raise ValueError("O arquivo de tarefas deve conter uma lista JSON.")

    ids = set()
    for tarefa in tarefas:
        if (
            not isinstance(tarefa, dict)
            # O ID precisa ser inteiro; type(...) is int também rejeita True/False.
            or type(tarefa.get("id")) is not int
            or tarefa["id"] < 1
            or tarefa["id"] in ids
            or not isinstance(tarefa.get("titulo"), str)
            or not tarefa["titulo"].strip()
            or type(tarefa.get("concluida")) is not bool
        ):
            raise ValueError("O arquivo contém uma tarefa inválida.")
        ids.add(tarefa["id"])
    return tarefas


def salvar(caminho, tarefas):
    """Escreve primeiro em um temporário para evitar um JSON incompleto."""
    temporario = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=caminho.parent,
            suffix=".tmp", delete=False,
        ) as arquivo:
            temporario = Path(arquivo.name)
            json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)
            arquivo.write("\n")
        os.replace(temporario, caminho)
    finally:
        if temporario is not None:
            # missing_ok=True aceita que ele já não exista após os.replace().
            temporario.unlink(missing_ok=True)


def adicionar(tarefas, titulo):
    titulo = titulo.strip()
    if not titulo:
        raise ValueError("Escreva um título para a tarefa.")

    # Se não houver tarefas, default=0 faz o primeiro ID ser 1.
    novo_id = max((tarefa["id"] for tarefa in tarefas), default=0) + 1
    tarefa = {"id": novo_id, "titulo": titulo, "concluida": False}
    tarefas.append(tarefa)
    return tarefa


def concluir(tarefas, tarefa_id):
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            tarefa["concluida"] = True
            return tarefa
    raise ValueError(f"Não existe tarefa com o ID {tarefa_id}.")


def filtrar(tarefas, status="todas"):
    """Seleciona tarefas por situação sem alterar a lista original."""
    if status == "todas":
        return tarefas.copy()
    if status not in ("pendentes", "concluidas"):
        raise ValueError("Use o filtro: todas, pendentes ou concluidas.")

    concluida = status == "concluidas"
    filtradas = []
    for tarefa in tarefas:
        if tarefa["concluida"] == concluida:
            filtradas.append(tarefa)
    return filtradas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--arquivo", type=Path,
        default=Path(__file__).with_name("tarefas.json"),
        help="Caminho do JSON (padrão: tarefas.json ao lado do programa).",
    )
    comandos = parser.add_subparsers(dest="comando", required=True)
    novo = comandos.add_parser("adicionar", help="Cria uma tarefa.")
    novo.add_argument("titulo")
    listar = comandos.add_parser("listar", help="Exibe tarefas com filtro opcional.")
    listar.add_argument(
        "--status", choices=("todas", "pendentes", "concluidas"), default="todas",
        help="Filtra pela situação da tarefa (padrão: todas).",
    )
    pronto = comandos.add_parser("concluir", help="Marca uma tarefa como concluída.")
    pronto.add_argument("id", type=int)
    args = parser.parse_args()

    try:
        tarefas = carregar(args.arquivo)
        if args.comando == "adicionar":
            tarefa = adicionar(tarefas, args.titulo)
            salvar(args.arquivo, tarefas)
            print(f"Tarefa {tarefa['id']} adicionada: {tarefa['titulo']}")
        elif args.comando == "concluir":
            tarefa = concluir(tarefas, args.id)
            salvar(args.arquivo, tarefas)
            print(f"Tarefa {tarefa['id']} concluída: {tarefa['titulo']}")
        else:
            filtradas = filtrar(tarefas, args.status)
            if not filtradas:
                if args.status == "todas":
                    print("Nenhuma tarefa cadastrada.")
                else:
                    print("Nenhuma tarefa encontrada para esse filtro.")
            for tarefa in filtradas:
                marca = "x" if tarefa["concluida"] else " "
                print(f"[{marca}] {tarefa['id']}: {tarefa['titulo']}")
    except (OSError, ValueError) as erro:
        parser.exit(1, f"Erro: {erro}\n")




if __name__ == "__main__":
    main()
