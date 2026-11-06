"""Mesma regra, agora com os casos de fronteira (valor-limite) que matam os mutantes."""


def pode_comprar_bebida(idade: int) -> bool:
    return idade >= 18


CASOS: tuple[tuple[int, bool], ...] = (
    (30, True),
    (10, False),
    (18, True),
    (17, False),
)
