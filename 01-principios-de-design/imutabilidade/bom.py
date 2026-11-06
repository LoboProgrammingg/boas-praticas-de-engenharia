"""Valor imutável: cada alteração devolve um carrinho novo e o original fica intacto.

Pode ser guardado em histórico, compartilhado entre threads e usado como chave de
dicionário sem cópia defensiva.
"""

from dataclasses import dataclass, replace


@dataclass(frozen=True, slots=True)
class Carrinho:
    itens: tuple[str, ...] = ()


def adicionar_item(carrinho: Carrinho, item: str) -> Carrinho:
    return replace(carrinho, itens=(*carrinho.itens, item))
