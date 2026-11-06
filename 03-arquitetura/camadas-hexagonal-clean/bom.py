"""Dependency Rule aplicada: a regra de negócio só conhece portas que ela mesma define.

Círculos, de dentro para fora:

* domínio: ``Pedido`` (regra e invariantes);
* aplicação: ``FazerPedido`` (caso de uso) e as portas ``RepositorioDePedidos`` e ``Notificador``;
* infraestrutura: ``RepositorioSqlite`` e ``RepositorioEmMemoria`` (adaptadores).

Nenhuma classe de dentro menciona ``sqlite3``: as dependências de código apontam para dentro.
"""

import sqlite3
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True, slots=True)
class Pedido:
    cliente: str
    itens: tuple[Decimal, ...]

    def __post_init__(self) -> None:
        if not self.itens:
            raise ValueError("pedido vazio")

    def total(self) -> Decimal:
        return sum(self.itens, Decimal("0"))


class RepositorioDePedidos(Protocol):
    def salvar(self, pedido: Pedido) -> None: ...


class Notificador(Protocol):
    def pedido_confirmado(self, pedido: Pedido) -> None: ...


class FazerPedido:
    def __init__(self, repositorio: RepositorioDePedidos, notificador: Notificador) -> None:
        self._repositorio = repositorio
        self._notificador = notificador

    def __call__(self, cliente: str, itens: tuple[Decimal, ...]) -> Pedido:
        pedido = Pedido(cliente, itens)
        self._repositorio.salvar(pedido)
        self._notificador.pedido_confirmado(pedido)
        return pedido


class RepositorioEmMemoria:
    def __init__(self) -> None:
        self.salvos: list[Pedido] = []

    def salvar(self, pedido: Pedido) -> None:
        self.salvos.append(pedido)


class RepositorioSqlite:
    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        conexao.execute("CREATE TABLE IF NOT EXISTS pedidos (cliente TEXT, total TEXT)")

    def salvar(self, pedido: Pedido) -> None:
        self._conexao.execute(
            "INSERT INTO pedidos VALUES (?, ?)", (pedido.cliente, str(pedido.total()))
        )
