"""OCP violado: cada novo tipo de desconto obriga a editar a mesma função."""

from decimal import Decimal


def preco_com_desconto(tipo: str, preco: Decimal) -> Decimal:
    if tipo == "black_friday":
        return preco * Decimal("0.8")
    if tipo == "cliente_vip":
        return preco * Decimal("0.9")
    return preco
