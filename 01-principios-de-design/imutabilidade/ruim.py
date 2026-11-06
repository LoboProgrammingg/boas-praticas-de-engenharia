"""Mutação do argumento: quem guardou uma referência vê o valor mudar por baixo.

O "histórico" e o carrinho atual são o mesmo objeto; qualquer função que receba a
lista pode alterá-la sem que o chamador perceba.
"""


def adicionar_item(carrinho: list[str], item: str) -> None:
    carrinho.append(item)
