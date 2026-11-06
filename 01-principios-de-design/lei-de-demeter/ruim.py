"""Lei de Demeter violada: o chamador navega pela estrutura interna do pedido.

``calcular_frete`` conhece Pedido, Cliente e Endereco. Se qualquer ligação da
cadeia mudar, todo código que a percorre quebra.
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Endereco:
    cidade: str


@dataclass(frozen=True, slots=True)
class Cliente:
    nome: str
    endereco: Endereco


@dataclass(frozen=True, slots=True)
class Pedido:
    cliente: Cliente


def calcular_frete(pedido: Pedido) -> Decimal:
    if pedido.cliente.endereco.cidade == "Recife":
        return Decimal("0")
    return Decimal("25")
