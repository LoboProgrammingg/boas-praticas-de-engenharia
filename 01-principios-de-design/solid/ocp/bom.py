"""OCP aplicado: novos descontos entram por extensão, sem editar o que já funciona."""

from collections.abc import Callable
from decimal import Decimal

type Desconto = Callable[[Decimal], Decimal]


class TabelaDeDescontos:
    def __init__(self) -> None:
        self._descontos: dict[str, Desconto] = {"nenhum": lambda preco: preco}

    def registrar(self, nome: str, desconto: Desconto) -> None:
        if nome in self._descontos:
            raise ValueError(f"Desconto '{nome}' já registrado.")
        self._descontos[nome] = desconto

    def aplicar(self, nome: str, preco: Decimal) -> Decimal:
        try:
            return self._descontos[nome](preco)
        except KeyError:
            raise ValueError(f"Desconto '{nome}' desconhecido.") from None


def percentual(fator: str) -> Desconto:
    multiplicador = Decimal(fator)
    return lambda preco: preco * multiplicador
