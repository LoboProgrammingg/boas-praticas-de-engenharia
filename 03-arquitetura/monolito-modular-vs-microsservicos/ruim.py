"""Monólito "bola de lama": o módulo de pedidos mexe direto nas entranhas do estoque.

Não há fronteira. ``Pedidos`` lê o dicionário interno de ``Estoque``; renomear essa
estrutura quebra pedidos, e separar os dois em serviços exigiria reescrever tudo.
"""


class Estoque:
    def __init__(self, saldos: dict[str, int]) -> None:
        self._saldos = saldos


class Pedidos:
    def __init__(self, estoque: Estoque) -> None:
        self._estoque = estoque

    def fazer(self, sku: str, quantidade: int) -> bool:
        if self._estoque._saldos.get(sku, 0) < quantidade:
            return False
        self._estoque._saldos[sku] -= quantidade
        return True
