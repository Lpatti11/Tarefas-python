"""Lê despesas de um CSV e apresenta totais por categoria."""

import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


def ler_gastos(caminho):
    gastos = []
    # utf-8-sig também aceita arquivos UTF-8 com a marca BOM.
    with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        campos = ["data", "descricao", "categoria", "valor"]
        if leitor.fieldnames != campos:
            raise ValueError("O cabeçalho deve ser: data;descricao;categoria;valor")

        for linha in leitor:
            numero = leitor.line_num
            if None in linha or any(valor is None for valor in linha.values()):
                raise ValueError(f"Linha {numero}: quantidade de campos inválida.")
            try:
                data = date.fromisoformat(linha["data"].strip())
                valor = Decimal(linha["valor"].strip().replace(",", "."))
            except (ValueError, InvalidOperation) as erro:
                raise ValueError(f"Linha {numero}: data ou valor inválido.") from erro

            if (
                not valor.is_finite()
                or valor <= 0
                or valor > Decimal("999999999.99")
            ):
                raise ValueError(f"Linha {numero}: use valor entre 0,01 e 999999999,99.")
            if valor != valor.quantize(Decimal("0.01")):
                raise ValueError(f"Linha {numero}: use no máximo duas casas decimais.")

            descricao = linha["descricao"].strip()
            categoria = linha["categoria"].strip().casefold()
            if not descricao or not categoria:
                raise ValueError(f"Linha {numero}: descrição e categoria são obrigatórias.")
            gastos.append({
                "data": data, "descricao": descricao,
                "categoria": categoria, "valor": valor,
            })
    return gastos


def resumir(gastos, mes=None):
    categorias = {}
    quantidade = 0
    for gasto in gastos:
        if mes and gasto["data"].strftime("%Y-%m") != mes:
            continue
        categoria = gasto["categoria"]
        # Decimal evita os erros de representação de valores como 0.1 em float.
        categorias[categoria] = categorias.get(categoria, Decimal("0")) + gasto["valor"]
        quantidade += 1
    total = sum(categorias.values(), Decimal("0"))
    return quantidade, total, categorias


def moeda(valor):
    return f"R$ {valor:.2f}".replace(".", ",")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("arquivo", type=Path, help="CSV separado por ponto e vírgula.")
    parser.add_argument("--mes", help="Filtra um mês no formato AAAA-MM.")
    args = parser.parse_args()

    try:
        if args.mes:
            data = date.fromisoformat(args.mes + "-01")
            if data.isoformat()[:7] != args.mes:
                raise ValueError("Use --mes no formato AAAA-MM.")
        gastos = ler_gastos(args.arquivo)
        quantidade, total, categorias = resumir(gastos, args.mes)
        print(f"Despesas: {quantidade}")
        print(f"Total: {moeda(total)}")
        if not quantidade:
            print("Nenhuma despesa no período selecionado.")
        for categoria, valor in sorted(categorias.items(), key=lambda item: (-item[1], item[0])):
            print(f"  {categoria}: {moeda(valor)}")
    except (OSError, ValueError, csv.Error) as erro:
        parser.exit(1, f"Erro: {erro}\n")


if __name__ == "__main__":
    main()
