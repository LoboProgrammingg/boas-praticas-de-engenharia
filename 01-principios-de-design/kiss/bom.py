"""KISS aplicado: uma função que faz o que o problema pede.

Simples não é ingênuo: o dinheiro continua em ``Decimal``, nunca em ``float``.
"""

from collections.abc import Iterable
from decimal import Decimal


def total(precos: Iterable[Decimal]) -> Decimal:
    return sum(precos, Decimal(0))
