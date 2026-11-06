"""Cada preocupação em sua função: interpretar, calcular e formatar.

Só a casca (``gerar_relatorio``) junta as três. Cada parte é testável sozinha,
com texto em memória, sem disco e sem ``print``.
"""

import csv
import io
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Venda:
    produto: str
    quantidade: int
    preco: Decimal


def ler_vendas(texto_csv: str) -> list[Venda]:
    leitor = csv.DictReader(io.StringIO(texto_csv))
    return [
        Venda(linha["produto"], int(linha["quantidade"]), Decimal(linha["preco"]))
        for linha in leitor
    ]


def totais_por_produto(vendas: list[Venda]) -> dict[str, Decimal]:
    totais: dict[str, Decimal] = {}
    for venda in vendas:
        totais[venda.produto] = (
            totais.get(venda.produto, Decimal(0)) + venda.preco * venda.quantidade
        )
    return totais


def formatar_relatorio(totais: dict[str, Decimal]) -> str:
    return "\n".join(f"{produto:<8} R$ {total:>7.2f}" for produto, total in sorted(totais.items()))


def gerar_relatorio(texto_csv: str) -> str:
    return formatar_relatorio(totais_por_produto(ler_vendas(texto_csv)))
