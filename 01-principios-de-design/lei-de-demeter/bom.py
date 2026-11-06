"""Lei de Demeter aplicada: fale só com seus amigos imediatos.

``calcular_frete`` pergunta ao pedido a cidade de entrega. Como o pedido a obtém
é problema do pedido, e o frete depende de uma porta estreita (``ComEntrega``).
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


class ComEntrega(Protocol):
    def cidade_de_entrega(self) -> str: ...


@dataclass(frozen=True, slots=True)
class Endereco:
    cidade: str


@dataclass(frozen=True, slots=True)
class Cliente:
    nome: str
    endereco: Endereco

    def cidade(self) -> str:
        return self.endereco.cidade


@dataclass(frozen=True, slots=True)
class Pedido:
    cliente: Cliente

    def cidade_de_entrega(self) -> str:
        return self.cliente.cidade()


def calcular_frete(pedido: ComEntrega) -> Decimal:
    if pedido.cidade_de_entrega() == "Recife":
        return Decimal("0")
    return Decimal("25")
