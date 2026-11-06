"""Monólito modular: módulos conversam apenas por uma API pública (porta).

``Pedidos`` depende de ``ApiDeEstoque``. Hoje a implementação roda no mesmo processo
(``EstoqueLocal``: uma chamada de função). Se um dia o estoque virar um serviço, só o
adaptador (``EstoqueRemoto``) muda, e com ele aparecem os problemas de rede, que o módulo
local nunca teve: timeout e falha parcial.
"""

from collections.abc import Callable
from typing import Protocol


class FalhaDeRedeError(Exception):
    """A chamada ao outro serviço falhou: algo que não existe dentro do mesmo processo."""


class ApiDeEstoque(Protocol):
    def reservar(self, sku: str, quantidade: int) -> bool: ...


class EstoqueLocal:
    def __init__(self, saldos: dict[str, int]) -> None:
        self._saldos = saldos

    def reservar(self, sku: str, quantidade: int) -> bool:
        if self._saldos.get(sku, 0) < quantidade:
            return False
        self._saldos[sku] -= quantidade
        return True


class EstoqueRemoto:
    """Adaptador para o estoque como serviço; ``chamada`` representa o HTTP."""

    def __init__(self, chamada: Callable[[str, int], bool]) -> None:
        self._chamada = chamada

    def reservar(self, sku: str, quantidade: int) -> bool:
        return self._chamada(sku, quantidade)


class Pedidos:
    def __init__(self, estoque: ApiDeEstoque) -> None:
        self._estoque = estoque

    def fazer(self, sku: str, quantidade: int) -> bool:
        return self._estoque.reservar(sku, quantidade)
