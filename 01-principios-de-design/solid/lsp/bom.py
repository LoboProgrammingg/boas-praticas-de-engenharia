"""LSP respeitado: formas imutáveis que cumprem o mesmo contrato, sem herança enganosa."""

from dataclasses import dataclass, replace
from typing import Protocol


class Forma(Protocol):
    def area(self) -> float: ...


@dataclass(frozen=True, slots=True)
class Retangulo:
    largura: float
    altura: float

    def area(self) -> float:
        return self.largura * self.altura

    def com_largura(self, largura: float) -> "Retangulo":
        return replace(self, largura=largura)


@dataclass(frozen=True, slots=True)
class Quadrado:
    lado: float

    def area(self) -> float:
        return self.lado**2


def area_total(formas: list[Forma]) -> float:
    return sum(forma.area() for forma in formas)
