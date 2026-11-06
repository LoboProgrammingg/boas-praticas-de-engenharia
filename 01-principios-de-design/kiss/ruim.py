"""KISS violado: fábrica, estratégia e registro para somar uma lista de preços.

São quatro peças móveis para fazer o que ``sum`` já faz, e a escolha da estratégia
por texto só falha em tempo de execução.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from decimal import Decimal


class EstrategiaDeSoma(ABC):
    @abstractmethod
    def executar(self, precos: Iterable[Decimal]) -> Decimal: ...


class SomaSimples(EstrategiaDeSoma):
    def executar(self, precos: Iterable[Decimal]) -> Decimal:
        total = Decimal(0)
        for preco in precos:
            total += preco
        return total


class FabricaDeEstrategias:
    def __init__(self) -> None:
        self._registro: dict[str, type[EstrategiaDeSoma]] = {"soma": SomaSimples}

    def criar(self, nome: str) -> EstrategiaDeSoma:
        return self._registro[nome]()


def total(precos: Iterable[Decimal]) -> Decimal:
    return FabricaDeEstrategias().criar("soma").executar(precos)
