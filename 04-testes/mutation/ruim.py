"""Suíte com 100% de cobertura de linhas e que não protege a regra.

Os dois casos executam todas as linhas de ``pode_comprar_bebida``, mas nenhum deles testa a
fronteira dos 18 anos: trocar ``>=`` por ``>`` não derruba o teste.
"""


def pode_comprar_bebida(idade: int) -> bool:
    return idade >= 18


CASOS: tuple[tuple[int, bool], ...] = (
    (30, True),
    (10, False),
)
