"""Preocupações misturadas: ler arquivo, interpretar, calcular e imprimir na mesma função.

Para exercitar só o cálculo é preciso criar um arquivo em disco e capturar a saída
padrão; mudar o formato do relatório obriga a mexer no código que lê o CSV.
"""

import csv
from decimal import Decimal


def relatorio(caminho: str) -> None:
    totais: dict[str, Decimal] = {}
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        for linha in csv.DictReader(arquivo):
            subtotal = Decimal(linha["preco"]) * int(linha["quantidade"])
            totais[linha["produto"]] = totais.get(linha["produto"], Decimal(0)) + subtotal
    for produto, total in sorted(totais.items()):
        print(f"{produto:<8} R$ {total:>7.2f}")
