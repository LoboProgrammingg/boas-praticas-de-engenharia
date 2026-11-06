"""SRP aplicado: cada módulo tem um único motivo para mudar.

* ``Fatura``: regra de negócio (muda quando o cálculo muda).
* ``RepositorioDeFaturas``: persistência (muda quando o banco muda).
* ``formatar_email``: apresentação (muda quando o texto muda).
"""

import sqlite3
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True, slots=True)
class Item:
    descricao: str
    preco: Decimal
    quantidade: int


@dataclass(frozen=True, slots=True)
class Fatura:
    cliente: str
    itens: tuple[Item, ...]

    def total(self) -> Decimal:
        return sum((item.preco * item.quantidade for item in self.itens), Decimal("0"))


class RepositorioDeFaturas(Protocol):
    def salvar(self, fatura: Fatura) -> None: ...


class RepositorioSqlite:
    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

    def salvar(self, fatura: Fatura) -> None:
        self._conexao.execute(
            "INSERT INTO faturas (cliente, total) VALUES (?, ?)",
            (fatura.cliente, str(fatura.total())),
        )


def formatar_email(fatura: Fatura) -> str:
    return f"Olá, {fatura.cliente}! Sua fatura deu R$ {fatura.total():.2f}."
