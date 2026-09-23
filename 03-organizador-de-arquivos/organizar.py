"""Organiza os arquivos de uma pasta por extensão; começa em modo de simulação."""

import argparse
from pathlib import Path
import shutil


EXTENSOES = {
    "imagens": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"},
    "documentos": {".pdf", ".txt", ".docx", ".odt", ".md"},
    "planilhas": {".csv", ".xlsx", ".ods"},
    "codigo": {".py", ".js", ".html", ".css", ".json"},
    "compactados": {".zip", ".rar", ".7z", ".gz"},
}


def categoria(arquivo):
    for nome, extensoes in EXTENSOES.items():
        if arquivo.suffix.lower() in extensoes:
            return nome
    return "outros"


def planejar(pasta):
    """Calcula todos os destinos sem criar pastas ou mover arquivos."""
    pasta = pasta.expanduser().resolve(strict=True)
    if not pasta.is_dir():
        raise ValueError("Informe o caminho de uma pasta.")

    plano = []
    reservados = set()
    for origem in sorted(pasta.iterdir(), key=lambda item: item.name):
        if origem.is_symlink() or origem.name.startswith(".") or not origem.is_file():
            continue
        destino_pasta = pasta / categoria(origem)
        if destino_pasta.is_symlink():
            raise ValueError(f"A pasta de destino não pode ser um link: {destino_pasta}")
        if destino_pasta.exists() and not destino_pasta.is_dir():
            raise ValueError(f"Um arquivo ocupa o nome da pasta de destino: {destino_pasta}")

        destino = destino_pasta / origem.name
        contador = 1
        while destino.exists() or destino.is_symlink() or destino in reservados:
            destino = destino_pasta / f"{origem.stem}_{contador}{origem.suffix}"
            contador += 1
        reservados.add(destino)
        plano.append((origem, destino))
    return plano


def mover_sem_sobrescrever(origem, destino):
    """Copia para um arquivo novo e remove a origem só após concluir a cópia."""
    if origem.is_symlink() or destino.parent.is_symlink():
        raise ValueError("Um dos caminhos foi alterado para um link. Execute novamente.")
    destino.parent.mkdir(exist_ok=True)
    criado = False
    try:
        # O modo xb falha se o destino já existir, inclusive após o planejamento.
        with origem.open("rb") as entrada, destino.open("xb") as saida:
            criado = True
            shutil.copyfileobj(entrada, saida)
    except OSError:
        if criado:
            destino.unlink(missing_ok=True)
        raise
    origem.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pasta", type=Path, help="Pasta cujos arquivos serão organizados.")
    parser.add_argument("--aplicar", action="store_true", help="Executa o plano exibido.")
    args = parser.parse_args()

    try:
        plano = planejar(args.pasta)
        if not plano:
            print("Nenhum arquivo para organizar.")
            return
        print("Aplicação:" if args.aplicar else "Simulação: nenhum arquivo será movido.")
        for origem, destino in plano:
            print(f"  {origem.name} -> {destino.parent.name}/{destino.name}")
        if args.aplicar:
            for origem, destino in plano:
                mover_sem_sobrescrever(origem, destino)
            print(f"Concluído: {len(plano)} arquivo(s) organizado(s).")
        else:
            print("Para executar, repita o comando incluindo --aplicar.")
    except (OSError, ValueError) as erro:
        parser.exit(1, f"Erro: {erro}\n")


if __name__ == "__main__":
    main()
